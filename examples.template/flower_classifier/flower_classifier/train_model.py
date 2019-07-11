# -*- coding: utf-8 -*-
"""
    Treatment in charge of training the model.
"""
import logging
import math
import pickle
import sys
from pathlib import Path
from typing import Tuple, Sequence, Mapping, Optional, Any, Iterator

import click
import click_pathlib
import dotenv
import numpy as np
import tensorflow as tf
import keras
from keras.applications import vgg16, VGG19
from keras.callbacks import Callback, TensorBoard
from keras.layers import Input, Dense, Flatten, Lambda, Dropout
from keras.utils import np_utils
from sklearn.model_selection import train_test_split

from flower_classifier.tools.tools import decode_and_resize_image, Glob, load_images, init_logger

LOGGER = logging.getLogger(__name__)

Model = keras.Model


def _create_model(input_shape: Tuple[int, int, int], classes: int) -> Model:
    """
      use VGG19
    """
    model = VGG19(weights="imagenet",
                  include_top=False,
                  input_shape=input_shape)

    # Freeze the layers which you don't want to train. Here I am freezing the first 5 layers.
    for layer in model.layers[:1]:
        layer.trainable = False

    # Adding custom Layers
    x = model.output
    x = Flatten()(x)
    x = Dense(1024, activation="relu")(x)
    x = Dropout(0.5)(x)
    x = Dense(1024, activation="relu")(x)
    predictions = Dense(classes, activation="softmax", name='predictions')(x)

    # creating the final model
    final_model = Model(inputs=model.input, outputs=predictions)

    final_model.compile(loss='categorical_crossentropy', optimizer='adam',
                        metrics=['acc'])  # optimizer=RMSprop(lr=0.001)

    return final_model


class _MLflowLogger(Callback):
    """
    Keras callback for logging metrics and final model with MLflow.

    Metrics are logged after every epoch. The logger keeps track of the best model based on the
    validation metric. At the end of the training, the best model is logged with MLflow.
    """

    def __init__(self,
                 model: Model,
                 x_train: np.array,
                 y_train: np.array,
                 x_valid: np.array,
                 y_valid: np.array,
                 **kwargs):
        super(_MLflowLogger, self).__init__()
        self._model = model
        self._best_val_loss = math.inf
        self._train = (x_train, y_train)
        self._valid = (x_valid, y_valid)
        self._pyfunc_params = kwargs
        self._best_weights = None

    def on_epoch_end(self, epoch: int, logs=None):
        """
        Log Keras metrics with MLflow. Update the best model if the model improved on the validation
        data.
        """
        if not logs:
            return
        # for name, value in logs.items():
        #     if name.startswith("val_"):
        #         name = "valid_" + name[4:]
        #     else:
        #         name = "train_" + name
        #     mlflow.log_metric(name, value)
        val_loss = logs["val_loss"]
        if val_loss < self._best_val_loss:
            # Save the "best" weights
            self._best_val_loss = val_loss
            self._best_weights = [x.copy() for x in self._model.get_weights()]

    def on_train_end(self, logs=None):
        """
        Log the best model with MLflow and evaluate it on the train and validation data so that the
        metrics stored with MLflow reflect the logged model.
        """
        # self._model.set_weights(self._best_weights)
        # x, y = self._train
        # train_res = self._model.evaluate(x=x, y=y)
        # for name, value in zip(self._model.metrics_names, train_res):
        #     LOGGER.info("train_%s=%s", name, value)
        #     # mlflow.log_metric("train_{}".format(name), value)
        # x, y = self._valid
        # valid_res = self._model.evaluate(x=x, y=y)
        # for name, value in zip(self._model.metrics_names, valid_res):
        #     LOGGER.info("valid_%s=%s", name, value)
        #     # mlflow.log_metric("valid_{}".format(name), value)


def train_model(
        domain: Mapping[str, int],
        labels: Sequence[int],
        image_datas: Iterator[np.array],
        test_ratio: float,
        epochs: int = 1,
        batch_size: int = 1,
        image_width: int = 224,
        image_height: int = 224,
        seed: Optional[int] = None,
        logdir: Path="./logdir/") -> Model:
    """ Train VGG19 model on provided image files.

        May be called in Tensorflow session.

        :param labels: Sequence of labels for the image files.
        :param domain: Dictionary representing the domain of the reponse.
                       Provides mapping label-name -> label-id.
        :param image_datas: iterator of nparray with image in float normalisation
        :param test_ratio: Ration beetween train and test. (default 0.2)
        :param epoch: Maximum number of epochs to evaluate. (default 1)
        :param batch_size: Batch size passed to the learning algo. (default 1)
        :param image_width: Input image width in pixels. (default 224)
        :param image_height: Input image height in pixels. (default 224)
        :param seed: Force seed (default None)
        :return: The trained model
    """
    meta_parameters = {
        "test_ratio": test_ratio,
        "image_width": image_width,
        "image_height": image_height,
        "epochs": epochs,
        "batch_size": batch_size,
        "seed": seed
    }
    LOGGER.info("Training model with the following parameters: %s", meta_parameters)

    LOGGER.info("Domain: %s", domain)

    assert len(set(labels)) == len(domain)

    input_shape = (image_width, image_height, 3)

    # PPR dims = input_shape[:2]
    x = np.array([datas for datas in image_datas])
    y = np_utils.to_categorical(np.array(labels), num_classes=len(domain))
    train_size = 1 - test_ratio
    x_train, x_valid, y_train, y_valid = train_test_split(x, y, random_state=seed,
                                                          train_size=train_size)
    model = _create_model(input_shape=input_shape, classes=len(domain))
    model.compile(
        optimizer=keras.optimizers.SGD(decay=1e-5, nesterov=True, momentum=.9),
        loss=keras.losses.categorical_crossentropy,
        metrics=["accuracy"])
    sorted_domain = sorted(domain.keys(), key=lambda x: domain[x])
    logger = _MLflowLogger(model=model,
                           x_train=x_train,
                           y_train=y_train,
                           x_valid=x_valid,
                           y_valid=y_valid,
                           artifact_path="model",
                           domain=sorted_domain,
                           image_dims=input_shape)
    tensorboard = TensorBoard(log_dir=logdir)
    model.fit(
        x=x_train,
        y=y_train,
        validation_data=(x_valid, y_valid),
        epochs=epochs,
        batch_size=batch_size,
        callbacks=[logger, tensorboard])

    return model


@click.command(help="Trains an Keras model on flower_photos dataset."
                    "Parameters:"
                    "- The input is expected as a directory tree with pictures for each category in a"
                    " folder named by the category, or a glob path."
                    "- The output is the model file path (.h5 extension)."
                    "- The domain file path (.pkl extension)")
@click.argument('input_files', type=Glob(default_suffix="**/*.jpg"))
@click.argument('model_filepath', type=click_pathlib.Path(file_okay=True))
@click.argument('domain_filepath', type=click_pathlib.Path(dir_okay=True))
# Hyper parameters
@click.option("--epochs", type=click.INT, default=1, help="Maximum number of epochs to evaluate.")
@click.option("--batch-size", type=click.INT, default=1,
              help="Batch size passed to the learning algo.")
@click.option("--image-width", type=click.INT, default=224, help="Input image width in pixels.")
@click.option("--image-height", type=click.INT, default=224, help="Input image height in pixels.")
@click.option("--test-ratio", type=click.FLOAT, default=0.2)
@click.option("--seed", type=click.INT, help="Seed for the random generator.")
@click.option('--logdir', type=click_pathlib.Path(), help='Tensorflow logdir', default="./logdir/")
def main(input_files: Sequence[Path],
         model_filepath: Path,
         domain_filepath: Path,
         test_ratio: float,
         epochs: int,
         batch_size: int,
         image_width: int,
         image_height: int,
         seed: Optional[int],
         logdir: Path) -> int:
    """ Train the model from input_filepath and save it in model_filepath

        :param input_filepath: glob data file path
        :param model_filepath: file to write the model
        :param epoch: Value of epoch (default 128)
        :param batch_size: Value of batch size (default 1024)
        :param seed: The initial seed (default None)
        :param logdir: Tensorboard logdir (default None)
        :return: 0 if ok, else error
    """
    LOGGER.info('Train model from processed and featured data')

    with tf.Graph().as_default() as graph:  # pylint: disable=E1129
        with tf.Session(graph=graph).as_default():  # pylint: disable=E1129
            # 1. Load datas
            model_filepath = Path(model_filepath)
            labels, domain, image_datas = load_images(input_files)

            # 2. Train the model
            model = train_model(
                domain,
                labels,
                iter(image_datas),
                test_ratio,
                epochs,
                batch_size,
                image_width,
                image_height,
                seed,
                logdir)

            # 3. Save the model
            model.save(str(model_filepath))
            # mlflow.keras.save_model(model, path=model_filepath.with_suffix(".h5"))
            with open(domain_filepath, 'wb') as domain_file:
                pickle.dump(domain, domain_file)
    return 0


if __name__ == '__main__':
    init_logger(LOGGER, logging.INFO)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    dotenv.load_dotenv(dotenv.find_dotenv())

    sys.exit(main())  # pylint: disable=E1120

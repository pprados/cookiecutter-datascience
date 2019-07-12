# -*- coding: utf-8 -*-
"""
    Treatment in charge of training the model.
"""
import logging
import math
import sys
from pathlib import Path
from typing import Tuple, Sequence, Mapping, Optional, Iterator

import click
import click_pathlib
import dotenv
import keras
import numpy as np
import tensorflow as tf
from keras.applications import VGG19
from keras.callbacks import Callback, TensorBoard
from keras.layers import Dense, Flatten, Dropout
from keras.utils import np_utils
from sklearn.model_selection import train_test_split

from flower_classifier.tools.tools import init_logger, save_model_and_domain, Glob, load_images, Model

LOGGER = logging.getLogger(__name__)

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


def train_model(
        domain: Mapping[str, int],
        labels: Sequence[int],
        image_datas: Iterator[np.array],
        test_ratio: float,
        epochs: int = 1,
        batch_size: int = 1,
        dim: Tuple[int, int] = (224, 224),
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
        :param dim: Input image width and height in pixels. (default 224,224)
        :param seed: Force seed (default None)
        :param logdir: Tensorflow logdir
        :return: The trained model
    """
    meta_parameters = {
        "test_ratio": test_ratio,
        "image_width": dim[0],
        "image_height": dim[1],
        "epochs": epochs,
        "batch_size": batch_size,
        "seed": seed
    }
    LOGGER.info("Training model with the following parameters: %s", meta_parameters)

    assert len(set(labels)) == len(domain)

    input_shape = (dim[0], dim[1], 3)

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
    model.fit(
        x=x_train,
        y=y_train,
        validation_data=(x_valid, y_valid),
        epochs=epochs,
        batch_size=batch_size,
        callbacks=[TensorBoard(log_dir=logdir)])

    return model


@click.command(short_help="Train model")
@click.argument('input_files', metavar='<selected files>', type=Glob(default_suffix="**/*.jpg"))
@click.argument('model_filepath', metavar='<model>', type=click_pathlib.Path(file_okay=True))
@click.argument('domain_filepath', metavar='<domain>', type=click_pathlib.Path(dir_okay=True))
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
    """
    Train the model with glob <selected files>, and save in <model> and <domain>.

    \b
    Parameters:
    - The input is expected as a directory tree with pictures for each category in a
     folder named by the category, or a glob path.
    - The output file path (.h5 extension).
    - The domain file path (.pkl extension)
    """
    LOGGER.info('Train model from processed and featured data')

    with tf.Graph().as_default() as graph:  # pylint: disable=E1129
        with tf.Session(graph=graph).as_default():  # pylint: disable=E1129
            # 1. Load datas
            dim = (image_width, image_height)
            labels, domain, image_datas = load_images(input_files)

            # 2. Train the model
            model = train_model(
                domain,
                labels,
                iter(image_datas),
                test_ratio,
                epochs,
                batch_size,
                dim,
                seed,
                logdir)

            # 3. Save the model
            save_model_and_domain(model_filepath, model,
                                  domain_filepath, domain)
    return 0


if __name__ == '__main__':
    init_logger(LOGGER, logging.INFO)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    dotenv.load_dotenv(dotenv.find_dotenv())

    sys.exit(main())  # pylint: disable=E1120

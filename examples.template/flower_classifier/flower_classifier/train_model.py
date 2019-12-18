# -*- coding: utf-8 -*-
"""
    Treatment in charge of training the model.
"""
import logging
import sys
from pathlib import Path
from typing import Tuple, Sequence, Mapping, Optional, Iterable, Dict, List

import click
import click_pathlib
import dotenv
import numpy as np
from PIL import Image
from keras.callbacks import TensorBoard
from keras.layers import Conv2D, MaxPool2D, Flatten, Dense
from keras.models import Sequential
from sklearn.model_selection import train_test_split

from flower_classifier.tools.tools import init_logger, save_model_and_domain, Glob, Model, normalize_image
from flower_classifier.tools import DEFAULT_TEST_RATIO, DEFAULT_EPOCHS, DEFAULT_BATCH_SIZE, DEFAULT_IMAGE_SIZE

LOGGER = logging.getLogger(__name__)


def _create_model(input_shape: Tuple[int, int, int], classes: int) -> Model:
    model = Sequential()
    model.add(Conv2D(16, (2, 2), input_shape=input_shape, activation='relu'))
    model.add(MaxPool2D(pool_size=(2, 2)))
    model.add(Conv2D(32, (2, 2), activation='relu'))
    model.add(MaxPool2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(classes, activation='softmax'))

    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    return model


def train_model(
        domain: Mapping[str, int],
        labels: Sequence[int],
        image_datas: Iterable[np.ndarray],
        test_ratio: float = DEFAULT_TEST_RATIO,
        epochs: int = DEFAULT_EPOCHS,
        batch_size: int = DEFAULT_BATCH_SIZE,
        dims: Tuple[int, int] = (DEFAULT_IMAGE_SIZE, DEFAULT_IMAGE_SIZE),
        seed: Optional[int] = None,
        logdir: Path = "./logdir/") -> Model:
    """ Train model on provided image files.

        :param labels: Sequence of labels for the image files.
        :param domain: Dictionary representing the domain of the reponse.
                       Provides mapping label-name -> label-id.
        :param image_datas: iterator of ndarray with image in float normalisation
        :param test_ratio: Ration beetween train and test. (default 0.2)
        :param epochs: Maximum number of epochs to evaluate. (default 1)
        :param batch_size: Batch size passed to the learning algo. (default 1)
        :param dims: Input image width and height in pixels. (default 224,224)
        :param seed: Force seed (default None)
        :param logdir: Tensorflow logdir
        :return: The trained model
    """
    meta_parameters = {
        "test_ratio": test_ratio,
        "image_width": dims[0],
        "image_height": dims[1],
        "epochs": epochs,
        "batch_size": batch_size,
        "seed": seed
    }
    LOGGER.info("Training model with the following parameters: %s", meta_parameters)

    assert len(set(labels)) == len(domain)

    model = _create_model(input_shape=dims + (3,), classes=len(domain))

    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    x = np.array(list(image_datas))
    y = np.array(list(labels))
    x_train, x_valid, y_train, y_valid = train_test_split(x, y,
                                                          random_state=seed,
                                                          train_size=1 - test_ratio)

    model.fit(
        x=x_train,
        y=y_train,
        validation_data=(x_valid, y_valid),
        epochs=epochs,
        batch_size=batch_size,
        callbacks=[TensorBoard(log_dir=logdir)])

    return model


def _load_images(files: Iterable[Path], dim: Tuple[int, int]) -> \
        Tuple[List[int], Dict[str, int], np.ndarray]:
    """
    Load iterator and returns data and labels
    :param files: Iterable of Path
    :return: labels, domain and images
    """
    labels: List[int] = []
    domain: Dict[str, int] = {}
    image_datas: List[bytes] = []
    for file in files:
        with Image.open(file).resize(dim) as image_file:
            clazz = Path(file).parts[-2:-1][0]
            if clazz not in domain:
                domain[clazz] = len(domain)
            labels.append(domain[clazz])
            image = normalize_image(np.array(image_file, dtype=float))
            image_datas.append(image)
    return labels, domain, image_datas


@click.command(short_help="Train model")
@click.argument('input_files', metavar='<selected files>', type=Glob(default_suffix="**/*.jpg"))
@click.argument('model_filepath', metavar='<model>', type=click_pathlib.Path(file_okay=True))
@click.argument('domain_filepath', metavar='<domain>', type=click_pathlib.Path(dir_okay=True))
@click.option('--logdir', type=click_pathlib.Path(), help='Tensorflow logdir', default="./logdir/")
# Hyper parameters
@click.option("--epochs", type=click.INT, default=DEFAULT_EPOCHS, help="Maximum number of epochs to evaluate.")
@click.option("--batch-size", type=click.INT, default=DEFAULT_BATCH_SIZE,
              help="Batch size passed to the learning algo.")
@click.option("--image-width", type=click.INT, default=DEFAULT_IMAGE_SIZE, help="Input image width in pixels.")
@click.option("--image-height", type=click.INT, default=DEFAULT_IMAGE_SIZE, help="Input image height in pixels.")
@click.option("--test-ratio", type=click.FLOAT, default=DEFAULT_TEST_RATIO)
@click.option("--seed", type=click.INT, help="Seed for the random generator.")
def main(input_files: Iterable[Path], model_filepath: Path, domain_filepath: Path,
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

    # 1. Load datas
    dim = (image_width, image_height)
    labels, domain, image_datas = _load_images(input_files, dim)

    # 2. Train the model
    model = train_model(
        domain, labels, image_datas,
        test_ratio, epochs, batch_size,
        dim, seed, logdir)

    # 3. Save the model
    save_model_and_domain(model_filepath, model,
                          domain_filepath, domain)
    return 0


if __name__ == '__main__':
    init_logger(LOGGER, logging.INFO)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    if not getattr(sys, 'frozen') and hasattr(sys, '_MEIPASS'):
        dotenv.load_dotenv(dotenv.find_dotenv())

    sys.exit(main())  # pylint: disable=E1120

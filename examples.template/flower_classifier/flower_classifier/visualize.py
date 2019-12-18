# -*- coding: utf-8 -*-
"""
    Treatment in charge of training visualize the results.
"""
import logging
import pickle
import sys
from pathlib import Path
from typing import Mapping, Iterable, Tuple
from typing import Sequence

import click
import click_pathlib
import dotenv
import numpy as np
from PIL import Image
from keras.models import Model
from keras.models import load_model
from matplotlib import pyplot as plt

from flower_classifier.tools import DEFAULT_IMAGE_SIZE
from flower_classifier.tools.tools import normalize_image, init_logger, Glob

LOGGER = logging.getLogger(__name__)


def visualize(file_names: Sequence[Path],
              input_files: Iterable[np.array],
              model: Model,
              domains: Mapping[str, int],
              interactive: bool) -> None:
    """ Visualize the results

        :param file_names list of filename
        :param input_files list of array of image
        :param model The trained model
        :param domains A list of domain
        :param interactive Show image or just print prediction
        :return: 0 if ok, else error
    """
    domains_name = {v: k for k, v in domains.items()}
    max_items = 6
    nb_cols = 2
    for i, image in enumerate(input_files):
        predict = model.predict(np.expand_dims(image, axis=0))
        label = domains_name[np.argmax(predict)]
        if interactive:
            byte_image = ((image + 1) * 127.5).astype(np.uint8)
            plt.subplot(max_items // nb_cols, nb_cols, (i % max_items) + 1)
            plt.title(label)
            plt.imshow(byte_image)  # PPR: Bug d'affichage et de prédiction
        else:
            print(f"{file_names[i]} = {label}")
        if interactive and not (i + 1) % max_items:
            plt.show()

    if interactive:
        plt.show()


def _load_images_predict(files: Iterable[Path], dims: Tuple[int, int]) -> Iterable[Sequence[bytes]]:
    """
    Load iterator and returns images
    :param files: A list of Path
    :param dims: Dimension of target image
    :return: Se
    """
    for file in files:
        with Image.open(file).resize(dims) as image_file:
            yield normalize_image(np.array(image_file, dtype=float))


@click.command(help="Apply the model")
@click.argument('input_files', metavar='<selected files>', type=Glob(default_suffix="**/*.jpg"))
@click.argument('model_filepath', metavar='<model>', type=click_pathlib.Path(exists=True))
@click.argument('domain_filepath', metavar='<domain>', type=click_pathlib.Path(exists=True))
@click.option("--image-width", type=click.INT, default=DEFAULT_IMAGE_SIZE, help="Input image width in pixels.")
@click.option("--image-height", type=click.INT, default=DEFAULT_IMAGE_SIZE, help="Input image height in pixels.")
@click.option("--interactive", type=click.BOOL, default=True, help="Wait user input ?")
def main(input_files: Sequence[Path],
         model_filepath: Path,
         domain_filepath: Path,
         image_width: int,  # PPR
         image_height: int,
         interactive: bool) -> int:
    """ Apply the <model> and <model> on glob <selected files>
    """
    LOGGER.info('Visualize the results')

    # 1. Load datas
    images = _load_images_predict(input_files, (image_width, image_height))
    model = load_model(str(model_filepath))
    with open(str(domain_filepath), 'rb') as domain_file:
        domain: Mapping[str, int] = pickle.load(domain_file)

    # 2. Visualize datas
    visualize(input_files, list(images), model, domain, interactive)

    return 0


if __name__ == '__main__':
    init_logger(LOGGER, logging.INFO)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    if not getattr(sys, 'frozen') and hasattr(sys, '_MEIPASS'):
        dotenv.load_dotenv(dotenv.find_dotenv())

    sys.exit(main())  # pylint: disable=E1120

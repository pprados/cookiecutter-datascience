# -*- coding: utf-8 -*-
"""
    Treatment in charge of preparing the dataset.
    (change format, cleaning, etc).
"""
import logging
import sys
import tarfile
from pathlib import Path
from typing import Tuple, Sequence, IO, Iterator

import click
import click_pathlib
import dotenv
import numpy as np
from PIL import Image
from flower_classifier.tools.tools import init_logger

LOGGER = logging.getLogger(__name__)


def prepare_dataset(streams: Iterator[Tuple[Path, IO[bytes]]],
                    image_width: int = 224,
                    image_height: int = 224,
                    ) -> Iterator[Tuple[Path, np.array]]:
    """ Extract and resize image from streams

        :param streams: List of tuple with path and IOBase
        :param image_width: Target image width
        :param image_height: Target image height
        :return: Array of tuple with filename and dataframe
    """
    size = (image_width, image_height)
    for path, stream in streams:
        image = Image.open(stream).resize(size)
        yield (path, np.array(image))


@click.command()
@click.argument('input_raw_filepath', type=click_pathlib.Path(exists=True, file_okay=True))
@click.argument('output_prepared_path', type=click_pathlib.Path(dir_okay=True))
@click.option("--image-width", type=click.INT, default=224, help="Input image width in pixels.")
@click.option("--image-height", type=click.INT, default=224, help="Input image height in pixels.")
def main(input_raw_filepath: Path,
         output_prepared_path: Path,
         image_width: int,
         image_height: int) -> int:
    """ Process to turn raw data file into prepared data file.

        :param input_raw_filepath: data file path
        :param output_prepared_path: directory to write prepared datas
        :return: 0 if ok, else error
    """
    LOGGER.info("Extract and resize images from %s", input_raw_filepath)

    output_prepared_path.mkdir(parents=True, exist_ok=True)

    def extract_tgz(tgz_filepath: Path) -> Iterator[Tuple[Path, tarfile.ExFileObject]]:
        with tarfile.open(tgz_filepath) as tar:
            # Open tgz
            for tarf in tar:
                if tarf.isfile() and tarf.name.endswith('.jpg'):
                    path = Path(tarf.name)
                    path = path.relative_to(*path.parts[:1])
                    yield (path, tar.extractfile(tarf))

    # Write files
    output_prepared_path.touch()
    for (uname, flower) in prepare_dataset(extract_tgz(input_raw_filepath),
                                           image_width=image_width,
                                           image_height=image_height):
        target_path = output_prepared_path.joinpath(uname)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        while True:
            target_path = target_path.parent
            if str(target_path) != ".":
                target_path.touch()
            else:
                break

        Image.fromarray(flower).save(output_prepared_path.joinpath(uname))
    return 0


if __name__ == '__main__':
    init_logger(LOGGER, logging.INFO)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    dotenv.load_dotenv(dotenv.find_dotenv())

    sys.exit(main())  # pylint: disable=E1120

# -*- coding: utf-8 -*-
"""
    Treatment in charge of preparing the dataset.
    (change format, cleaning, etc).
"""
import logging
import sys
import tarfile
from pathlib import Path
from typing import Tuple, IO, Iterable

import click
import click_pathlib
import dotenv
import numpy as np
from PIL import Image

from flower_classifier.tools import DEFAULT_IMAGE_SIZE
from flower_classifier.tools.tools import normalize_image, init_logger

LOGGER = logging.getLogger(__name__)


def prepare_dataset(opened_files: Iterable[Tuple[Path, IO[bytes]]],
                    dim: Tuple[int, int] = (224, 224),
                    ) -> Iterable[Tuple[Path, np.ndarray]]:
    """ Extract and resize image from streams

        :param opened_files: List of tuple with path and IOBase
        :param dim: Input image width and height in pixels. (default 224,224)
        :return: Array of tuple with filename and dataframe
    """
    for path, stream in opened_files:
        image = normalize_image(np.asarray(Image.open(stream).resize(dim)))
        yield (path, image)


@click.command(short_help="Prepare dataset")
@click.argument('input_raw_filepath', metavar='<tgz file>', type=click_pathlib.Path(exists=True, file_okay=True))
@click.argument('output_prepared_path', metavar='<target>', type=click_pathlib.Path(dir_okay=True))
@click.option("--image-width", type=click.INT, default=DEFAULT_IMAGE_SIZE, help="Input image width in pixels.")
@click.option("--image-height", type=click.INT, default=DEFAULT_IMAGE_SIZE, help="Input image height in pixels.")
def main(input_raw_filepath: Path,
         output_prepared_path: Path,
         image_width: int,
         image_height: int) -> int:
    """
    This script extract and resize images from <tgz file> to <target>
    """
    LOGGER.info("Extract and resize images from '%s'", input_raw_filepath)

    output_prepared_path.mkdir(parents=True, exist_ok=True)
    dim = (image_width, image_height)

    def extract_tgz(tgz_filepath: Path) -> Iterable[Tuple[Path, IO[bytes]]]:
        with tarfile.open(tgz_filepath) as tar:
            # Open tgz
            for tarf in tar:
                if tarf.isfile() and tarf.name.endswith('.jpg'):
                    path = Path(tarf.name)
                    path = path.relative_to(*path.parts[:1])
                    yield (path, tar.extractfile(tarf))

    # Write files
    output_prepared_path.touch()
    for (uname, flower) in prepare_dataset(extract_tgz(input_raw_filepath), dim):
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
    if not getattr(sys, 'frozen') and hasattr(sys, '_MEIPASS'):
        dotenv.load_dotenv(dotenv.find_dotenv())

    sys.exit(main(standalone_mode=False))  # pylint: disable=no-value-for-parameter,unexpected-keyword-arg

# -*- coding: utf-8 -*-
"""
    Treatment in charge of preparing the dataset.
    (change format, cleaning, etc).
"""
import io
import logging
import os
import sys
import tarfile
from pathlib import Path
from typing import List, Tuple, Sequence, IO

import click
import click_pathlib
import dotenv

from flower_classifier.tools.tools import init_logger

LOGGER = logging.getLogger(__name__)


def prepare_dataset(streams: Sequence[Tuple[Path, IO[bytes]]]) -> Sequence[Tuple[Path, bytes]]:
    """ Extract image from tgz stream

        :param streams: List of tuple with path and IOBase
        :return: Array of tuple with filename and dataframe
    """
    flowers: List[Tuple[str, bytes]] = []
    for path, stream in streams:
        flowers.append((path, stream.read()))
    return flowers


@click.command()
@click.argument('input_raw_filepath', type=click_pathlib.Path(exists=True, file_okay=True))
@click.argument('output_prepared_path', type=click_pathlib.Path(dir_okay=True))
def main(input_raw_filepath: Path,
         output_prepared_path: Path) -> int:
    """ Process to turn raw data file into prepared data file.

        :param input_raw_filepath: data file path
        :param output_prepared_path: directory to write prepared datas
        :return: 0 if ok, else error
    """
    LOGGER.info("Extract %s", input_raw_filepath)

    output_prepared_path.mkdir(parents=True, exist_ok=True)

    with tarfile.open(input_raw_filepath) as tar:
        # Open tgz
        streams: List[Tuple[Path, io.BufferedReader]] = []
        for tarf in tar:
            if tarf.isfile():
                path = Path(tarf.name)
                # Remove first part
                path = path.relative_to(*path.parts[:1])
                streams.append((path, tar.extractfile(tarf)))

        # Write files
        output_prepared_path.touch()
        for (uname, flower) in prepare_dataset(streams):
            target_path = Path(output_prepared_path, uname)
            target_path.parent.mkdir(parents=True, exist_ok=True)
            while True:
                target_path = target_path.parent
                if str(target_path) != ".":
                    target_path.touch()
                else:
                    break

            with io.open(os.path.join(output_prepared_path, uname), "w+b") as output:
                output.write(flower)
    return 0


if __name__ == '__main__':
    init_logger(LOGGER, logging.INFO)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    dotenv.load_dotenv(dotenv.find_dotenv())

    sys.exit(main())  # pylint: disable=E1120

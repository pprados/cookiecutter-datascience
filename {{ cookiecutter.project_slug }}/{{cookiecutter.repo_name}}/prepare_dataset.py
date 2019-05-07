# -*- coding: utf-8 -*-
"""
    Traitement en charge de préparer le dataset (changement de format, nettoyage, etc)
"""

import os
import pathlib
import logging
import shutil

import click
import dotenv

from .tools import *  # pylint: disable=W0401


@click.command()
@click.argument('input_raw_filepath', type=click.Path(exists=True))
@click.argument('output_interim_filepath', type=click.Path())
def main(input_raw_filepath, output_interim_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed and extended with
        features (saved in ../interim).
    """
    logger = logging.getLogger(__name__)
    logger.info('Clean data set from raw data to interim')

    pathlib.Path(os.path.dirname(output_interim_filepath))\
        .mkdir(parents=True, exist_ok=True)
    # FIXME: remove this sample line
    shutil.copyfile(input_raw_filepath, output_interim_filepath)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # not used in this stub but often useful for finding various files
    PROJECT_DIR = pathlib.Path(__file__).resolve().parents[1]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    dotenv.load_dotenv(dotenv.find_dotenv())

    main()  # pylint: disable=E1120

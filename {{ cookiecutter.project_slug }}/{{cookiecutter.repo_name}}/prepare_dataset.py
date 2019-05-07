# -*- coding: utf-8 -*-
import os
import pathlib
from shutil import copyfile

import click
import logging
from dotenv import find_dotenv, load_dotenv

from .tools import *


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
    copyfile(input_raw_filepath, output_interim_filepath)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()

# -*- coding: utf-8 -*-
from shutil import copyfile

import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv


@click.command()
@click.argument('input_raw_filepath', type=click.Path(exists=True))
@click.argument('output_interim_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed and extended with features (saved in ../interim).
    """
    logger = logging.getLogger(__name__)
    logger.info('Clean data set from raw data to interim')

    copyfile(input_filepath, output_filepath) # FIXME: remove this sample line


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()

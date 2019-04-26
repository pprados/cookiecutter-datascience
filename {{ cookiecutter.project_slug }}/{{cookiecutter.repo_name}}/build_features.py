# -*- coding: utf-8 -*-
import os
import pathlib
from shutil import copyfile

import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

@click.command()
@click.argument('input_prepared_filepath', type=click.Path(exists=True))
@click.argument('output_featured_filepath', type=click.Path())
def main(input_prepared_filepath, output_featured_filepath):
    """ Runs data processing scripts to turn raw data from (../interim) into
        extended data (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('add features from prepared data')

    pathlib.Path(os.path.dirname(output_featured_filepath)).mkdir(parents=True, exist_ok=True)
    copyfile(input_prepared_filepath, output_featured_filepath)  # FIXME: remove this sample line

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()

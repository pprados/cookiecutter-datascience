# -*- coding: utf-8 -*-
import os
import pathlib
from shutil import copyfile

import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

from .tools import *


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('model_filepath', type=click.Path())
def main(input_filepath, model_filepath):
    """ Train the model from input_filepath and save it in ../models
    """
    logger = logging.getLogger(__name__)
    logger.info('train model from processed and featured data')

    pathlib.Path(os.path.dirname(model_filepath))\
        .mkdir(parents=True, exist_ok=True)
    copyfile(input_filepath, model_filepath)  # FIXME: remove this sample line


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()

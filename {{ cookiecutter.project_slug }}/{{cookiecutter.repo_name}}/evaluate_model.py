# -*- coding: utf-8 -*-
import os
import pathlib
from shutil import copyfile

import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv


@click.command()
@click.argument('data_filepath', type=click.Path(exists=True))
@click.argument('model_filepath', type=click.Path(exists=True))
@click.argument('evaluate_filepath', type=click.Path())
def main(data_filepath, model_filepath, evaluate_filepath):
    """ Prefict with using the model from model_filepath and data from data_filepath
    """
    logger = logging.getLogger(__name__)
    logger.info('Evaludate model from processed data')

    pathlib.Path(os.path.dirname(evaluate_filepath)).mkdir(parents=True, exist_ok=True)
    copyfile(data_filepath, evaluate_filepath)  # FIXME: remove this sample line

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()

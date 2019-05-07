# -*- coding: utf-8 -*-
"""
    Traitement en charge de l'apprentissage du modèle.
"""

import os
import pathlib
import logging
import shutil

import click
import dotenv

from .tools import *  # pylint: disable=W0401


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
    shutil.copyfile(input_filepath, model_filepath)  # FIXME: remove this sample line


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # not used in this stub but often useful for finding various files
    PROJECT_DIR = pathlib.Path(__file__).resolve().parents[1]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    dotenv.load_dotenv(dotenv.find_dotenv())

    main()  # pylint: disable=E1120

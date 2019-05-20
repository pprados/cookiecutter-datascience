# -*- coding: utf-8 -*-
"""
    Traitement en charge de l'apprentissage du modèle.
"""
import glob
import os
import pathlib
import logging
import shutil
import sys

import click
import dotenv

from .tools import *  # pylint: disable=W0401

logger = logging.getLogger(__name__)


def train_model(input_filepath: str,
                model_filepath: str,
                epoch: int,
                batch_size: int) -> int:
    """ Train the model from input_filepath and save it in ../models

        :param input_filepath: data file path
        :param model_filepath: file to write the model
        :param epoch: Value of epoch (default 128)
        :param batch_size: Value of batch size (default 1024)
        :return: 0 if ok, else error
    """
    pathlib.Path(os.path.dirname(model_filepath)) \
        .mkdir(parents=True, exist_ok=True)
    inputs = [f for f in glob.glob(input_filepath, recursive=True)]
    # TODO: Remplacez la ligne suivante par un apprentissage
    shutil.copyfile(inputs[0], model_filepath)

    return 0


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('model_filepath', type=click.Path())
# hyperparameters sent by the client are passed as command-line arguments to the script.
@click.option('--epoch', default=128, type=int, help='Epoch')
@click.option('--batch-size', default=1024, type=int, help='Batch size')
def main(input_filepath: str,
         model_filepath: str,
         epoch: int,
         batch_size: int) -> int:
    """ Train the model from input_filepath and save it in ../models

        :param input_filepath: glob data file path
        :param model_filepath: file to write the model
        :param epoch: Value of epoch (default 128)
        :param batch_size: Value of batch size (default 1024)
        :return: 0 if ok, else error
    """
    logger.info('train model from processed and featured data')
    return train_model(input_filepath, model_filepath, epoch, batch_size)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # not used in this stub but often useful for finding various files
    PROJECT_DIR = pathlib.Path(__file__).resolve().parents[1]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    dotenv.load_dotenv(dotenv.find_dotenv())

    sys.exit(main())  # pylint: disable=E1120

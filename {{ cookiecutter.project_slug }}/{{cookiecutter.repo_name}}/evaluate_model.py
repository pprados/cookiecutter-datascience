# -*- coding: utf-8 -*-
"""
    Traitement en charge d'évaluer le modèle.
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


def evaluate_model(data_filepath: str, model_filepath: str, evaluate_filepath: str) -> int:
    """ Evaluate the model from model_filepath and data
        from data_filepath

        :param data_filepath: data file path
        :param model_filepath: model file path with features
        :param evaluate_filepath: evaluate file path to write
        :return: 0 if ok, else error
    """
    pathlib.Path(os.path.dirname(evaluate_filepath)) \
        .mkdir(parents=True, exist_ok=True)
    for f in glob.glob(evaluate_filepath, recursive=True):
        pass # TODO
    with open(evaluate_filepath,"w") as file:
        f.write("0.90") # TODO Write AUC or others metrics
    return 0


@click.command()
@click.argument('data_filepath', type=click.Path(exists=True))
@click.argument('model_filepath', type=click.Path(exists=True))
@click.argument('evaluate_filepath', type=click.Path())
def main(data_filepath: str, model_filepath: str, evaluate_filepath: str) -> int:
    """ Evaluate the model from model_filepath and data
        from data_filepath

        :param data_filepath: data file path
        :param model_filepath: model file path with features
        :param evaluate_filepath: evaluate file path to write
        :return: 0 if ok, else error
    """
    logger.info('Evaludate model %s from processed data', model_filepath)
    return evaluate_model(data_filepath, model_filepath, evaluate_filepath)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # not used in this stub but often useful for finding various files
    PROJECT_DIR = pathlib.Path(__file__).resolve().parents[1]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    dotenv.load_dotenv(dotenv.find_dotenv())

    sys.exit(main())  # pylint: disable=E1120

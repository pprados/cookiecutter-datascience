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


def evaluate_model(model_filepath: str, data_filepath: str, evaluate_filepath: str) -> int:
    """ Evaluate the model from model_filepath and data
        from data_filepath

        :param model_filepath: model file path with features
        :param data_filepath: data file path
        :param evaluate_filepath: evaluate file path to write
        :return: 0 if ok, else error
    """
    pathlib.Path(os.path.dirname(evaluate_filepath)) \
        .mkdir(parents=True, exist_ok=True)
    for f in glob.glob(evaluate_filepath, recursive=True):
        pass # TODO PPR Boucle d'eval de fichier ?
    with open(evaluate_filepath,"w") as auc:
        auc.write("0.90") # TODO Remplacez le code pour écriture les métriques dans un fichier au format JSON
    return 0


@click.command()
@click.argument('model_filepath', type=click.Path(exists=True))
@click.argument('data_filepath', type=click.Path(exists=True))
@click.argument('evaluate_filepath', type=click.Path())
def main(model_filepath: str, data_filepath: str, evaluate_filepath: str) -> int:
    """ Evaluate the model from model_filepath and data
        from data_filepath
 PPR : c'est la doc du mode --help
        :param model_filepath: model file path with features
        :param data_filepath: data file path
        :param evaluate_filepath: evaluate file path to write
        :return: 0 if ok, else error
    """
    logger.info('Evaludate model %s from processed data', model_filepath)
    return evaluate_model(model_filepath, data_filepath, evaluate_filepath)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # not used in this stub but often useful for finding various files
    PROJECT_DIR = pathlib.Path(__file__).resolve().parents[1]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    dotenv.load_dotenv(dotenv.find_dotenv())

    sys.exit(main())  # pylint: disable=E1120

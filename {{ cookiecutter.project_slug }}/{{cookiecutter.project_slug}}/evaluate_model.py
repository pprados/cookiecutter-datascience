# -*- coding: utf-8 -*-
"""
    Traitement en charge d'évaluer le modèle.
"""
import glob
import json
import logging
import pickle
import sys
from typing import List

import click
import dotenv

LOGGER = logging.getLogger(__name__)


def evaluate_model(model: str,
                   files: List[str]) -> dict:
    """ Evaluate the model from model and data
        from data_filepath

        :param model: model
        :param data_filepath: data file path
        :param evaluate_filepath: evaluate file path to write
        :return: dictionary with metrics
    """
    metrics = {}
    for a_file in files:
        pass  # TODO Code d'evaluation de chaque fichier
    metrics['auc'] = 0.99
    return metrics


@click.command()
@click.argument('model_filepath', type=click.Path(exists=True))
@click.argument('data_filepath', type=click.Path(exists=True))
@click.argument('evaluate_filepath', type=click.Path())
def main(model_filepath: str,
         data_filepath: str,
         evaluate_filepath: str) -> int:
    """ Evaluate the model from model_filepath and data
        from data_filepath
        :param model_filepath: model file path with features
        :param data_filepath: data file path
        :param evaluate_filepath: evaluate file path to write
        :return: 0 if ok, else error
    """
    LOGGER.info('Evaluate model %s from processed data', model_filepath)

    model = pickle.load(open(model_filepath, 'rb'))
    files = [str(f) for f in glob.glob(data_filepath, recursive=True)]
    metrics = evaluate_model(model, files)
    with open(evaluate_filepath, 'w') as evaluate_file:
        json.dump(metrics, evaluate_file, indent=4)
    return 0


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    dotenv.load_dotenv(dotenv.find_dotenv())

    sys.exit(main())  # pylint: disable=E1120

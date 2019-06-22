# -*- coding: utf-8 -*-
"""
    Treatment in charge of evaluate model
"""
import glob
import json
import logging
import pickle
import sys
from typing import Any, Sequence

import click
import dotenv
import pandas as pd

LOGGER = logging.getLogger(__name__)


def evaluate_model(model: Any,
                   samples: Sequence[pd.DataFrame]) -> dict:
    """ Evaluate the model with sample datas

        :param model: model
        :param samples: A list of samples dataframe
        :return: dictionary with metrics
    """
    metrics = {}
    for a_sample in samples:
        pass  # TODO Code d'evaluation de chaque dataframe
    metrics['auc'] = 0.99
    return metrics


@click.command()
@click.argument('model_filepath', type=click.Path(exists=True))
@click.argument('sample_filepath', type=click.Path(exists=True))
@click.argument('evaluate_filepath', type=click.Path())
def main(model_filepath: str,
         sample_filepath: str,
         evaluate_filepath: str) -> int:
    """ Evaluate the model with samples
        :param model_filepath: model file path
        :param sample_filepath: data files path
        :param evaluate_filepath: json file path with metrics to write
        :return: 0 if ok, else error
    """
    LOGGER.info('Evaluate model %s from processed data', model_filepath)

    model: Any = pickle.load(open(model_filepath, 'rb'))

    datasets: Sequence[pd.DataFrame] = \
        [pd.read_csv(f) for f in glob.glob(sample_filepath, recursive=True)]
    metrics: dict = evaluate_model(model, datasets)
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

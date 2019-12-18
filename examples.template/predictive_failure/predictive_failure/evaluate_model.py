# -*- coding: utf-8 -*-
"""
    Treatment in charge of evaluate model
"""
import json
import logging
import pickle
import sys
from pathlib import Path
from time import strftime, gmtime
from typing import Sequence, Iterator

import click
import click_pathlib
import dotenv
import pandas as pd

from .tools.tools import Glob, init_logger
from .train_model import Model

LOGGER = logging.getLogger(__name__)


def evaluate_model(model: Model,
                   samples: Iterator[pd.DataFrame]) -> dict:
    """ Evaluate the model with sample datas

        :param model: model
        :param samples: A list of samples dataframe
        :return: dictionary with metrics
    """
    LOGGER.info('Evaluate model')

    metrics = {}
    for a_sample in samples:
        pass  # TODO Code d'evaluation de chaque dataframe
    metrics['datetime'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    metrics['auc'] = 0.99
    return metrics


@click.command(short_help='Evaluate the model')
@click.argument('model_filepath', metavar='<model>', type=click_pathlib.Path(exists=True))
@click.argument('sample_files', metavar='<selected files>', type=Glob(default_suffix="**/*.csv"))
@click.argument('evaluate_filepath', metavar='<evaluate>', type=click_pathlib.Path())
def main(model_filepath: Path,
         sample_files: Sequence[Path],
         evaluate_filepath: Path) -> int:
    """ Evaluate the <model> with <selected files> and save result in <evaluate>.
    """

    model = pickle.load(open(model_filepath, 'rb'))

    datasets = [pd.read_csv(f) for f in sample_files]
    metrics = evaluate_model(model, iter(datasets))
    with open(evaluate_filepath, 'wt') as evaluate_file:
        json.dump(metrics, evaluate_file, indent=4)
    return 0


if __name__ == '__main__':
    init_logger(LOGGER, logging.INFO)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    if not getattr(sys, 'frozen') and hasattr(sys, '_MEIPASS'):
        dotenv.load_dotenv(dotenv.find_dotenv())

    sys.exit(main())  # pylint: disable=E1120

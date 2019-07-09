# -*- coding: utf-8 -*-
"""
    Treatment in charge of training visualize the results.
"""
import json
import logging
import os
import sys
from typing import Sequence, IO

import click
import dotenv

from tools.tools import Glob, init_logger

LOGGER = logging.getLogger(__name__)


def visualize(streams: Sequence[IO[str]]) -> None:
    """ Visualize the results

        :param streams list of files
        :return: 0 if ok, else error
    """
    for stream in streams:
        # TODO: Ajoutez le code de visualisation de l'évalusation ici
        metric = json.load(stream)
        print("date,                 auc")
        print(metric["datetime"], ",", metric["auc"])


@click.command(help="Visualize the results")
@click.argument('evaluate_filepath', type=Glob(recursive=True))
def main(evaluate_filepath: Sequence[str]) -> int:
    """ Visualize the results

        :param evaluate_filepath: glob data file path
        :return: 0 if ok, else error
    """
    LOGGER.info('Visualize the results')

    inputs = [open(a_file, "rt")
              for a_file in evaluate_filepath
              if not os.path.isdir(a_file)]
    visualize(inputs)
    return 0


if __name__ == '__main__':
    init_logger(LOGGER, logging.INFO)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    dotenv.load_dotenv(dotenv.find_dotenv())

    sys.exit(main())  # pylint: disable=E1120

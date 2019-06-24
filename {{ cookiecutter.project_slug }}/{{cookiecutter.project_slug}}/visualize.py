# -*- coding: utf-8 -*-
"""
    Treatment in charge of training visualize the results.
"""
import glob
import json
import logging
import os
import sys
from typing import Sequence, IO

import click
import dotenv

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


@click.command()
@click.argument('evaluate_filepath', type=str)
def main(evaluate_filepath: str) -> int:
    """ Visualize the results

        :param evaluate_filepath: glob data file path
        :return: 0 if ok, else error
    """
    LOGGER.info('Visualize the results')

    if (evaluate_filepath.find("*") == -1):
        evaluate_filepath += "*"
    inputs: Sequence[IO[str]] = \
        [open(a_file, "r")
         for a_file in glob.glob(evaluate_filepath, recursive=True)
         if not os.path.isdir(a_file)]
    visualize(inputs)
    return 0


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    dotenv.load_dotenv(dotenv.find_dotenv())

    sys.exit(main())  # pylint: disable=E1120

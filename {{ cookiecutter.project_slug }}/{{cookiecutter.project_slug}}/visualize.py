# -*- coding: utf-8 -*-
"""
    Traitement en charge de visualiser l'évolution du modèle.
"""
import glob
import logging
import sys
from typing import List

import click
import dotenv

LOGGER = logging.getLogger(__name__)


def visualize(files: List[str]) -> None:
    """ Visualize the results

        :param list of files
        :return: 0 if ok, else error
    """
    for a_file in files:
        pass  # TODO: Ajoutez le code de visualisation ici


@click.command()
@click.argument('evaluate_filepath', type=click.Path(exists=True))
def main(evaluate_filepath: str) -> None:
    """ Visualize the results

        :param evaluate_filepath: glob data file path
        :return: 0 if ok, else error
    """
    LOGGER.info('Visualize the results')

    inputs = [str(a_file)
              for a_file in glob.glob(evaluate_filepath, recursive=True)]
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

# -*- coding: utf-8 -*-
"""
    Traitement en charge de visualiser l'évolution du modèle.
"""

import pathlib
import logging
import sys

import click
import dotenv


def visualize(evaluate_filepath: str) -> None:
    """ Predict with using the model from model_filepath and data
        from data_filepath

        :param evaluate_filepath: data file path
        :return: 0 if ok, else error
    """
    # TODO: Add your code here
    return 0


@click.command()
@click.argument('evaluate_filepath', type=click.Path(exists=True))
def main(evaluate_filepath: str) -> None:
    """ Predict with using the model from model_filepath and data
        from data_filepath

        :param evaluate_filepath: data file path
        :return: 0 if ok, else error
    """
    logger = logging.getLogger(__name__)
    logger.info('Visualize the results')
    return visualize(evaluate_filepath)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # not used in this stub but often useful for finding various files
    PROJECT_DIR = pathlib.Path(__file__).resolve().parents[1]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    dotenv.load_dotenv(dotenv.find_dotenv())

    sys.exit(main())  # pylint: disable=E1120

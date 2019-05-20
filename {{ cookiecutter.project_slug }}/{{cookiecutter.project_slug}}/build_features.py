# -*- coding: utf-8 -*-
"""
    Traitement en charge d'ajouter des features aux données brutes.
"""
# pylint: disable-msg=R0801

import os
import pathlib
import logging
import shutil
import sys

import click
import dotenv

from .tools import *  # pylint: disable=W0401

logger = logging.getLogger(__name__)


def build_features(input_prepared_filepath: str, output_featured_filepath: str) -> int:
    pathlib.Path(os.path.dirname(output_featured_filepath)) \
        .mkdir(parents=True, exist_ok=True)
    # TODO: Remplacez la ligne suivante pour un enrichissement du dataset
    shutil.copyfile(input_prepared_filepath, output_featured_filepath)
    return 0


@click.command()
@click.argument('input_prepared_filepath', type=click.Path(exists=True))
@click.argument('output_featured_filepath', type=click.Path())
def main(input_prepared_filepath: str, output_featured_filepath: str) -> int:
    """ Runs data processing scripts to turn raw data from (../interim) into
        extended data (saved in ../processed).

        :param input_prepared_filepath: input prepared file path
        :param output_featured_filepath: output file path with features
        :return: 0 if ok, else error
    """
    logger.info('add features from prepared data')
    return build_features(input_prepared_filepath, output_featured_filepath)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # not used in this stub but often useful for finding various files
    PROJECT_DIR = pathlib.Path(__file__).resolve().parents[1]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    dotenv.load_dotenv(dotenv.find_dotenv())

    sys.exit(main())  # pylint: disable=E1120

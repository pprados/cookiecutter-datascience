# -*- coding: utf-8 -*-
"""
    Treatment in charge of adding features.
"""
# pylint: disable-msg=R0801

import logging
import sys
from pathlib import Path

import click
import dotenv
import pandas as pd

from tools.tools import init_logger

LOGGER = logging.getLogger(__name__)


def build_features(input_prepared: pd.DataFrame) -> pd.DataFrame:
    """ Add features to turn input_prepared data into
        data with new features.

        :param input_prepared: data prepared
        :return: data with features
    """
    # TODO: Remplacez la ligne suivante pour un enrichissement du dataset
    output_feature = input_prepared
    return output_feature


@click.command(help="Add features")
@click.argument('input_prepared_filepath', type=click_pathlib.Path(exists=True))
@click.argument('output_featured_filepath', type=click_pathlib.Path())
def main(input_prepared_filepath: Path,
         output_featured_filepath: Path) -> int:
    """ Runs data processing scripts to turn add features from raw data
        into data with features.

        :param input_prepared_filepath: input prepared file path
        :param output_featured_filepath: output file path with features
        :return: 0 if ok, else error
    """
    LOGGER.info('Add features from prepared data')

    output_featured_filepath.dirname().mkdir(parents=True, exist_ok=True)

    input_prepared = pd.read_csv(input_prepared_filepath)
    output_feature = build_features(input_prepared)
    output_feature.to_csv(output_featured_filepath)
    return 0


if __name__ == '__main__':
    init_logger(LOGGER, logging.INFO)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    dotenv.load_dotenv(dotenv.find_dotenv())

    sys.exit(main())  # pylint: disable=E1120

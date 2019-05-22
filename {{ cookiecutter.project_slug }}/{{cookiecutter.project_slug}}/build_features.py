# -*- coding: utf-8 -*-
"""
    Treatment in charge of adding features.
"""
# pylint: disable-msg=R0801

import logging
import os
import pathlib
import sys

import click
import dotenv
import pandas as pd

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


@click.command()
@click.argument('input_prepared_filepath', type=click.Path(exists=True))
@click.argument('output_featured_filepath', type=click.Path())
def main(input_prepared_filepath: str,
         output_featured_filepath: str) -> int:
    """ Runs data processing scripts to turn add features from raw data
        into data with features.

        :param input_prepared_filepath: input prepared file path
        :param output_featured_filepath: output file path with features
        :return: 0 if ok, else error
    """
    LOGGER.info('add features from prepared data')

    pathlib.Path(os.path.dirname(output_featured_filepath)) \
        .mkdir(parents=True, exist_ok=True)

    input_prepared = pd.read_csv(input_prepared_filepath)
    output_feature = build_features(input_prepared)
    output_feature.to_csv(output_featured_filepath)
    return 0


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    dotenv.load_dotenv(dotenv.find_dotenv())

    sys.exit(main())  # pylint: disable=E1120

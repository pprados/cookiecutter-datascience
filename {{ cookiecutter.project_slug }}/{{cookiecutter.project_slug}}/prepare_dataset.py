# -*- coding: utf-8 -*-
"""
    Traitement en charge de préparer le dataset
    (changement de format, nettoyage, etc).
"""

import logging
import os
import pathlib
import sys

import click
import dotenv
import pandas as pd

LOGGER = logging.getLogger(__name__)


def prepare_dataset(input_raw: pd.DataFrame) -> pd.DataFrame:
    """ Runs data processing scripts to turn raw data from (../interim) into
        extended data (saved in ../processed).

        :param input_raw: input raw dataframe
        :return: output_prepared dataframe
    """
    # TODO: Remplacez la ligne suivante pour un enrichissement du dataset
    output_prepared = input_raw
    return output_prepared


@click.command()
@click.argument('input_raw_filepath', type=click.Path(exists=True))
@click.argument('output_interim_filepath', type=click.Path())
def main(input_raw_filepath: str,
         output_prepared_filepath: str) -> int:
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed and extended with
        features (saved in ../interim).

        :param input_raw_filepath: data file path
        :param output_prepared_filepath: new file to write with prepared datas
        :return: 0 if ok, else error
    """
    LOGGER.info('Clean data set from raw data to interim')

    pathlib.Path(os.path.dirname(output_prepared_filepath)) \
        .mkdir(parents=True, exist_ok=True)

    input_raw = pd.read_csv(input_raw_filepath)
    output_prepared = prepare_dataset(input_raw)
    output_prepared.to_csv(output_prepared_filepath)
    return 0


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    dotenv.load_dotenv(dotenv.find_dotenv())

    sys.exit(main())  # pylint: disable=E1120

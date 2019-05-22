# -*- coding: utf-8 -*-
"""
    Treatment in charge of preparing the dataset.
    (change format, cleaning, etc).
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
    """ Process to turn raw data into prepared data.

        :param input_raw: Input raw dataframe
        :return: Prepared dataframe
    """
    # TODO: Remplacez la ligne suivante pour un enrichissement du dataset
    output_prepared = input_raw
    return output_prepared


@click.command()
@click.argument('input_raw_filepath', type=click.Path(exists=True))
@click.argument('output_prepared_filepath', type=click.Path())
def main(input_raw_filepath: str,
         output_prepared_filepath: str) -> int:
    """ Process to turn raw data file into prepared data file.

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

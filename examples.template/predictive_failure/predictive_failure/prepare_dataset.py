# -*- coding: utf-8 -*-
"""
    Treatment in charge of preparing the dataset.
    (change format, cleaning, etc).
"""

import logging
import sys
from pathlib import Path

import click
import click_pathlib
import dotenv
import pandas as pd

from .tools.tools import init_logger

LOGGER = logging.getLogger(__name__)


def prepare_dataset(input_raw: pd.DataFrame) -> pd.DataFrame:
    """ Process to turn raw data into prepared data.

        :param input_raw: Input raw dataframe
        :return: Prepared dataframe
    """
    LOGGER.info('Prepare data set from raw data')

    # TODO: Remplacez la ligne suivante pour un enrichissement du dataset
    output_prepared = input_raw
    return output_prepared


@click.command(short_help="Prepare the dataset.")
@click.argument('input_raw_filepath', metavar='<selected files>',type=click_pathlib.Path(exists=True))
@click.argument('output_prepared_filepath', metavar='<output>', type=click_pathlib.Path())
def main(input_raw_filepath: Path,
         output_prepared_filepath: Path) -> int:
    """
    Prepare the <selected files> and save in <output>.
    """

    output_prepared_filepath.parent.mkdir(parents=True, exist_ok=True)

    input_raw = pd.read_csv(input_raw_filepath)
    output_prepared = prepare_dataset(input_raw)
    output_prepared.to_csv(output_prepared_filepath)
    return 0


if __name__ == '__main__':
    init_logger(LOGGER, logging.INFO)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    dotenv.load_dotenv(dotenv.find_dotenv())

    sys.exit(main())  # pylint: disable=E1120

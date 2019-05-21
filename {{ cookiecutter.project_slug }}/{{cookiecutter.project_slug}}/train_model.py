# -*- coding: utf-8 -*-
"""
    Traitement en charge de l'apprentissage du modèle.
"""
import glob
import logging
import os
import pathlib
import pickle
import sys
from typing import List, Any

import click
import dotenv

LOGGER = logging.getLogger(__name__)


def train_model(inputs: List[str],
                epoch: int,
                batch_size: int) -> Any:
    """ Train the model from input_filepath and save it in ../models

        :param inputs: list of file to train the model
        :param epoch: Value of epoch (default 128)
        :param batch_size: Value of batch size (default 1024)
        :return: The trained model
    """
    # TODO: Remplacez la ligne suivante par un apprentissage
    model = "TODO"

    return model


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('model_filepath', type=click.Path())
# hyperparameters sent by the client are passed as
# command-line arguments to the script.
@click.option('--epoch', default=128, type=int, help='Epoch')
@click.option('--batch-size', default=1024, type=int, help='Batch size')
def main(input_filepath: str,
         model_filepath: str,
         epoch: int,
         batch_size: int) -> int:
    """ Train the model from input_filepath and save it in ../models

        :param input_filepath: glob data file path
        :param model_filepath: file to write the model
        :param epoch: Value of epoch (default 128)
        :param batch_size: Value of batch size (default 1024)
        :return: 0 if ok, else error
    """
    LOGGER.info('train model from processed and featured data')

    pathlib.Path(os.path.dirname(model_filepath)) \
        .mkdir(parents=True, exist_ok=True)
    inputs = [f for f in glob.glob(input_filepath, recursive=True)]
    model = train_model(inputs, epoch, batch_size)
    pickle.dump(model, open(model_filepath, 'wb'))
    return 0


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    dotenv.load_dotenv(dotenv.find_dotenv())

    sys.exit(main())  # pylint: disable=E1120

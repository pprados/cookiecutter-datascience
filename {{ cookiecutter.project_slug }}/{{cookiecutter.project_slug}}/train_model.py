# -*- coding: utf-8 -*-
"""
    Treatment in charge of training the model.
"""
import logging
import pickle
import sys
from pathlib import Path
from typing import Any, Sequence, Optional

import click
import click_pathlib
import dotenv
{% if cookiecutter.use_tensorflow == 'y' %}import keras{% endif %}
from tools.tools import Glob, init_logger

LOGGER = logging.getLogger(__name__)

{% if cookiecutter.use_tensorflow == 'n' %}Model = keras.Model{% else %}Model = Any  # TODO: Select type{% endif %}

def train_model(inputs: Sequence[str],
                epoch: int = 128,
                batch_size: int = 1024,
                seed:Optional[int] = None) -> Model:
    """ Train the model from inputs

        :param inputs: list of datasets to train the model
        :param epoch: Value of epoch (default 128)
        :param batch_size: Value of batch size (default 1024)
        :param seed: Force seed (default None)
        :return: The trained model
    """
    # TODO: Remplacez la ligne suivante par un apprentissage
    model = "TODO"

    return model


@click.command(help="Trains model.")
@click.argument('input_files', type=Glob(default_suffix="**/*.csv"))
@click.argument('model_filepath', type=click_pathlib.Path())
# Hyper parameters
@click.option('--epoch', default=128, type=int, help='Epoch')
@click.option('--batch-size', default=1024, type=int, help='Batch size')
@click.option('--seed',  type=int, help='Batch size', default=None)
def main(input_files: Sequence[Path],
         model_filepath: Path,
         epoch: int,
         batch_size: int,
         seed: Optional[int]) -> int:
    """ Train the model from input_filepath and save it in model_filepath

        :param input_filepath: glob data file path
        :param model_filepath: file to write the model
        :param epoch: Value of epoch (default 128)
        :param batch_size: Value of batch size (default 1024)
        :param seed: The initial seed (default None)
        :return: 0 if ok, else error
    """
    LOGGER.info('Train model from processed and featured data')

    model_filepath.dirname().mkdir(parents=True, exist_ok=True)

    model: Model = train_model(input_files, epoch, batch_size, seed)
    pickle.dump(model, open(model_filepath, 'wb'))
    return 0


if __name__ == '__main__':
    init_logger(LOGGER, logging.INFO)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    dotenv.load_dotenv(dotenv.find_dotenv())

    sys.exit(main())  # pylint: disable=E1120

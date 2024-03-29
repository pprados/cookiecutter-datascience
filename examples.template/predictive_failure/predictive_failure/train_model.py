# -*- coding: utf-8 -*-
"""
    Treatment in charge of training the model.
"""
import logging
import pickle
import sys
from pathlib import Path
from typing import Any, Sequence, Optional, Iterator

import click
import click_pathlib
import dotenv

from .tools.tools import Model, Glob, init_logger

LOGGER = logging.getLogger(__name__)


def train_model(inputs: Sequence[Path],
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
    LOGGER.info('Train model from processed and featured data')

    # TODO: Remplacez la ligne suivante par un apprentissage
    model = "TODO"

    return model

# Les paramètres ci-dessous permettent d'avoir une possibilité d'invoquer
# la méthode `train_model` à partir de la ligne de commande, en utilisant des fichiers.
# Vous pouvez invoquer `python -m predictive_failure.train_model --help`
# pour consulter l'aide générée.
# Tous les méta-paramètres doivent être valorisable en paramètre
# afin de permettre l'optimisation des méta-paramètres via différents outils.
@click.command(short_help="Trains model.")
@click.argument('input_files', metavar='<selected files>', type=Glob(default_suffix="**/*.csv"))
@click.argument('model_filepath', metavar='<model>', type=click_pathlib.Path())
# Hyper parameters
@click.option('--epoch', default=128, type=int, help='Epoch')
@click.option('--batch-size', default=1024, type=int, help='Batch size')
@click.option('--seed',  type=int, help='Fixed seed', default=None)
def main(input_files: Sequence[Path],
         model_filepath: Path,
         epoch: int,
         batch_size: int,
         seed: Optional[int],
        ) -> int:
    """
    Train the <model> from <selected files>
    """
    model_filepath.parent.mkdir(parents=True, exist_ok=True)

    model = train_model(input_files, epoch, batch_size, seed)
    pickle.dump(model, open(model_filepath, 'wb'))
    return 0


if __name__ == '__main__':
    init_logger(LOGGER, logging.INFO)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    if not getattr(sys, 'frozen') and hasattr(sys, '_MEIPASS'):
        dotenv.load_dotenv(dotenv.find_dotenv())

    sys.exit(main(standalone_mode=False))  # pylint: disable=no-value-for-parameter,unexpected-keyword-arg

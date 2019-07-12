# -*- coding: utf-8 -*-
"""
    All in memory. Reduce the cost in cloud.
"""
import json
import logging
import sys
import tarfile
from pathlib import Path
from typing import Tuple, Iterator, Optional

import click
import click_pathlib
import dotenv

from flower_classifier.evaluate_model import evaluate_model
from flower_classifier.prepare_dataset import prepare_dataset
from flower_classifier.tools.tools import init_logger, caculate_domains_from_tar, save_model_and_domain, \
    generator_itemgetter
from flower_classifier.train_model import train_model

LOGGER = logging.getLogger(__name__)


@click.command("Train the model from raw")
@click.argument('input_raw_filepath', metavar='<tgz file>', type=click_pathlib.Path(exists=True, file_okay=True))
@click.argument('model_filepath', metavar='<model>', type=click_pathlib.Path(file_okay=True))
@click.argument('domain_filepath', metavar='<domain>', type=click_pathlib.Path(dir_okay=True))
# Hyper parameters
@click.option("--epochs", type=click.INT, default=1, help="Maximum number of epochs to evaluate.")
@click.option("--batch-size", type=click.INT, default=1,
              help="Batch size passed to the learning algo.")
@click.option("--image-width", type=click.INT, default=224, help="Input image width in pixels.")
@click.option("--image-height", type=click.INT, default=224, help="Input image height in pixels.")
@click.option("--test-ratio", type=click.FLOAT, default=0.2)
@click.option("--seed", type=click.INT, help="Seed for the random generator.")
@click.option('--logdir', type=click_pathlib.Path(), help='Tensorflow logdir', default="./logdir/")
def main(input_raw_filepath: Path,
         model_filepath: Path,
         domain_filepath: Path,
         test_ratio: float,
         epochs: int,
         batch_size: int,
         image_width: int,
         image_height: int,
         seed: Optional[int],
         logdir: Path) -> int:
    """
    Trains the model from <tgz file>, and save <model> and <domain>
    """
    LOGGER.info("Train the model from %s", input_raw_filepath)

    dim = (image_width, image_height)
    model_filepath.parent.mkdir(parents=True, exist_ok=True)

    def extract_tgz(tgz_filepath: Path) -> Iterator[Tuple[Path, tarfile.ExFileObject]]:
        with tarfile.open(tgz_filepath) as tar:
            # Open tgz
            for tarf in tar:
                if tarf.isfile() and tarf.name.endswith('.jpg'):
                    path = Path(tarf.name)
                    path = path.relative_to(*path.parts[:1])
                    yield (path, tar.extractfile(tarf))

    # 1. load and train the model simultaneously
    labels, domain = caculate_domains_from_tar(input_raw_filepath)
    image_datas = generator_itemgetter(1, prepare_dataset(extract_tgz(input_raw_filepath), dim))
    model = train_model(domain,
                        labels,
                        image_datas,
                        test_ratio,
                        epochs,
                        batch_size,
                        dim,
                        seed,
                        logdir)


    # 3. Save the model and metrics
    save_model_and_domain(model_filepath, model,
                          domain_filepath, domain)

    return 0


if __name__ == '__main__':
    init_logger(LOGGER, logging.INFO)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    dotenv.load_dotenv(dotenv.find_dotenv())

    sys.exit(main())  # pylint: disable=E1120

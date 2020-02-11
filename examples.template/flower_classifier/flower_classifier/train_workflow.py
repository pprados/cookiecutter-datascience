# -*- coding: utf-8 -*-
"""
    All in memory. Reduce the cost in cloud.
"""
import logging
import sys
import tarfile
from pathlib import Path
from typing import Iterable, Optional, Tuple, IO

import click
import click_pathlib
import dotenv

from flower_classifier.prepare_dataset import prepare_dataset
from flower_classifier.tools import DEFAULT_BATCH_SIZE, DEFAULT_IMAGE_SIZE, DEFAULT_TEST_RATIO
from flower_classifier.tools.tools import caculate_labels_and_domains_from_paths, save_model_and_domain, init_logger, \
    tar_paths
from flower_classifier.train_model import train_model

LOGGER = logging.getLogger(__name__)


@click.command("Train the model from raw")
@click.argument('input_raw_filepath', metavar='<tgz file>', type=click_pathlib.Path(exists=True, file_okay=True))
@click.argument('model_filepath', metavar='<model>', type=click_pathlib.Path(file_okay=True))
@click.argument('domain_filepath', metavar='<domain>', type=click_pathlib.Path(dir_okay=True))
# Hyper parameters
@click.option("--epochs", type=click.INT, default=1, help="Maximum number of epochs to evaluate.")
@click.option("--batch-size", type=click.INT, default=DEFAULT_BATCH_SIZE,
              help="Batch size passed to the learning algo.")
@click.option("--image-width", type=click.INT, default=DEFAULT_IMAGE_SIZE, help="Input image width in pixels.")
@click.option("--image-height", type=click.INT, default=DEFAULT_IMAGE_SIZE, help="Input image height in pixels.")
@click.option("--test-ratio", type=click.FLOAT, default=DEFAULT_TEST_RATIO)
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

    def extract_tgz(tgz_filepath: Path) -> Iterable[Tuple[Path, IO[bytes]]]:
        with tarfile.open(tgz_filepath) as tar:
            # Open tgz
            for tarf in tar:
                if tarf.isfile() and tarf.name.endswith('.jpg'):
                    path = Path(tarf.name)
                    path = path.relative_to(*path.parts[:1])
                    yield (path, tar.extractfile(tarf))

    # 1. load and train the model simultaneously, with cascade of generators
    labels, domain = caculate_labels_and_domains_from_paths(tar_paths(input_raw_filepath))
    image_datas = (x[1] for x in prepare_dataset(extract_tgz(input_raw_filepath), dim))
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
    if not getattr(sys, 'frozen') and hasattr(sys, '_MEIPASS'):
        dotenv.load_dotenv(dotenv.find_dotenv())

    sys.exit(main(standalone_mode=False))  # pylint: disable=no-value-for-parameter,unexpected-keyword-arg

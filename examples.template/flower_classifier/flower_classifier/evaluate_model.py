# -*- coding: utf-8 -*-
"""
    Treatment in charge of evaluate model
"""
import json
import logging
import pickle
import sys
from pathlib import Path
from time import strftime, gmtime
from typing import Iterable, Any, Sequence, Optional, Mapping, Tuple, List

import click
import click_pathlib
import dotenv
import tensorflow as tf
from PIL import Image
from keras.models import load_model
from sklearn.model_selection import train_test_split
import numpy as np

from flower_classifier.tools.tools import normalize_image, Glob, init_logger, Model

LOGGER = logging.getLogger(__name__)


def evaluate_model(model: Model,
                   domain: Mapping[str, int],  # PPR: TODO
                   image_datas: Iterable[np.ndarray],
                   labels: Sequence[int],
                   test_ratio: float = 1,
                   seed: Optional[int] = None) -> Mapping[str, Any]:
    """ Evaluate the model with sample datas

        Must be called in Tensorflow session.

        :param model: model
        :param domain: Dictionay with domain name and ids
        :param image_datas: A sequences of jpeg image in memory
        :param labels: The labels associates with each image
        :param labels: The labels associates with each image
        :param test_ratio: The test ration from image_datas
        :param seed: The specified seed or None
        :return: dictionary with metrics
    """

    x = np.array(image_datas)
    y = np.array(labels)

    if test_ratio != 1:
        _, x_test, _, y_test = \
            train_test_split(x, y,
                             random_state=seed,
                             train_size=1 - test_ratio)
    else:
        x_test = x
        y_test = y

    del x, y
    # pred = model.predict_classes(x_valid[:10])
    #
    # for i in range(len(pred)):
    #     print(pred[i], '==>', y_valid[i])

    scores = model.evaluate(x_test, y_test,
                            verbose=LOGGER.isEnabledFor(logging.INFO))

    metrics = {'datetime': strftime("%Y-%m-%d %H:%M:%S", gmtime())}
    for i, name in enumerate(model.metrics_names):
        LOGGER.info("%s:%3.2f", name, scores[i] * 100.0)
        metrics[name] = scores[i]
    return metrics


def _load_images(domain: Mapping[str, int], files: Iterable[Path]) -> \
        Tuple[List[int], List[np.array]]:
    """
    Load iterator and returns data and labels
    :param domain: The domain map
    :param files: Iterable of paths
    :return: sequence of labels, and sequence of image in np.array
    """
    labels: List[str] = []
    image_datas: List[np.array] = []
    for file in files:
        with Image.open(file) as image_file:
            clazz = Path(file).parts[-2:-1][0]
            if clazz in domain:
                labels.append(domain[clazz])
            else:
                LOGGER.warning("label '%s' not found in domain", clazz)
                labels.append(0)
            image = normalize_image(np.array(image_file, dtype=float))
            image_datas.append(image)
    return labels, image_datas


@click.command(short_help="Evaluate model")
@click.argument('input_files', metavar='<selected files>', type=Glob(default_suffix="**/*.jpg"))
@click.argument('model_filepath', metavar='<model>', type=click_pathlib.Path(exists=True, file_okay=True))
@click.argument('domain_filepath', metavar='<domain>', type=click_pathlib.Path(exists=True, file_okay=True))
@click.argument('evaluate_filepath', metavar='<evaluate>', type=click_pathlib.Path(file_okay=True))
@click.option("--test-ratio", type=click.FLOAT, default=1)
@click.option("--seed", type=click.INT, help="Seed for the random generator.")
def main(input_files: Sequence[Path],
         model_filepath: Path,
         domain_filepath: Path,
         evaluate_filepath: Path,
         test_ratio: float,
         seed: Optional[int]) -> int:
    """
    Apply <model> and <domain> with glob <selected files>, and save result in <evaluate>
    """
    LOGGER.info('Evaluate model \'%s\' with datas', model_filepath)

    with tf.Graph().as_default() as graph:  # pylint: disable=not-context-manager
        with tf.Session(graph=graph).as_default():  # pylint: disable=not-context-manager
            # 1. Load datas
            with open(str(domain_filepath), 'rb') as domain_file:
                domain = pickle.load(domain_file)
            labels, image_datas = _load_images(domain, input_files)
            model = load_model(str(model_filepath))

            # 2. Calculate metrics
            metrics = evaluate_model(model,
                                     domain,
                                     image_datas,
                                     labels,
                                     test_ratio,
                                     seed)

            # 3. Write results
            with open(str(evaluate_filepath), 'wt') as evaluate_file:
                json.dump(metrics, evaluate_file, indent=4)
    return 0


if __name__ == '__main__':
    init_logger(LOGGER, logging.INFO)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    if not getattr(sys, 'frozen') and hasattr(sys, '_MEIPASS'):
        dotenv.load_dotenv(dotenv.find_dotenv())

    sys.exit(main(standalone_mode=False))  # pylint: disable=no-value-for-parameter,unexpected-keyword-arg

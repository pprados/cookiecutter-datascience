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
from typing import Any, Mapping, Sequence, Iterator, Tuple

import click
import click_pathlib
import dotenv
import numpy as np
import tensorflow as tf
from keras.models import load_model
from keras.utils import np_utils

from flower_classifier.tools.tools import Glob, load_images, init_logger, Model

LOGGER = logging.getLogger(__name__)


def evaluate_model(model: Model,
                   domain: Mapping[str, int],
                   image_datas: Iterator[bytes],
                   labels: Sequence[int]) -> Mapping[str, Any]:
    """ Evaluate the model with sample datas

        Must be called in Tensorflow session.

        :param model: model
        :param image_datas: A sequences of jpeg image in memory
        :param labels: The labels associates with each image
        :param labels: The labels associates with each image
        :param image_width: Width of images
        :param image_height: Height of images
        :return: dictionary with metrics
    """

    images = np.array([datas for datas in image_datas])
    labels = np_utils.to_categorical(np.array(labels), num_classes=len(domain))

    scores = model.evaluate(images, labels,
                            verbose=LOGGER.isEnabledFor(logging.INFO))
    LOGGER.info("%s:%3.2f", (model.metrics_names[0], scores[0] * 100.0))
    LOGGER.info("%s:%3.2f", (model.metrics_names[1], scores[1] * 100.0))

    metrics = {}
    metrics['datetime'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    for i, name in enumerate(model.metrics_names):
        metrics[name] = scores[i]
    return metrics


@click.command(short_help="Evaluate model")
@click.argument('input_files', metavar='<selected files>', type=Glob(default_suffix="**/*.jpg"))
@click.argument('model_filepath', metavar='<model>', type=click_pathlib.Path(exists=True, file_okay=True))
@click.argument('domain_filepath', metavar='<domain>', type=click_pathlib.Path(exists=True, file_okay=True))
@click.argument('evaluate_filepath', metavar='<evaluate>', type=click_pathlib.Path(file_okay=True))
def main(input_files: Sequence[Path],
         model_filepath: Path,
         domain_filepath: Path,
         evaluate_filepath: Path) -> int:
    """ 
    Apply <model> and <domain> with glob <selected files>, and save result in <evaluate>
    """
    LOGGER.info('Evaluate model \'%s\' with datas', model_filepath)

    with tf.Graph().as_default() as graph:  # pylint: disable=E1129
        with tf.Session(graph=graph).as_default():  # pylint: disable=E1129
            # 1. Load datas
            labels, _, image_datas = load_images(iter(input_files))
            model = load_model(str(model_filepath))
            with open(domain_filepath, 'rb') as domain_file:
                domain = pickle.load(domain_file)

            # 2. Calculate metrics
            metrics = evaluate_model(model,
                                     domain,
                                     iter(image_datas),
                                     labels)

            # 3. Write results
            with open(evaluate_filepath, 'wt') as evaluate_file:
                json.dump(metrics, evaluate_file, indent=4)
    return 0


if __name__ == '__main__':
    init_logger(LOGGER, logging.INFO)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    dotenv.load_dotenv(dotenv.find_dotenv())

    sys.exit(main())  # pylint: disable=E1120

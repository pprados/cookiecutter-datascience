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
from typing import Any, Mapping, Sequence

import click
import click_pathlib
import dotenv
import numpy as np
import tensorflow as tf
from keras.models import load_model
from keras.utils import np_utils

from flower_classifier.tools.tools import decode_and_resize_image, Glob, load_images, init_logger
from flower_classifier.train_model import Model

LOGGER = logging.getLogger(__name__)


def evaluate_model(model: Model,
                   domain: Mapping[str, int],
                   image_datas: Sequence[bytes],
                   labels: Sequence[int],
                   image_width: int = 224,
                   image_height: int = 224) -> Mapping[str, Any]:
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

    input_shape = (image_width, image_height, 3)
    dims = input_shape[:2]
    images = np.array([decode_and_resize_image(datas, dims) for datas in image_datas])
    labels = np_utils.to_categorical(np.array(labels), num_classes=len(domain))

    scores = model.evaluate(images, labels,
                            verbose=LOGGER.isEnabledFor(logging.INFO))
    LOGGER.info("%s", f"{model.metrics_names[1]}:{scores[1] * 100}")

    metrics = {}
    metrics['datetime'] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    for i, name in enumerate(model.metrics_names):
        metrics[name] = scores[i]
    return metrics


@click.command(help="Evaluate the model with a set of images"
                    "Parameters:"
                    "- The input is expected as a directory tree with pictures for each category in a"
                    " folder named by the category, or a glob path."
                    "- The trained model file path (.h5 extension)."
                    "- The extract domain file path (.pkl extension)")
@click.argument('input_files', type=Glob(default_suffix="**/*.jpg"))
@click.argument('model_filepath', type=click_pathlib.Path(exists=True, file_okay=True))
@click.argument('domain_filepath', type=click_pathlib.Path(exists=True, file_okay=True))
@click.argument('evaluate_filepath', type=click_pathlib.Path(file_okay=True))
@click.option("--image-width", type=click.INT, default=224, help="Input image width in pixels.")
@click.option("--image-height", type=click.INT, default=224, help="Input image height in pixels.")
def main(input_files: Sequence[Path],
         model_filepath: Path,
         domain_filepath: Path,
         evaluate_filepath: Path,
         image_width: int,
         image_height: int) -> int:
    """ Evaluate the model with samples
        :param input_filepath: glob data files path
        :param model_filepath: model file path
        :param evaluate_filepath: json file path with metrics to write
        :return: 0 if ok, else error
    """
    LOGGER.info('Evaluate model \'%s\' with datas', model_filepath)

    with tf.Graph().as_default() as graph:  # pylint: disable=E1129
        with tf.Session(graph=graph).as_default():  # pylint: disable=E1129
            # 1. Load datas
            labels, _, image_datas = load_images(input_files)
            model: Model = load_model(str(model_filepath))
            with open(domain_filepath, 'rb') as domain_file:
                domain: Mapping[str, int] = pickle.load(domain_file)

            # 2. Calculate metrics
            metrics: Mapping[str, Any] = evaluate_model(model, domain, image_datas, labels, image_width, image_height)

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

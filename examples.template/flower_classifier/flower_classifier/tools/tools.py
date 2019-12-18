# -*- coding: utf-8 -*-
"""
Example of a custom python function implementing image classifier with image preprocessing embedded
in the model.
"""
import glob
import logging
import os
import pickle
import tarfile
from pathlib import Path
from typing import Sequence, Tuple, Optional, List, Mapping, Iterator

import click
import keras
import numpy as np

Model = keras.Model

LOGGER = logging.getLogger(__name__)


def init_logger(logger: logging.Logger, level: int) -> None:
    """ Init logger

    :param logger The logger to initialize
    :param level The level
    """
    # See https://tinyurl.com/yynfczc8
    logging.getLogger().setLevel(level)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(console_handler)


class Glob(click.ParamType):
    """
    A Click path argument that returns a ``List[Path]`` via un glob syntax.
    """

    def __init__(self,
                 exists: bool = False,
                 recursive: bool = False,
                 default_suffix: str = "*"):
        self.exists = exists
        self.default_suffix = default_suffix
        self.recursive = recursive

    def convert(
            self,
            value: str,
            param: Optional[click.core.Parameter],
            ctx: Optional[click.core.Context],
    ) -> List[Path]:
        """
        Return a ``Path`` from the string ``click`` would have created with
        the given options.
        """
        if "*" not in value:
            value = os.path.join(value, self.default_suffix)
        return [Path(x) for x in
                glob.glob(super().convert(value=value, param=param, ctx=ctx), recursive=self.recursive)]


def caculate_labels_and_domains_from_paths(paths: Iterator[Path]) -> Tuple[Sequence[int], Mapping[str, int]]:
    """
    Calculate labels and domains from path name.
    :param paths: Iterator of Path.
    :return: Sequences of labels and detected domain.
    """
    labels: List[int] = []
    domain: Mapping[str, int] = {}
    for path in paths:
        if path.suffix == ".jpg":
            clazz = path.parts[-2:-1][0]
            if clazz not in domain:
                domain[clazz] = len(domain)
            labels.append(domain[clazz])
    return labels, domain


def normalize_image(image: np.array) -> np.array:
    """
    Normalise image range values.
    :param image: The image to transform
    :return: The image with right range values.
    """
    return np.array((image / 127.5) - 1)


def save_model_and_domain(model_filepath: Path,
                          model: Model,
                          domain_filepath: Path,
                          domain: Mapping[str, int]) -> None:
    """
    Save model and demains if files.
    :param model_filepath:  Model file name.
    :param model: The model to save.
    :param domain_filepath: Domain file name.
    :param domain: The domain
    """
    model.save(str(model_filepath))
    with open(str(domain_filepath), 'wb') as domain_file:
        pickle.dump(domain, domain_file)


def tar_paths(tar_filepath: Path) -> Iterator[Path]:
    """
    Return generator with Path of tar files"
    :param tar_filepath: Tar file name
    :return: Generator to yield path of each files in tar file.
    """
    return (Path(tarf.name) for tarf in tarfile.open(tar_filepath))

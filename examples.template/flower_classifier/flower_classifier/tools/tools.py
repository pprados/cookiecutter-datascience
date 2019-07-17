# -*- coding: utf-8 -*-
"""
Example of a custom python function implementing image classifier with image preprocessing embedded
in the model.
"""
import glob
import logging
import operator
import os
import pickle
import tarfile
from pathlib import Path
from typing import Sequence, Tuple, Optional, List, Mapping, Iterator, Generator, Any

import click
import keras
import numpy as np
from PIL import Image

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
    labels: Sequence[str] = []
    domain: Mapping[str, int] = {}
    for path in paths:
        if path.suffix == ".jpg":
            clazz = path.parts[-2:-1][0]
            if clazz not in domain:
                domain[clazz] = len(domain)
            labels.append(domain[clazz])
    return labels, domain


def normalize_image(image: np.array) -> np.array:
    return (image / 127.5) - 1



def save_model_and_domain(model_filepath: Path,
                          model: Model,
                          domain_filepath: Path,
                          domain: Mapping[str, int]) -> None:
    model.save(str(model_filepath))
    with open(domain_filepath, 'wb') as domain_file:
        pickle.dump(domain, domain_file)


def generator_itemgetter(k: Any, generator: Generator) -> Generator:
    """A generator to select specify key of the previous generator """
    for g in generator:
        yield g.__getitem__(k)


def tar_paths(tar_filepath: Path) -> Iterator[Path]:
    def tarIterator(tar):
        for tarf in tar:
            yield Path(tarf.name)

    return tarIterator(tarfile.open(tar_filepath))

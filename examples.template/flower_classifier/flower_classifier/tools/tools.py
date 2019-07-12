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


def caculate_domains_from_tar(tar_filepath: Path) -> Tuple[Sequence[int], Mapping[str, int]]:
    with tarfile.open(tar_filepath) as tar:
        labels: Sequence[str] = []
        domain: Mapping[str, int] = {}
        for tarf in tar:
            path = Path(tarf.name)
            if path.suffix == ".jpg":
                clazz = path.parts[-2:-1][0]
                if clazz not in domain:
                    domain[clazz] = len(domain)
                labels.append(domain[clazz])
        return labels, domain

# PPR: a virer ?
def load_images(files: Iterator[Path]) -> Tuple[Sequence[int], Mapping[str, int], Sequence[bytes]]:
    """
    Load directories and returns data and labels
    :param input_filepath: Glob path
    :return: (
    """
    labels: Sequence[str] = []
    domain: Mapping[str, int] = {}
    image_datas: Sequence[bytes] = []
    for file in files:
        with Image.open(file) as image_file:
            clazz = Path(file).parts[-2:-1][0]
            if clazz not in domain:
                domain[clazz] = len(domain)
            labels.append(domain[clazz])
            image = (np.array(image_file, dtype=float) / 127.5) - 1
            image_datas.append(image)
    return labels, domain, image_datas


def save_model_and_domain(model_filepath: Path, 
                          model: Model, 
                          domain_filepath: Path,
                          domain: Mapping[str, int]) -> None:
    model.save(str(model_filepath))
    with open(domain_filepath, 'wb') as domain_file:
        pickle.dump(domain, domain_file)

def generator_itemgetter(k:Any, generator:Generator) -> Generator:
    """A generator to select specify key of the previous generator """
    for g in generator:
        yield g.__getitem__(k)

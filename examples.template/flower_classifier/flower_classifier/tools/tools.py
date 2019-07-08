# -*- coding: utf-8 -*-
"""
Example of a custom python function implementing image classifier with image preprocessing embedded
in the model.
"""
import glob
import logging
import os
from io import BytesIO
from pathlib import Path
from typing import Sequence, Tuple, Optional, List, Mapping

import click
import numpy as np
from PIL import Image


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


def decode_and_resize_image(raw_bytes: bytes, size: Tuple[int, int]) -> np.ndarray:
    """
    Read, decode and resize raw image bytes (e.g. raw content of a jpeg file).

    :param raw_bytes: Image bits, e.g. jpeg image.
    :param size: requested output dimensions
    :return: Multidimensional numpy array representing the resized image.
    """
    data = np.array(Image.open(BytesIO(raw_bytes)).resize(size))
    info = np.iinfo(data.dtype)  # Get the information of the incoming image type
    return np.asarray(data.astype(np.float32) / info.max)  # normalize the data to 0 - 1


def load_images(files: Sequence[Path]) -> Tuple[Sequence[int], Mapping[str, int], Sequence[bytes]]:
    """
    Load directories and returns data and labels
    :param input_filepath: Glob path
    :return: (
    """
    labels: Sequence[str] = []
    domain: Mapping[str, int] = {}
    image_datas: Sequence[bytes] = []
    for file in files:
        with open(file, "rb") as image_file:
            clazz = Path(file).parts[-2:-1][0]
            if clazz not in domain:
                domain[clazz] = len(domain)
            labels.append(domain[clazz])
            image_datas.append(image_file.read())
    return labels, domain, image_datas

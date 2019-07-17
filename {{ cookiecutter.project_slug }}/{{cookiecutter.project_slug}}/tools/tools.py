# -*- coding: utf-8 -*-
"""
Tools for machine learning pipeline.
"""
import glob
import logging
import os
from typing import Optional, List, Any
from pathlib import Path

import click

{% if cookiecutter.use_tensorflow == 'y' %}Model = keras.Model{% else %}Model = Any  # TODO: Select type{% endif %}

def init_logger(logger: logging.Logger, level:int) -> None:
    """ Init logger

    :param logger The logger to initialize
    :param level The level
    """
    # See https://stackoverflow.com/questions/20240464/python-logging-file-is-not-working-when-using-logging-basicconfig
    logging.getLogger().setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(ch)

class Glob(click.ParamType):
    def __init__(self, exists=False, recursive=False, default_suffix="*"):
        self.exists = exists
        self.default_suffix = default_suffix
        self.recursive = recursive

    """
    A Click path argument that returns a ``List[str`` via un glob syntax, not a string.
    """

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
        if not "*" in value:
            value = os.path.join(value, self.default_suffix)
        return [Path(x) for x in
                glob.glob(super().convert(value=value, param=param, ctx=ctx), recursive=self.recursive)]


# TODO: Ajoutez le code communs ici

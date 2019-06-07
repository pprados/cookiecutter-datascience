# -*- coding: utf-8 -*-
"""
    Test.
"""
import unittest

import pandas as pd
from typing import List, Any

import pytest

from bda_project.build_features import build_features
from bda_project.evaluate_model import evaluate_model
from bda_project.prepare_dataset import prepare_dataset
from bda_project.train_model import train_model


@pytest.mark.functional
class TestFunctional(unittest.TestCase):
    """ Functional test of pipeline.
    """

    def test_all_pipeline_with_none(self):  # pylint: disable=R0201
        """ Test prepare_dataset() with no data.
        """
        # Given
        input_raw: pd.DataFrame = pd.DataFrame(
            data={1, 2, 3})
        train_inputs: List[pd.DataFrame] = []
        validate_files: List[str] = []

        # When
        train_inputs.append(build_features(prepare_dataset(input_raw=input_raw)))
        model: Any = train_model(inputs=train_inputs, epoch=1, batch_size=1)
        metrics = evaluate_model(model, validate_files)

        # Then
        self.assertGreater(metrics['auc'], 0.8)

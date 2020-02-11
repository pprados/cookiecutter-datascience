# -*- coding: utf-8 -*-
"""
    Test.
"""
import unittest
from typing import List, Any, Dict, Mapping

import pandas as pd
import pytest
from {{ cookiecutter.project_slug }}.build_features import build_features
from {{ cookiecutter.project_slug }}.evaluate_model import evaluate_model
from {{ cookiecutter.project_slug }}.prepare_dataset import prepare_dataset
from {{ cookiecutter.project_slug }}.train_model import train_model


Model = Any  # TODO: Select type

# @pytest.mark.skip(reason="no way of currently testing this")
@pytest.mark.functional
class TestFunctional(unittest.TestCase):
    """ Functional test of pipeline.
    """

    def test_all_pipeline_with_none(self) -> None:  # pylint: disable=no-self-use
        """ Test prepare_dataset() with no data.
        """
        # Given
        input_raw: pd.DataFrame = pd.DataFrame(
            data={1, 2, 3})
        train_inputs: List[pd.DataFrame] = []
        validate_files: List[str] = []

        # When
        train_inputs.append(build_features(prepare_dataset(input_raw=input_raw)))
        model: Model = train_model(inputs=train_inputs,
                                 epochs=1,
                                 batch_size=1)
        metrics: Mapping[str,Any] = evaluate_model(model, validate_files)

        # Then
        self.assertGreater(metrics['auc'], 0.8)

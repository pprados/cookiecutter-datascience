# -*- coding: utf-8 -*-
"""
    Test.
"""
import unittest
from typing import List, Any, Mapping

import pandas as pd
from predictive_failure.evaluate_model import evaluate_model

Model = Any  # TODO: Select type

class TestEvaluateModel(unittest.TestCase):
    """ Unit test of prepare_dataset.
    """

    def test_evaluate_model_with_empty_list(self) -> None:  # pylint: disable=no-self-use
        """ Test train_model() with no data.
        """
        # Given
        model: Model = "TODO"
        validate_files: List[pd.DataFrame] = []

        # When
        metrics: Mapping[str,Any] = evaluate_model(model=model, samples=validate_files)

        # Then
        self.assertGreater(metrics['auc'], 0.8)

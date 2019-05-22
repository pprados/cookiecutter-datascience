# -*- coding: utf-8 -*-
"""
    Test.
"""
import unittest
from typing import List, Any

import pandas as pd
from bda_project.evaluate_model import evaluate_model


class TestEvaluateModel(unittest.TestCase):
    """ Unit test of prepare_dataset.
    """

    def test_evaluate_model_with_empty_list(self):  # pylint: disable=R0201
        """ Test train_model() with no data.
        """
        # Given
        model: Any = "TODO"
        validate_files: List[pd.DataFrame] = []

        # When
        metrics = evaluate_model(model=model, samples=validate_files)

        # Then
        self.assertGreater(metrics['auc'], 0.8)

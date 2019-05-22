# -*- coding: utf-8 -*-
"""
    Test.
"""
import unittest

import pandas as pd
from typing import List, Any

from bda_project.train_model import train_model


class TestTrainModel(unittest.TestCase):
    """ Unit test of prepare_dataset.
    """

    def test_train_model_with_empty_list(self):  # pylint: disable=R0201
        """ Test train_model() with no data.
        """
        # Given
        train_inputs: List[pd.DataFrame] = []

        # When
        model: Any = train_model(inputs=train_inputs,
                                 epoch=1,
                                 batch_size=1)

        # Then
        self.assertIsNotNone(model)

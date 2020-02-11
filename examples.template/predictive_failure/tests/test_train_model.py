# -*- coding: utf-8 -*-
"""
    Test.
"""
import unittest
from typing import Any, List

import pandas as pd
import pytest
from predictive_failure.train_model import train_model

Model = Any  # TODO: Select type


class TestTrainModel(unittest.TestCase):
    """ Unit test of prepare_dataset.
    """

    @pytest.mark.slow
    @pytest.mark.gpu
    def test_train_model_with_empty_list(self) -> None:  # pylint: disable=no-self-use
        """ Test train_model() with no data.
        """
        # Given
        train_inputs: List[pd.DataFrame] = []

        # When
        model: Model = train_model(inputs=train_inputs,
                                 epoch=1,
                                 batch_size=1)

        # Then
        self.assertIsNotNone(model)

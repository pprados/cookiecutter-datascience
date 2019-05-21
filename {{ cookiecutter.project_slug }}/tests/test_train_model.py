# -*- coding: utf-8 -*-
"""
    Test.
"""
import unittest
from typing import List

from bda_project.train_model import train_model


class TestTrainModel(unittest.TestCase):
    """ Unit test of prepare_dataset.
    """

    def test_train_model_with_empty_list(self):  # pylint: disable=R0201
        """ Test train_model() with no data.
        """
        # Given
        inputs: List[str] = []

        # When
        model = train_model(inputs=inputs,
                            epoch=1,
                            batch_size=1)

        # Then
        self.assertIsNotNone(model)

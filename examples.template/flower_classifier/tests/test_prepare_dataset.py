# -*- coding: utf-8 -*-
"""
    Test.
"""
import os
import unittest
from pathlib import Path

from flower_classifier.prepare_dataset import prepare_dataset


class TestPrepareDataSet(unittest.TestCase):
    """ Unit test of evaluate_model.
    """

    def test_prepare_dataset_with_none(self) -> None:  # pylint: disable=no-self-use
        """ Test prepare_dataset() with no data.
        """
        # Given
        pseudo_generator = []

        # When
        prepared_data = prepare_dataset(opened_files=pseudo_generator)

        # Then
        self.assertIsNotNone(prepared_data)

    def test_prepare_dataset_with_data(self) -> None:
        """ Test prepare_dataset() with no data.
        """
        # Given
        pseudo_generator = [(Path("tests/sample.jpg"), open(os.path.join("tests", "sample.jpg"), "rb"))]

        # When
        prepared_data = list(prepare_dataset(opened_files=pseudo_generator))

        # Then
        self.assertIsNotNone(prepared_data)
        self.assertEqual(prepared_data[0][0], pseudo_generator[0][0])

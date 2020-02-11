# -*- coding: utf-8 -*-
"""
    Test.
"""
import unittest
from typing import List

from predictive_failure.visualize import visualize


class TestVisualize(unittest.TestCase):
    """ Unit test of prepare_dataset.
    """

    def test_visualize_with_empty_list(self) -> None:  # pylint: disable=no-self-use
        """ Test train_model() with no data.
        """
        # Given
        files: List[str] = []

        # When
        visualize(files)

        # Then

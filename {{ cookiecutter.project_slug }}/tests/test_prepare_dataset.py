# -*- coding: utf-8 -*-
"""
    Test.
"""
import unittest

import pandas as pd
from bda_project.prepare_dataset import prepare_dataset


class TestPrepareDataSet(unittest.TestCase):
    """ Unit test of evaluate_model.
    """

    def test_prepare_dataset_with_none(self) -> None:  # pylint: disable=R0201
        """ Test prepare_dataset() with no data.
        """
        # Given
        input_raw: pd.DataFrame = pd.DataFrame(
            data={1, 2, 3})

        # When
        prepared_data: pd.DataFrame = prepare_dataset(input_raw=input_raw)

        # Then
        self.assertIsNotNone(prepared_data)

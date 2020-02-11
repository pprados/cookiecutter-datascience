# -*- coding: utf-8 -*-
"""
    Test.
"""
import unittest

import pandas as pd

from {{ cookiecutter.project_slug }}.build_features import build_features


class TestBuildFeatures(unittest.TestCase):
    """ Unit test of prepare_dataset.
    """

    def test_build_features_with_none(self) -> None:  # pylint: disable=no-self-use
        """ Test build_features() with no data.
        """
        # Given
        input_prepared: pd.DataFrame = pd.DataFrame(
            data={1, 2, 3})

        # When
        output_feature = build_features(input_prepared)

        # Then
        self.assertIsNotNone(output_feature)

# -*- coding: utf-8 -*-
"""
    Test.
"""
import logging
import unittest
from pathlib import Path

import numpy as np
from flower_classifier.tools import init_logger, caculate_labels_and_domains_from_paths


class TestTools(unittest.TestCase):
    """ Test tools
    """

    def test_init_logger(self) -> None:  # pylint: disable=R0201
        """ Test init_logger().
        """
        # Given
        logger = logging.getLogger(__name__)

        # When
        init_logger(logger, logging.INFO)

        # Then
        self.assertTrue(logger.isEnabledFor(logging.INFO))

    def test_caculate_labels_and_domains_from_paths(self) -> None:
        # Given
        files = [Path('roses/a.jpg'), Path('tulips/b.jpg'), Path('roses/c.jpg')]

        # When
        # decode_and_resize_image(raw_bytes: bytes, size: Tuple[int, int]) -> np.ndarray:
        labels, domain = caculate_labels_and_domains_from_paths(files)

        # Then
        self.assertEqual(2, len(domain))
        self.assertEqual(0, domain["roses"])
        self.assertEqual(1, domain["tulips"])
        self.assertListEqual(labels, [0, 1, 0])

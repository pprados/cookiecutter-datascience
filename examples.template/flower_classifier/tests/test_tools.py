# -*- coding: utf-8 -*-
"""
    Test.
"""
import logging
import os
import unittest

import numpy as np

from flower_classifier.tools.tools import decode_and_resize_image, init_logger


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

    def test_decode_and_resize_image(self) -> None:
        # Given
        with open(os.path.join("tests", "sample.jpg"), "rb") as image_file:
            data = image_file.read()

        # When
        # decode_and_resize_image(raw_bytes: bytes, size: Tuple[int, int]) -> np.ndarray:
        array: np.ndarray = decode_and_resize_image(data, (10, 10))

        # Then
        self.assertEqual((10, 10, 3), array.shape)
        self.assertTrue(np.float32, array.dtype)

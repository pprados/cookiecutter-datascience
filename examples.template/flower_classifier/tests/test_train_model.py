# -*- coding: utf-8 -*-
"""
    Test.
"""
import os
import unittest

import numpy as np
import pytest
from PIL import Image

from flower_classifier.evaluate_model import evaluate_model
from flower_classifier.train_model import train_model


class TestTrainModel(unittest.TestCase):
    """ Unit test of prepare_dataset.
    """

    @pytest.mark.slow
    @pytest.mark.gpu
    def test_train_model_with_two_image_and_evaluate(self) -> None:  # pylint: disable=no-self-use
        """ Test train_model() with no data.
        """
        # Given
        dim = (100, 100)
        image_datas = \
            [np.array(Image.open(os.path.join("tests", "sample.jpg")).resize(dim), dtype=float),
             np.array(Image.open(os.path.join("tests", "sample.jpg")).resize(dim), dtype=float)]
        labels = [0, 1]
        domain = {"a": 0, "b": 1}

        # When
        model = train_model(labels=labels,
                            domain=domain,
                            image_datas=image_datas,
                            test_ratio=0,
                            epochs=1,
                            batch_size=1,
                            dims=dim,
                            seed=0)
        metric = evaluate_model(model=model,
                                domain=domain,
                                image_datas=image_datas,
                                labels=labels,
                                test_ratio=0,)

        # Then
        self.assertIsNotNone(model)
        self.assertEqual(metric['acc'], 0.5)

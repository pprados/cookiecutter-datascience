# -*- coding: utf-8 -*-
"""
    Test.
"""
import os
import unittest

import pytest

from flower_classifier.evaluate_model import evaluate_model
from flower_classifier.train_model import train_model, Model


class TestTrainModel(unittest.TestCase):
    """ Unit test of prepare_dataset.
    """

    @pytest.mark.slow
    @pytest.mark.gpu
    def test_train_model_with_two_image_and_evaluate(self) -> None:  # pylint: disable=R0201
        """ Test train_model() with no data.
        """
        # Given
        with open(os.path.join("tests", "sample.jpg"), "rb") as image_file:
            data = image_file.read()
        image_datas = [data, data]
        labels = [0, 1]
        domain = {"a": 0, "b": 1}

        # When
        model: Model = train_model(labels=labels,
                                   domain=domain,
                                   image_datas=image_datas,
                                   test_ratio=0,
                                   epochs=1,
                                   batch_size=1,
                                   image_width=100,
                                   image_height=100,
                                   seed=0)
        metric = evaluate_model(model=model,
                                domain=domain,
                                image_datas=image_datas,
                                labels=labels,
                                image_width=100,
                                image_height=100)

        # Then
        self.assertIsNotNone(model)
        self.assertEqual(metric['acc'], 0.5)

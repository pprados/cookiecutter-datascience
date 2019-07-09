# -*- coding: utf-8 -*-
"""
    Test.
"""
import io
import tarfile
import unittest
from pathlib import Path
from typing import List, Any, Tuple, Sequence, Mapping

import numpy as np
import pytest

from flower_classifier.evaluate_model import evaluate_model
from flower_classifier.prepare_dataset import prepare_dataset
from flower_classifier.tools.tools import decode_and_resize_image
from flower_classifier.train_model import train_model, Model


# @pytest.mark.skip(reason="no way of currently testing this")
@pytest.mark.functional
class TestFunctional(unittest.TestCase):
    """ Functional test of pipeline.
    """

    def test_all_pipeline_with_none(self) -> None:  # pylint: disable=R0201
        """ Test prepare_dataset() with no data.
        """
        # Given
        streams = []
        with tarfile.open("tests/samples.tar.xz") as tar:  # pylint: disable=E1120
            for tarf in tar:
                if tarf.isfile():
                    path = Path(tarf.name)
                    # Remove first part
                    path = path.relative_to(*path.parts[:1])
                    streams.append((path, tar.extractfile(tarf)))
            # When
            prepared_data = prepare_dataset(streams=streams)
            _, image_datas = zip(*prepared_data)

        labels = [0, 1]
        domain = {"a": 0, "b": 1}

        model = train_model(labels=labels,
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

        image = decode_and_resize_image(open("tests/sample.jpg", "rb").read(), (100, 100))

        predict = model.predict(np.expand_dims(image, axis=0))

        # Then
        self.assertIsNotNone(model)
        self.assertEqual(metric['acc'], 0.5)
        self.assertGreaterEqual(predict[0][0], 0.5)
        self.assertLessEqual(predict[0][1], 0.5)

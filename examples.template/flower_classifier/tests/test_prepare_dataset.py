# -*- coding: utf-8 -*-
"""
    Test.
"""
import io
import os
import tarfile
import unittest
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import List, Tuple, Sequence

from flower_classifier.prepare_dataset import prepare_dataset


class TestPrepareDataSet(unittest.TestCase):
    """ Unit test of evaluate_model.
    """

    def test_prepare_dataset_with_none(self) -> None:  # pylint: disable=R0201
        """ Test prepare_dataset() with no data.
        """
        # Given

        # When
        prepared_data = prepare_dataset(streams=[])

        # Then
        self.assertIsNotNone(prepared_data)

    def test_prepare_dataset_with_data(self) -> None:
        """ Test prepare_dataset() with no data.
        """
        # Given
        tmpfile = NamedTemporaryFile(suffix=".tgz").name
        with tarfile.open(tmpfile, mode="x:gz") as tar_handle:
            tar_handle.add(os.path.join("tests", "sample.jpg"))

        streams = []
        with tarfile.open(tmpfile) as tar:
            for tarf in tar:
                if tarf.isfile():
                    path = Path(tarf.name)  # pylint: disable=E1120
                    # Remove first part
                    path = path.relative_to(*path.parts[:1])
                    streams.append((path, tar.extractfile(tarf)))
            # When
            prepared_data: Sequence[Tuple[Path, bytes]] = prepare_dataset(streams=streams)

        # Then
        self.assertIsNotNone(prepared_data)
        self.assertEqual(prepared_data[0][0], Path('sample.jpg'))

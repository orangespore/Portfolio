import unittest

import json

from pyspark.sql.functions import mean

from dependencies.spark import start_spark
from jobs.etl_job import flatten_data


class SparkETLTests(unittest.TestCase):
    """Test suite for transformation in etl_job.py
    """

    def setUp(self):
        """Start Spark, define config and path to test data
        """
        self.spark, *_ = start_spark()
        self.test_data_path = 'tests/test_data/'

    def tearDown(self):
        """Stop Spark
        """
        self.spark.stop()

    def test_flatten_data(self):
        """Test data transformer.

        """
        # assemble
        input_data = (
            self.spark
            .read
            .json(self.test_data_path + '210401.json'))

        expected_data = (
            self.spark
            .read
            .json(self.test_data_path + '210401.csv'))

        expected_cols = len(expected_data.columns)
        expected_rows = expected_data.count()

        # act
        data_transformed = flatten_data(input_data)

        cols = len(expected_data.columns)
        rows = expected_data.count()

        # assert
        self.assertEqual(expected_cols, cols)
        self.assertEqual(expected_rows, rows)
        self.assertTrue([col in expected_data.columns
                         for col in data_transformed.columns])


if __name__ == '__main__':
    unittest.main()

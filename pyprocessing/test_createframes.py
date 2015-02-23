#!/bin/env dls-python

import unittest
from pkg_resources import require
require("mock")
from mock import patch, ANY
import createframes


class ReadDataTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('createframes.os.path.exists')
    def test_given_filename_in_argument_when_class_invoked_then_check_file_existence(self, mock_exists):

        filename = 'some_file.hdf5'

        createframes.ReadData(filename)

        mock_exists.assert_called_once_with(filename)

    @patch('createframes.os.path.exists',return_value=False)
    def test_given_filename_in_argument_when_class_invoked_then_assertion_error_if_file_nonexistent(self, mock_exists):

        filename = 'some_file.hdf5'

        with self.assertRaises(AssertionError):
            createframes.ReadData(filename)

    def test_given_real_hdf5_file_when_class_invoked_then_hdf5_file_type_recognised(self):
        pass


if __name__ == '__main__':

    unittest.main()
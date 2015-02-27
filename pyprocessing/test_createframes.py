#!/bin/env dls-python

import unittest
from pkg_resources import require
require("mock")
from mock import patch, ANY
import createframes
import h5py


class ReadDataTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('createframes.h5py.is_hdf5', return_value=True)
    @patch('createframes.os.path.exists')
    def test_given_filename_in_argument_when_method_invoked_then_check_file_existence(self, mock_exists, mock_ish5):

        filename = 'some_file.hdf5'

        createframes.read_data(filename)

        mock_exists.assert_called_once_with(filename)


    @patch('createframes.os.path.exists',return_value=False)
    def test_given_filename_in_argument_when_method_invoked_then_assertion_error_if_file_nonexistent(self, mock_exists):

        filename = 'some_file.hdf5'

        with self.assertRaises(AssertionError):
            createframes.read_data(filename)


    def test_given_real_hdf5_file_when_class_invoked_then_hdf5_file_type_recognised(self):

        filename = '../p2m.hdf5'

        try:
            createframes.read_data(filename)
        except IOError:
            self.fail('createframes.read_data IOerror raised')


class VisitAllObjects(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_given_hdf5_group_argument_when_called_then_return_dict(self):

        with h5py.File('../p2m.hdf5','r') as h5_file:
            h5_group = h5_file[h5_file.keys()[0]]

            data_dict = createframes.visit_all_objects(h5_group,'')

            self.assertIsInstance(data_dict,dict)

    def test_given_non_hdf5_group_argument_when_called_then_return_empty_dict(self):

        data_dict = createframes.visit_all_objects({},'')

        self.assertIsInstance(data_dict,dict)
        self.assertTrue(len(data_dict)==0)


if __name__ == '__main__':

    unittest.main()
#!/dls_sw/prod/tools/RHEL6-x86_64/defaults/bin/dls-python
# testharness.py
#
# Author: Arvinder Palaha

# from pkg_resources import require
# require("numpy")

# import numpy as np
# import h5py

#   open/create file for test image datasets
#   check for datasets
#       if they don't exist, create them
#       if they do exist, read them
#           images for p2m and p13m
#           sample image with flat/ramp/noise
#           all sample images with asymmetric triangle shape
#           all sample images with four slices of different gain
#           conversion between digital and analogue
#           include calibration pixels (to be left empty)
#           all reset images w/ small values: mid-range of fine ADC w/ noise

import unittest
from pyprocessing.createframe import detector

class CreatingFrames(unittest.TestCase):

    def test_detector_has_default_parameters(self):
        det_obj = detector()
        columns = det_obj.ncol
        rows = det_obj.nrow
        calibrationcolumns = det_obj.ncolcal
        calibrationrows = det_obj.nrowcal
        self.assertEqual(1484,rows)
        self.assertEqual(1408,columns)
        self.assertEqual(7,calibrationrows)
        self.assertEqual(8,calibrationcolumns)

if __name__ == '__main__':
    unittest.main()
#!/dls_sw/prod/tools/RHEL6-x86_64/defaults/bin/dls-python
# testharness.py
#
# Author: Arvinder Palaha

from pkg_resources import require
require("numpy")

import numpy as np
import h5py
import timeit

from pyprocessing.createframe import *

print "hello world"

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
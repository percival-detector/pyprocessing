# createframe.py
#
# Author: Arvinder Palaha
from pkg_resources import require
require('numpy')
import os
import h5py
import numpy as np

def ReadData(filename):

    try:
        assert os.path.exists(filename)
    except AssertionError as e:
        e.args += (filename, 'does not exist')
        raise

    if not h5py.is_hdf5(filename):
        raise IOError('%s does not look like a hdf5 file' % filename)
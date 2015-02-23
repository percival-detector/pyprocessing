# createframe.py
#
# Author: Arvinder Palaha
import os

def ReadData(filename):

    if not filename.endswith(('.h5','.hdf5')):
        raise IOError('filename does not end with hdf5 format extension')

    try:
        assert os.path.exists(filename)
    except AssertionError as e:
        e.args += (filename, 'does not exist')
        raise
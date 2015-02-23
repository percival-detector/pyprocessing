# createframe.py
#
# Author: Arvinder Palaha
import os

def ReadData(filename):

    try:
        assert os.path.exists(filename)
    except AssertionError as e:
        e.args += (filename, 'does not exist')
        raise
# createframe.py
#
# Author: Arvinder Palaha
import os

class ReadData:

    def __init__(self, filename):

        try:
            assert os.path.exists(filename)
        except AssertionError as e:
            e.args += (filename, 'does not exist')
            raise

        self.filename = filename
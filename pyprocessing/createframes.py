# createframe.py
#
# Author: Arvinder Palaha
import os

class ReadData:

    def __init__(self, filename):

        assert os.path.exists(filename)

        self.filename = filename
# createframe.py
#
# Author: Arvinder Palaha
from pkg_resources import require
require('numpy')
import os
import h5py
import numpy as np


def visit_all_objects(group, path='', file_info=None):

    if file_info is None:
        file_info = {}

    for i in group.items():
        if isinstance(i[1], h5py.Group):
            visit_all_objects(i[1], path + '/' + i[0], file_info)
        elif isinstance(i[1], h5py.Dataset):
            dataset_name = path + '/' + i[0]
            file_info[dataset_name] = (i[1].shape,i[1].dtype)
    
    return file_info


class DataReader:

    def __init__(self,filename):
        try:
            assert os.path.exists(filename)
        except AssertionError as e:
            e.args += (filename, 'does not exist')
            raise

        if not h5py.is_hdf5(filename):
            raise IOError('%s does not look like a hdf5 file' % filename)

        self.file = h5py.File(filename,'r')
        self.dset_info = visit_all_objects(self.file)

    def get_dataset(self,path=''):
        return np.array((1,2))

#!/dls_sw/prod/tools/RHEL6-x86_64/defaults/bin/dls-python
# testharness.py
#
# Author: Arvinder Palaha

# Algorithm:
#
# generate datasets
#   create/open hdf5 file
#   create/open datasets
#     if no dset, create dset for 1 SAMPLE + RESET frame, for each P2M and P13M
#     method to append frames to dset (resizeable dset)
# implement processing steps 3-7
#   implement alternative methods for some steps
#   allow toggling of each processing step
# measure performance of implemented functions

# pick up dls controls environment and versioned libraries
from pkg_resources import require
require("numpy")

# import needed modules
import numpy as np
import h5py

# frame dimensions
nrow2 = 1408
ncol2 = 1484
nrow13 = 3528
ncol13 = 3717
nrowcal = 8
ncolcal = 7

# read write if exists, create otherwise
filename = 'processing-test-data.hdf5'
f = h5py.File(filename,'a')
print f.items()

# read/create file structure
gp2m = f.require_group("/p2m")
gp13m = f.require_group("/p13m")

# read/create datasets for RESET and SAMPLE frames
dsetp2m_s = gp2m.require_dataset('sample',
    shape=(1,ncol2+ncolcal,nrow2+nrowcal),
    dtype='uint16',
    exact=False)
dsetp2m_r = gp2m.require_dataset('reset',
    shape=(1,ncol2+ncolcal,nrow2+nrowcal),
    dtype='uint16',
    exact=False)
dsetp13m_s = gp13m.require_dataset('sample',
    shape=(1,ncol13+ncolcal,nrow13+nrowcal),
    dtype='uint16',
    exact=False)
dsetp13m_r = gp13m.require_dataset('reset',
    shape=(1,ncol13+ncolcal,nrow13+nrowcal),
    dtype='uint16',
    exact=False)

# create a linearly ramping (pixel by pixel) "image", use for reset and sample
dsetp2m_s[...] = np.arange(0,(ncol2+ncolcal)*(nrow2+nrowcal),
    dtype=np.uint16).reshape((ncol2+ncolcal,nrow2+nrowcal))
print dsetp2m_s[...]
dsetp2m_r[...] = dsetp2m_s[...]
dsetp13m_s[...] = np.arange(0,(ncol13+ncolcal)*(nrow13+nrowcal),
    dtype=np.uint16).reshape((ncol13+ncolcal,nrow13+nrowcal))
dsetp13m_r[...] = dsetp13m_s[...]

# create a 'flat' image 
# dsetp2m_s.resize(2)
# print dsetp2m_s.maxshape

# close the file
f.close()
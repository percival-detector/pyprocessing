#!/dls_sw/prod/tools/RHEL6-x86_64/defaults/bin/dls-python
# testharness.py
#
# Author: Arvinder Palaha

# Tasks
#
#    1 Develop a script which will generate a small set of test files to run processing on
#     a    Use numpy to generate appropriate datasets
#     b    Store datasets in HDF5 format
#     c    A file for each detector size: P2M, P13M
#     d    Different datasets for SAMPLE and RESET frames
#     e    Different datasets with varying noise levels
#    2 Implement functions to carry out the steps 3-7 of processing required
#     a    Note that some functions have alternatives - which also need to be implemented.
#     b    Implementation in a fashion so that the individual functions can be enabled/disabled and replaced by alternative implementations
#    3 Measure the performance of the implemented functions
#     a    See for instance ipython %time or %timeit


# pick up dls controls environment and versioned libraries
from pkg_resources import require
require("numpy")
require("h5py")
require("matplotlib")

# import modules as needed
import numpy as np 
import h5py
import matplotlib as mpl
from matplotlib.pylab import *

#-------------------------------------------------------------------------------
# 1a: use numpy to generate appropriate datasets

# start with p2m, store the dimensions in pixels as integers
nrow, ncol = 1408, 1484

# We want a 2d array of 15-bit integers, nearest real type is uint16
# Wo test the range of the image storage, let's fill the dataset with a linear
# ramp from 0 to 2**15-1 = 32767
ramp = np.arange(0,nrow*ncol,1,dtype=np.uint16) # linear ramp 1d array

# want to clip ramp at 2**15-1, using remainder of division (modulus)
ramp[ramp>2**15-1] %= 2**15 
# print max(ramp), ramp[2**15-2:2**15+2]

# reshape the 1d array with nrow*ncol entries to 2d array of (nrow,ncol) shape
ramp = ramp.reshape((nrow,ncol))

# dataset values, shape (dimensions), number of values, size in MB
print ramp, ramp.shape, ramp.size, ramp.nbytes/1024.**2, "MB"

# put this functionality into ... a function!
def linear_ramp_frame(rows,cols):
    frame = np.arange(0,rows*cols,1,dtype=np.uint16) # 1d array of rising ints
    frame[frame>2**15-1] %= 2**15      # reset ramp to 0 at every 2**15
    frame = frame.reshape((rows,cols)) # change to 2d array
    return frame

# other algorithms to produce test images:
#   flat colour (pick a value between 0 and 2**15-1)                        done
#   diagonal ramp (saw tooth gradient from corner to corner)                done
#   2-d gaussian                                                            done

def flat_frame(rows,cols,shade):
    shade %= 2**15
    frame = np.empty((rows,cols),dtype=np.uint16)
    frame[:] = shade
    return frame

def diagonal_ramp_frame(rows,cols):
    # print "diagonal_ramp_frame not implemented"
    frame = np.empty((rows,cols),dtype=np.uint16)
    for x in range(0,rows): # iterates integers from 0 to (rows-1)
        frame[x,:] = np.linspace(x,cols-1+x,cols).astype(np.uint16)
        frame[x,:] %= 2**15
    return frame

def gaussian_frame(rows,cols):
    x = np.arange(0,rows,1,float)
    y = x[:,np.newaxis]
    x0 = fwhmx = rows/2 
    y0 = fwhmy = cols/2
    return (np.exp(-4*np.log(2) * ((x-x0)**2/fwhmx**2 + (y-y0)**2/fwhmy**2))*(2**15-1)).astype(np.uint16)


#-------------------------------------------------------------------------------
# 1b: store datasets in HDF5 format

# open a hdf5 file with h5py, create it if it doesn't exist
# using 'with, as:' like this ensures file closes after this scope
with h5py.File('p2m_test_frames.hdf5','a') as f:

    # store ramp image to file
    dset = f.require_dataset('ramp',ramp.shape,dtype=ramp.dtype,exact=False)
    print dset[()] # show stored values, will be 0's if 1st time file opened
    dset[...] = ramp
    print dset[()] # show assigned values


#-------------------------------------------------------------------------------
# 1c: a file for each detector size (P2M and P13M)

# dimensions for P13M detector in pixels
nrow2, ncol2 = 3528,3717

# open a second file for the larger detector size, create it if it doesn't exist
with h5py.File('p13m_test_frames.hdf5','a') as f:

    # create/open dataset ready for linear ramp image with P13M dimensions
    dset = f.require_dataset('ramp',(nrow2,ncol2),dtype='uint16',exact=False)
    print dset[()], dset.shape, dset.size,


#-------------------------------------------------------------------------------
# 1d: different datasets for SAMPLE and RESET frames

# create a flat frame for each detector size, to act as the RESET frame
small_flat_reset = flat_frame(nrow,ncol,2**15/2)
large_flat_reset = flat_frame(nrow2,ncol2,2**15/2) # this works

# create two sample frames with a single shade/value
small_flat = flat_frame(nrow,ncol,2**15/8)
large_flat = flat_frame(nrow2,ncol2,15*(2**15)/16) # this works too :)

# create two sample frames with a diagonal ramp
small_diagonal = diagonal_ramp_frame(nrow,ncol)
large_diagonal = diagonal_ramp_frame(nrow2,ncol2) # these work!
# print small_diagonal[()], large_diagonal[()]

tiny_diagonal = diagonal_ramp_frame(10,12);
print tiny_diagonal[()]

small_gaus = gaussian_frame(nrow,ncol)
large_gaus = gaussian_frame(nrow2,ncol2) # these work!
print small_gaus[()]

matshow(small_gaus,cmap=cm.Greys)
show()

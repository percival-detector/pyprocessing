#!/dls_sw/prod/tools/RHEL6-x86_64/defaults/bin/dls-python
# generate_test_images.py
#
# Author: Arvinder Palaha

################################################################################
from pkg_resources import require
require("numpy")
require("matplotlib")


################################################################################
from pyprocessing.createframe import *
from matplotlib.pylab import *
import h5py
import numpy as np


################################################################################
######## ##     ## ##    ##  ######  ######## ####  #######  ##    ##  ######  
##       ##     ## ###   ## ##    ##    ##     ##  ##     ## ###   ## ##    ## 
##       ##     ## ####  ## ##          ##     ##  ##     ## ####  ## ##       
######   ##     ## ## ## ## ##          ##     ##  ##     ## ## ## ##  ######  
##       ##     ## ##  #### ##          ##     ##  ##     ## ##  ####       ## 
##       ##     ## ##   ### ##    ##    ##     ##  ##     ## ##   ### ##    ## 
##        #######  ##    ##  ######     ##    ####  #######  ##    ##  ######  

def check_create_dataset(group,dname,dshape):

    try:
        dset = group[dname]

    except KeyError:
        dset = group.require_dataset(
            dname,
            (1,dshape[0],dshape[1]),
            dtype='uint16',
            maxshape=(None,dshape[0],dshape[1]),
            fillvalue=2**16-1)
    
    # print dset.shape, dset.dtype, dset.attrs.keys()

    if dset[0,0,0] == dset.fillvalue:
        return 1 # dataset not allocated, need to generate image
    else:
        return 0 # dataset allocated, assume image already generated


################################################################################
########   #######  ##     ## 
##     ## ##     ## ###   ### 
##     ##        ## #### #### 
########   #######  ## ### ## 
##        ##        ##     ## 
##        ##        ##     ## 
##        ######### ##     ##

# standard detector parameters (pixel dimensions, etc)
p2m = detector()
p2mshape = p2m.fullshape


with h5py.File('p2m.hdf5','a') as f:

    print 'entering file', f.filename

    ############################################################################
    ########  ####  ######   #### ########    ###    ##       
    ##     ##  ##  ##    ##   ##     ##      ## ##   ##       
    ##     ##  ##  ##         ##     ##     ##   ##  ##       
    ##     ##  ##  ##   ####  ##     ##    ##     ## ##       
    ##     ##  ##  ##    ##   ##     ##    ######### ##       
    ##     ##  ##  ##    ##   ##     ##    ##     ## ##       
    ########  ####  ######   ####    ##    ##     ## ######## 

    dgroup = f.require_group('digital')

    # flat
    if check_create_dataset(dgroup,'flat',p2mshape):
        print 'creating digital flat image'
        dset = dgroup['flat']
        image = p2m.triangleflat(2**12-1)
        p2m.gainslices(image)
        image = p2m.addcalibrationpixels(image)
        dset[0] = image

    # flat_noisy
    if check_create_dataset(dgroup,'flat_noisy',p2mshape):
        print 'creating digital flat_noisy image'
        dset = dgroup['flat_noisy']
        image = p2m.triangleflat(2**12-1)
        p2m.poissonnoise(image)
        p2m.gainslices(image)
        image = p2m.addcalibrationpixels(image)
        dset[0] = image

    # ramp
    if check_create_dataset(dgroup,'ramp',p2mshape):
        print 'creating digital linear ramp image'
        dset = dgroup['ramp']
        image = p2m.trianglelinramp(p2m.nrow*p2m.ncol*1./(2.**p2m.nbit-1))
        p2m.gainslices(image)
        image = p2m.addcalibrationpixels(image)
        dset[0] = image

    # ramp_noisy
    if check_create_dataset(dgroup,'ramp_noisy',p2mshape):
        print 'creating digital noisy linear ramp  image'
        dset = dgroup['ramp_noisy']
        image = p2m.trianglelinramp(p2m.nrow*p2m.ncol*1./(2.**p2m.nbit-1))
        p2m.poissonnoise(image)
        p2m.gainslices(image)
        image = p2m.addcalibrationpixels(image)
        dset[0] = image

    # diag
    if check_create_dataset(dgroup,'diag',p2mshape):
        print 'creating digital diagonal ramp image'
        dset = dgroup['diag']
        image = p2m.trianglediagonalramp(5)
        p2m.gainslices(image)
        image = p2m.addcalibrationpixels(image)
        dset[0] = image

    # diag_noisy
    if check_create_dataset(dgroup,'diag_noisy',p2mshape):
        print 'creating digital noisy diagonal ramp image'
        dset = dgroup['diag_noisy']
        image = p2m.trianglediagonalramp(5)
        p2m.poissonnoise(image)
        p2m.gainslices(image)
        image = p2m.addcalibrationpixels(image)
        dset[0] = image

    # randm
    if check_create_dataset(dgroup,'randm',p2mshape):
        print 'creating digital random image'
        dset = dgroup['randm']
        image = p2m.trianglerandom()
        p2m.gainslices(image)
        image = p2m.addcalibrationpixels(image)
        dset[0] = image

    # randm_noisy
    if check_create_dataset(dgroup,'randm_noisy',p2mshape):
        print 'creating digital noisy random image'
        dset = dgroup['randm_noisy']
        image = p2m.trianglerandom()
        p2m.poissonnoise(image)
        p2m.gainslices(image)
        image = p2m.addcalibrationpixels(image)
        dset[0] = image

    # reset
    if check_create_dataset(dgroup,'reset',p2mshape):
        print 'creating digital reset image'
        dset = dgroup['reset']
        image = p2m.triangleflat(2**7-1) # midpoint of fine ADU range, 0 coarse
        # p2m.gainslices(image) # don't need gain slices for a reset image
        image = p2m.addcalibrationpixels(image)
        dset[0] = image

    # reset_noisy
    if check_create_dataset(dgroup,'reset_noisy',p2mshape):
        print 'creating digital noisy reset image'
        dset = dgroup['reset_noisy']
        image = p2m.triangleflat(2**7-1) # midpoint of fine ADU range, 0 coarse
        p2m.poissonnoise(image)
        # p2m.gainslices(image) # don't need gain slices for a reset image
        image = p2m.addcalibrationpixels(image)
        dset[0] = image

    ############################################################################
       ###    ##    ##    ###    ##        #######   ######   
      ## ##   ###   ##   ## ##   ##       ##     ## ##    ##  
     ##   ##  ####  ##  ##   ##  ##       ##     ## ##        
    ##     ## ## ## ## ##     ## ##       ##     ## ##   #### 
    ######### ##  #### ######### ##       ##     ## ##    ##  
    ##     ## ##   ### ##     ## ##       ##     ## ##    ##  
    ##     ## ##    ## ##     ## ########  #######   ######   

    dgroup = f.require_group('analog')

    # flat
    if check_create_dataset(dgroup,'flat',p2mshape):
        print 'converting flat image to analog'
        dset = dgroup['flat']
        image = f['digital/flat'][0]
        image = p2m.digital2analog(image)
        dset[0] = image

    # flat_noisy
    if check_create_dataset(dgroup,'flat_noisy',p2mshape):
        print 'converting noisy flat image to analog'
        dset = dgroup['flat_noisy']
        image = f['digital/flat_noisy'][0]
        image = p2m.digital2analog(image)
        dset[0] = image

    # ramp
    if check_create_dataset(dgroup,'ramp',p2mshape):
        print 'converting ramp image to analog'
        dset = dgroup['ramp']
        image = f['digital/ramp'][0]
        image = p2m.digital2analog(image)
        dset[0] = image

    # ramp_noisy
    if check_create_dataset(dgroup,'ramp_noisy',p2mshape):
        print 'converting noisy ramp image to analog'
        dset = dgroup['ramp_noisy']
        image = f['digital/ramp_noisy'][0]
        image = p2m.digital2analog(image)
        dset[0] = image

    # diag
    if check_create_dataset(dgroup,'diag',p2mshape):
        print 'converting diag image to analog'
        dset = dgroup['diag']
        image = f['digital/diag'][0]
        image = p2m.digital2analog(image)
        dset[0] = image

    # diag_noisy
    if check_create_dataset(dgroup,'diag_noisy',p2mshape):
        print 'converting noisy diag image to analog'
        dset = dgroup['diag_noisy']
        image = f['digital/diag_noisy'][0]
        image = p2m.digital2analog(image)
        dset[0] = image

    # randm
    if check_create_dataset(dgroup,'randm',p2mshape):
        print 'converting randm image to analog'
        dset = dgroup['randm']
        image = f['digital/randm'][0]
        image = p2m.digital2analog(image)
        dset[0] = image

    # randm_noisy
    if check_create_dataset(dgroup,'randm_noisy',p2mshape):
        print 'converting noisy randm image to analog'
        dset = dgroup['randm_noisy']
        image = f['digital/randm_noisy'][0]
        image = p2m.digital2analog(image)
        dset[0] = image

    # reset
    if check_create_dataset(dgroup,'reset',p2mshape):
        print 'converting reset image to analog'
        dset = dgroup['reset']
        image = f['digital/reset'][0]
        image = p2m.digital2analog(image)
        dset[0] = image

    # reset_noisy
    if check_create_dataset(dgroup,'reset_noisy',p2mshape):
        print 'converting noisy reset image to analog'
        dset = dgroup['reset_noisy']
        image = f['digital/reset_noisy'][0]
        image = p2m.digital2analog(image)
        dset[0] = image

################################################################################
########     ##    #######  ##     ## 
##     ##  ####   ##     ## ###   ### 
##     ##    ##          ## #### #### 
########     ##    #######  ## ### ## 
##           ##          ## ##     ## 
##           ##   ##     ## ##     ## 
##         ######  #######  ##     ## 

# larger detector parameters (pixel dimensions, etc)
p13m = detector(3528,3717)
p13mshape = p13m.fullshape

with h5py.File('p13m.hdf5','a') as f:

    print 'entering file', f.filename

    ############################################################################
    ########  ####  ######   #### ########    ###    ##       
    ##     ##  ##  ##    ##   ##     ##      ## ##   ##       
    ##     ##  ##  ##         ##     ##     ##   ##  ##       
    ##     ##  ##  ##   ####  ##     ##    ##     ## ##       
    ##     ##  ##  ##    ##   ##     ##    ######### ##       
    ##     ##  ##  ##    ##   ##     ##    ##     ## ##       
    ########  ####  ######   ####    ##    ##     ## ######## 

    dgroup = f.require_group('digital')

    # flat
    if check_create_dataset(dgroup,'flat',p13mshape):
        print 'creating digital flat image'
        dset = dgroup['flat']
        image = p13m.triangleflat(2**12-1)
        p13m.gainslices(image)
        image = p13m.addcalibrationpixels(image)
        dset[0] = image

    # flat_noisy
    if check_create_dataset(dgroup,'flat_noisy',p13mshape):
        print 'creating digital flat_noisy image'
        dset = dgroup['flat_noisy']
        image = p13m.triangleflat(2**12-1)
        p13m.poissonnoise(image)
        p13m.gainslices(image)
        image = p13m.addcalibrationpixels(image)
        dset[0] = image

    # ramp
    if check_create_dataset(dgroup,'ramp',p13mshape):
        print 'creating digital linear ramp image'
        dset = dgroup['ramp']
        image = p13m.trianglelinramp(p13m.nrow*p13m.ncol*1./(2.**p13m.nbit-1))
        p13m.gainslices(image)
        image = p13m.addcalibrationpixels(image)
        dset[0] = image

    # ramp_noisy
    if check_create_dataset(dgroup,'ramp_noisy',p13mshape):
        print 'creating digital noisy linear ramp  image'
        dset = dgroup['ramp_noisy']
        image = p13m.trianglelinramp(p13m.nrow*p13m.ncol*1./(2.**p13m.nbit-1))
        p13m.poissonnoise(image)
        p13m.gainslices(image)
        image = p13m.addcalibrationpixels(image)
        dset[0] = image

    # diag
    if check_create_dataset(dgroup,'diag',p13mshape):
        print 'creating digital diagonal ramp image'
        dset = dgroup['diag']
        image = p13m.trianglediagonalramp(5)
        p13m.gainslices(image)
        image = p13m.addcalibrationpixels(image)
        dset[0] = image

    # diag_noisy
    if check_create_dataset(dgroup,'diag_noisy',p13mshape):
        print 'creating digital noisy diagonal ramp image'
        dset = dgroup['diag_noisy']
        image = p13m.trianglediagonalramp(5)
        p13m.poissonnoise(image)
        p13m.gainslices(image)
        image = p13m.addcalibrationpixels(image)
        dset[0] = image

    # randm
    if check_create_dataset(dgroup,'randm',p13mshape):
        print 'creating digital random image'
        dset = dgroup['randm']
        image = p13m.trianglerandom()
        p13m.gainslices(image)
        image = p13m.addcalibrationpixels(image)
        dset[0] = image

    # randm_noisy
    if check_create_dataset(dgroup,'randm_noisy',p13mshape):
        print 'creating digital noisy random image'
        dset = dgroup['randm_noisy']
        image = p13m.trianglerandom()
        p13m.poissonnoise(image)
        p13m.gainslices(image)
        image = p13m.addcalibrationpixels(image)
        dset[0] = image

    # reset
    if check_create_dataset(dgroup,'reset',p13mshape):
        print 'creating digital reset image'
        dset = dgroup['reset']
        image = p13m.triangleflat(2**7-1) # midpoint of fine ADU range, 0 coarse
        # p13m.gainslices(image) # don't need gain slices for a reset image
        image = p13m.addcalibrationpixels(image)
        dset[0] = image

    # reset_noisy
    if check_create_dataset(dgroup,'reset_noisy',p13mshape):
        print 'creating digital noisy reset image'
        dset = dgroup['reset_noisy']
        image = p13m.triangleflat(2**7-1) # midpoint of fine ADU range, 0 coarse
        p13m.poissonnoise(image)
        # p13m.gainslices(image) # don't need gain slices for a reset image
        image = p13m.addcalibrationpixels(image)
        dset[0] = image

    ############################################################################
       ###    ##    ##    ###    ##        #######   ######   
      ## ##   ###   ##   ## ##   ##       ##     ## ##    ##  
     ##   ##  ####  ##  ##   ##  ##       ##     ## ##        
    ##     ## ## ## ## ##     ## ##       ##     ## ##   #### 
    ######### ##  #### ######### ##       ##     ## ##    ##  
    ##     ## ##   ### ##     ## ##       ##     ## ##    ##  
    ##     ## ##    ## ##     ## ########  #######   ######   

    dgroup = f.require_group('analog')

    # flat
    if check_create_dataset(dgroup,'flat',p13mshape):
        print 'converting flat image to analog'
        dset = dgroup['flat']
        image = f['digital/flat'][0]
        image = p13m.digital2analog(image)
        dset[0] = image

    # flat_noisy
    if check_create_dataset(dgroup,'flat_noisy',p13mshape):
        print 'converting noisy flat image to analog'
        dset = dgroup['flat_noisy']
        image = f['digital/flat_noisy'][0]
        image = p13m.digital2analog(image)
        dset[0] = image

    # ramp
    if check_create_dataset(dgroup,'ramp',p13mshape):
        print 'converting ramp image to analog'
        dset = dgroup['ramp']
        image = f['digital/ramp'][0]
        image = p13m.digital2analog(image)
        dset[0] = image

    # ramp_noisy
    if check_create_dataset(dgroup,'ramp_noisy',p13mshape):
        print 'converting noisy ramp image to analog'
        dset = dgroup['ramp_noisy']
        image = f['digital/ramp_noisy'][0]
        image = p13m.digital2analog(image)
        dset[0] = image

    # diag
    if check_create_dataset(dgroup,'diag',p13mshape):
        print 'converting diag image to analog'
        dset = dgroup['diag']
        image = f['digital/diag'][0]
        image = p13m.digital2analog(image)
        dset[0] = image

    # diag_noisy
    if check_create_dataset(dgroup,'diag_noisy',p13mshape):
        print 'converting noisy diag image to analog'
        dset = dgroup['diag_noisy']
        image = f['digital/diag_noisy'][0]
        image = p13m.digital2analog(image)
        dset[0] = image

    # randm
    if check_create_dataset(dgroup,'randm',p13mshape):
        print 'converting randm image to analog'
        dset = dgroup['randm']
        image = f['digital/randm'][0]
        image = p13m.digital2analog(image)
        dset[0] = image

    # randm_noisy
    if check_create_dataset(dgroup,'randm_noisy',p13mshape):
        print 'converting noisy randm image to analog'
        dset = dgroup['randm_noisy']
        image = f['digital/randm_noisy'][0]
        image = p13m.digital2analog(image)
        dset[0] = image

    # reset
    if check_create_dataset(dgroup,'reset',p13mshape):
        print 'converting reset image to analog'
        dset = dgroup['reset']
        image = f['digital/reset'][0]
        image = p13m.digital2analog(image)
        dset[0] = image

    # reset_noisy
    if check_create_dataset(dgroup,'reset_noisy',p13mshape):
        print 'converting noisy reset image to analog'
        dset = dgroup['reset_noisy']
        image = f['digital/reset_noisy'][0]
        image = p13m.digital2analog(image)
        dset[0] = image

# matshow(diagonal_ramp,cmap=cm.Greys_r)
# matshow(diagonal_ramp,cmap=cm.hot)
# matshow(analog_diagonal_ramp,cmap=cm.hot)
# colorbar()

# plt.show()

#!/dls_sw/prod/tools/RHEL6-x86_64/defaults/bin/dls-python
# generate_test_images.py
#
# Author: Arvinder Palaha

from pkg_resources import require
require("numpy")
require("matplotlib")

from pyprocessing.createframe import *
from matplotlib.pylab import *

p2m = detector()

triangle_mask = p2m.trianglemask() # true/false array of triangle shape

diagonal_ramp = p2m.diagonalxy(3)  # roughly 2*n diagonal ramps in pixel value
diagonal_ramp = triangle_mask*diagonal_ramp # apply triangle mask
p2m.gainslices(diagonal_ramp)      # apply different major gains over 4 slices
diagonal_ramp = p2m.addcalibrationpixels(diagonal_ramp) # returns larger array


# matshow(diagonal_ramp,cmap=cm.Greys_r)
matshow(diagonal_ramp,cmap=cm.hot)
colorbar()

plt.show()

import numpy as np


def linear_ramp_frame(x,y,clip=2**15):
    assert clip>0 
    assert x>0
    assert y>0
    frame = np.arange(x*y,dtype=np.uint16)
    frame[frame>clip-1] %= clip
    frame = frame.reshape((x,y))
    return frame

def flat_frame(x,y,shade,clip=2**15):
    assert x>0
    assert y>0
    assert clip>0 
    frame = np.empty((x,y),dtype=np.uint16)
    frame[:] = shade
    return frame

def diagonal_ramp_frame(x,y,clip=2**15):
    assert x>0
    assert y>0
    assert clip>0
    frame=np.empty((x,y),dtype=np.uint16)
    for row in range(x):
        frame[row,:] = np.linspace(0,clip-1,y).astype(np.uint16)+row*(clip-1)/x
        frame[row,:] %= clip
    return frame

def gaussian_frame(x,y,norm=2**15):
    assert x>0 
    assert y>0
    assert norm>0
    rows = np.arange(x)
    cols = np.arange(y)
    rows,cols = np.meshgrid(rows,cols)
    # norm = 10
    print rows, rows.shape, cols, cols.shape
    frame = (
        (norm-1)*np.exp(-4*np.log(2)
            * ( (rows-x/2.)**2/(x/2.5)**2 + (cols-y/2.)**2/(y/2.5)**2) )
        ).astype(np.uint16)
    return frame


class detector:

    def __init__(self,r = 1408,c = 1484,n = 15,rc = 8,cc = 7):
        self.nrow = r  
        self.ncol = c  
        self.nbit = n  
        self.rcal = rc # calibration rows
        self.ccal = cc # calibration columns

    def linramp(self):
        return linear_ramp_frame(
            self.nrow,
            self.ncol,
            2**self.nbit)

    def flat(self,shade):
        return flat_frame(
            self.nrow,
            self.ncol,
            shade,
            2**self.nbit)

    def diagonal(self):
        return diagonal_ramp_frame(
            self.nrow,
            self.ncol,
            2**self.nbit)

    def gaussian(self):
        return gaussian_frame(
            self.nrow,
            self.ncol,
            2**self.nbit)
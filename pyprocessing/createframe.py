# createframe.py
#
# Author: Arvinder Palaha
# import numpy as np
# import processframe as prcf


# class detector(object):

#     def __init__(self,
#         c = 1408, r = 1484, cc = 8, cr = 7,
#         Oc = 0, Gc = 1, Oct = 2**8-1, Gct = 2**8,
#         Of = 0, Gf = 1, Oft = 0,      Gft = 1
#         ):
#         self.nCol = c
#         self.nRow = r
#         self.nColCal = cc
#         self.nRowCal = cr
#         self.coarseOffset = Oc
#         self.coarseGain = Gc
#         self.fineOffset = Of
#         self.fineGain = Gf
#         self.coarseOffsetTarget = Oct
#         self.coarseGainTarget = Gct
#         self.fineOffsetTarget = Oft
#         self.fineGainTarget = Gft

# class detector:

#     def __init__(self,
#         c=1408, r=1484, cc=8, cr=7, n=13,
#         Oc = 0, Gc = 1, Oct = 2**8-1, Gct = 2**8,
#         Of = 0, Gf = 1, Oft = 0,      Gft = 1
#         ):
#         self.ncol = c
#         self.nrow = r
#         # self.nbit = n
#         self.ncolcal = cc
#         self.nrowcal = cr
#         self.coarseOffset = Oc
#         self.coarseGain = Gc
#         self.fineOffset = Of
#         self.fineGain = Gf
#         self.coarseOffsetTarget = Oct
#         self.coarseGainTarget = Gct
#         self.fineOffsetTarget = Oft
#         self.fineGainTarget = Gft

        
#     def flatimage(self,shade):
#         assert shade>0
#         image = np.zeros((self.nrow,self.ncol),dtype=np.uint16)
#         image[:] = shade % 2**self.nbit
#         return image

#     def linramp(self,nramps=1):
#         image = np.linspace(0,nramps*(2**self.nbit-1),self.nrow*self.ncol)
#         image %= 2**self.nbit
#         image = image.reshape((self.nrow,self.ncol)).astype(np.uint16)
#         return image

#     def diagonalxy(self,nramps=1):
#         assert nramps >= 1
#         return self.linramp(nramps*(self.nrow+1))

#     def gaussian(self,nramps=1):
#         xpoint = np.arange(self.ncol)
#         ypoint = np.arange(self.nrow)
#         xpoint,ypoint = np.meshgrid(xpoint,ypoint)
#         image = nramps*(2**self.nbit-1) * np.exp(
#             -4*np.log(2)
#             *( (xpoint-self.ncol/2.)**2/(self.ncol/2.5)**2
#             + (ypoint-self.nrow/2.)**2/(self.nrow/2.5)**2 )
#             )
#         image %= 2**self.nbit
#         return image.astype(np.uint16)

#     def randomframe(self):
#         return (
#             (2**self.nbit-1)
#             *np.random.random((self.nrow,self.ncol))
#             ).astype(np.uint16)

#     def trianglemask(self,
#         x1=.0, y1=.45 ,
#         x2=1., y2=.05,
#         x3=.9, y3=1. ):
        
#         tglparams = triangleparams(
#             x1*self.ncol, y1*self.nrow,
#             x2*self.ncol, y2*self.nrow,
#             x3*self.ncol, y3*self.nrow)
        
#         ypoint = np.arange(self.nrow)
#         xpoint = np.arange(self.ncol)

#         xpoint,ypoint = np.meshgrid(xpoint,ypoint)

#         mask1 = ypoint - tglparams.mAB*xpoint < tglparams.cAB
#         mask2 = ypoint - tglparams.mBC*xpoint < tglparams.cBC
#         mask3 = ypoint - tglparams.mCA*xpoint < tglparams.cCA

#         mask1 = mask1 if not tglparams.sideC else np.invert(mask1)
#         mask2 = mask2 if not tglparams.sideA else np.invert(mask2)
#         mask3 = mask3 if not tglparams.sideB else np.invert(mask3)

#         mask = mask1 & mask2 & mask3
#         return mask

#     def triangleflat(self,shade=100):
#         return self.trianglemask()*self.flatimage(shade)

#     def trianglelinramp(self,nramps=1):
#         return self.trianglemask()*self.linramp(nramps)

#     def trianglediagonalramp(self,nramps=1):
#         return self.trianglemask()*self.diagonalxy(nramps)

#     def trianglerandom(self):
#         return self.trianglemask()*self.randomframe()

#     def trianglegaus(self,nramps=5):
#         return self.trianglemask()*self.gaussian(nramps)

#     def addcalibrationpixels(self,image):
#         rows,cols = image.shape
#         rows += self.nrowcal
#         cols += self.ncolcal
#         newimage = np.zeros((rows,cols),dtype=image.dtype)
#         newimage[:rows-self.nrowcal,self.ncolcal:] = image[()]
#         return newimage

#     def gainslices(self,image):
#         quarter = image.shape[0]/4.
#         # image[0:quarter,:] += 0
#         image[1*quarter:2*quarter , :] += (1<<self.nbit)
#         image[2*quarter:3*quarter , :] += (1<<(self.nbit+1))
#         image[3*quarter:4*quarter , :] += (1<<self.nbit)+(1<<(self.nbit+1))

#     def poissonnoise(self,image):
#         vfunc = np.vectorize(prcf.poissonnoisepixel)
#         image[...] = vfunc(image,self.nbit)

#     def digital2analog(self,digital):
#         vfunc = np.vectorize(prcf.digital2analogpixel)
#         return vfunc(digital)


# class triangleparams:

#     def __init__(self,
#         ax = 0.0,ay = 0.45,
#         bx = 1.0,by = 0.05,
#         cx = 0.9,cy = 1.00):
#         self.ax = ax
#         self.ay = ay
#         self.bx = bx
#         self.by = by
#         self.cx = cx
#         self.cy = cy
#         self.mAB = (by-ay)/(bx-ax)
#         self.mBC = (by-cy)/(bx-cx)
#         self.mCA = (cy-ay)/(cx-ax)
#         self.cAB = ay-self.mAB*ax
#         self.cBC = by-self.mBC*bx
#         self.cCA = cy-self.mCA*cx
#         self.sideA = True if ay - self.mBC*ax > self.cBC else False
#         self.sideB = True if by - self.mCA*bx > self.cCA else False
#         self.sideC = True if cy - self.mAB*cx > self.cAB else False


# detector.py
#
# module for class that contains detector parameters
#
# Author: Arvinder Palaha

class detector(object):

    def __init__(self,
        c = 1408, r = 1484, cc = 8, cr = 7,
        ):

        self.nCol       = c
        self.nRow       = r
        self.nColCal    = cc
        self.nRowCal    = cr

        self.fullWellDiode  = 2.64e4
        self.fullWellC0     = 3.56e5
        self.fullWellC1     = 5.27e6
        self.fullWellC2     = 1.42e7

        self.diodeStartVoltage      = 2.
        self.diodeThresholdVoltage  = 0.25

        self.gains  = [1,2,4,8]

        # Oc = 0, Gc = 1, Oct = 2**8-1, Gct = 2**8,
        # Of = 0, Gf = 1, Oft = 0,      Gft = 1

        # self.coarseOffset = Oc
        # self.coarseGain = Gc
        # self.fineOffset = Of
        # self.fineGain = Gf

        # self.coarseOffsetTarget = Oct
        # self.coarseGainTarget = Gct
        # self.fineOffsetTarget = Oft
        # self.fineGainTarget = Gft

    def e2vin(self,nElec):

        vIn     = 0.
        vThres  = self.diodeThresholdVoltage
        vStart  = self.diodeStartVoltage
        vRange  = abs(vStart - vThres)

        fwD     = self.fullWellDiode
        fwC0    = self.fullWellC0 - self.fullWellDiode
        fwC1    = self.fullWellC1 - self.fullWellC0
        fwC2    = self.fullWellC2 - self.fullWellC1

        if nElec <= self.fullWellDiode:

            countedElec = nElec
            vIn = vStart - (vRange * (countedElec/fwD))# + vThres

        elif nElec <= self.fullWellC0:

            countedElec = nElec-self.fullWellDiode
            vIn = vStart - (vRange * (countedElec/fwC0))# + vThres

        elif nElec <= self.fullWellC1:

            countedElec = nElec-self.fullWellC0
            vIn = vStart - (vRange * (countedElec/fwC1))# + vThres

        elif nElec <= self.fullWellC2:

            countedElec = nElec-self.fullWellC1
            vIn = vStart - (vRange * (countedElec/fwC2))# + vThres

        else: # more electrons than full well of C2, saturated signal
            vIn = vThres

        return vIn

    def e2gain(self,nElec):
        if nElec <= self.fullWellDiode:
            return self.gains[0]
        elif nElec <= self.fullWellC0:
            return self.gains[1]
        elif nElec <= self.fullWellC1:
            return self.gains[2]
        else:
            return self.gains[3]

    #___________________________________________________________________________
    # methods to create frames will go here for now, but they will be in 
    # another module in the future

    #___________________________________________________________________________
    # methods to process frames will go here for now, but they will be in
    # another module in the future
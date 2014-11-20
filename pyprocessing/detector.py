# detector.py
#
# module for class that contains detector parameters
#
# Author: Arvinder Palaha


class detector(object):

    #___________________________________________________________________________
    def __init__(self,
        c = 1408, r = 1484, cc = 8, cr = 7,
        ):

        # settable parameters
        self.nCol       = c
        self.nRow       = r
        self.nColCal    = cc
        self.nRowCal    = cr

        self.cumuFullWellDiode  = 2.64e4
        self.cumuFullWellC0     = 3.56e5
        self.cumuFullWellC1     = 5.27e6
        self.cumuFullWellC2     = 1.42e7

        self.StartVoltage  = 2.
        self.SwitchVoltage = 0.25

        self.gains  = [1,2,4,8]

        # calculated parameters
        self.fullWellDiode  = self.cumuFullWellDiode
        self.fullWellC0     = self.cumuFullWellC0 - self.cumuFullWellDiode
        self.fullWellC1     = self.cumuFullWellC1 - self.cumuFullWellC0
        self.fullWellC2     = self.cumuFullWellC2 - self.cumuFullWellC1

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

    #___________________________________________________________________________
    def e2vin(self,nElec):

        vIn     = 0.
        vSwitch = self.SwitchVoltage
        vStart  = self.StartVoltage
        vRange  = abs(vStart - vSwitch)

        fwD     = self.fullWellDiode
        fwC0    = self.fullWellC0
        fwC1    = self.fullWellC1
        fwC2    = self.fullWellC2

        if nElec <= self.cumuFullWellDiode:

            countedElec = nElec
            vIn = vStart - (vRange * (countedElec/fwD))# + vThres

        elif nElec <= self.cumuFullWellC0:

            countedElec = nElec-self.cumuFullWellDiode
            vIn = vStart - (vRange * (countedElec/fwC0))# + vThres

        elif nElec <= self.cumuFullWellC1:

            countedElec = nElec-self.cumuFullWellC0
            vIn = vStart - (vRange * (countedElec/fwC1))# + vThres

        elif nElec <= self.cumuFullWellC2:

            countedElec = nElec-self.cumuFullWellC1
            vIn = vStart - (vRange * (countedElec/fwC2))# + vThres

        else: # more electrons than full well of C2, saturated signal
            vIn = vSwitch

        return vIn

    #___________________________________________________________________________
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
    def e2ADUcoarse(self,nElec):
        raise NotImplementedError
        leastSignificantBit = self.StartVoltage/31.
        vIn = self.e2vin(nElec)
        ADUc = 0


    #___________________________________________________________________________
    # methods to create frames will go here for now, but they will be in 
    # another module in the future

    #___________________________________________________________________________
    # methods to process frames will go here for now, but they will be in
    # another module in the future
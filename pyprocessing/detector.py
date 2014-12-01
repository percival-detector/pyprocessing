# detector.py
#
# module for class that contains detector parameters
#
# Author: Arvinder Palaha

import numpy as np

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

        self.startVoltage   = [2. for x in range(4)]
        self.switchVoltage  = [0.25 for x in range(4)]
        self.dbRefVoltage   = 0.25

        self.nCoarseBits        = 5
        self.nFineBits          = 7
        self.nFineOverRangeBits = 1

        self.nADC   = 7

        self.gains  = [1,2,4,8]

        # calculated parameters
        self.fullWellDiode  = self.cumuFullWellDiode
        self.fullWellC0     = self.cumuFullWellC0 - self.cumuFullWellDiode
        self.fullWellC1     = self.cumuFullWellC1 - self.cumuFullWellC0
        self.fullWellC2     = self.cumuFullWellC2 - self.cumuFullWellC1

        self.fineGainTarget     = (2**self.nFineBits-1)/(2./(2**self.nCoarseBits-1))
        self.fineOffsetTarget   = 0
        self.coarseGainTarget   = -2./(2**self.nCoarseBits-1)
        self.coarseOffsetTarget = 2**self.nCoarseBits-1

        self.adcFineGain        = [(2**self.nFineBits-1)/(2./(2**self.nCoarseBits-1))]*self.nADC
        self.adcFineOffset      = [0]*self.nADC
        self.adcCoarseGain      = [-2./(self.nCoarseBits-1)]*self.nADC
        self.adcCoarseOffset    = [2**self.nCoarseBits-1]*self.nADC
        self.adcVThreshold      = [2.]*self.nADC
        self.adcCoarseStep      = [(x/self.coarseOffsetTarget) for x in self.adcVThreshold]

    #___________________________________________________________________________
    def e2capaV(self,nElec):
        capaV = self.startVoltage[:]
        
        while nElec:

            if capaV[0] > self.switchVoltage[0]:
                if nElec <= self.fullWellDiode:
                    capaV[0] -= (nElec/self.fullWellDiode)*(self.startVoltage[0]-self.switchVoltage[0])
                    nElec -= nElec
                else:
                    capaV[0] = self.switchVoltage[0]
                    nElec -= self.fullWellDiode
            
            elif capaV[1] > self.switchVoltage[1]:
                if nElec <= self.fullWellC0:
                    capaV[1] -= nElec*(self.startVoltage[1]-self.switchVoltage[1])/self.fullWellC0
                    nElec -= nElec
                else:
                    capaV[1] = self.switchVoltage[1]
                    nElec -= self.fullWellC0
            
            elif capaV[2] > self.switchVoltage[2]:
                if nElec <= self.fullWellC1:
                    capaV[2] -= nElec*(self.startVoltage[2]-self.switchVoltage[2])/self.fullWellC1
                    nElec -= nElec
                else:
                    capaV[2] = self.switchVoltage[2]
                    nElec -= self.fullWellC1
            
            elif capaV[3] > self.switchVoltage[3]:
                if nElec <= self.fullWellC2:
                    capaV[3] -= nElec*(self.startVoltage[3]-self.switchVoltage[3])/self.fullWellC2
                    nElec -= nElec
                else:
                    capaV[3] = self.switchVoltage[3]
                    nElec = 0 # saturation
            else:
                pass
            # print nElec, capaV
        
        return capaV

    #___________________________________________________________________________
    def capaV2vInGain(self,capaV):
        # which diode/capacitor to use? Smallest one with V>VdbRef (==Vswitch)
        vIn = 0
        capaNum = 0

        if capaV[0] > self.dbRefVoltage:
            vIn = capaV[0]
        elif capaV[1] > self.dbRefVoltage:
            vIn = capaV[1]
            capaNum = 1
        elif capaV[2] > self.dbRefVoltage:
            vIn = capaV[2]
            capaNum = 2
        else:
            vIn = capaV[3]
            capaNum = 3

        return vIn, capaNum

    #___________________________________________________________________________
    def vIn2ADUCode(self,vIn,capaNum,ADCNum=0):

        # now I have vIn, I need number of coarse steps, then fine steps
        # for coarse, I need:
        #   diode voltage -> capaV[n]
        #   size of coarse step -> coarseGain
        #   where to start -> -coarseOffset
        # for fine, I need:
        #   diode voltage after coarse count -> capaV[n] + coarseADU*coarseStep
        #   size of fine step -> fineGain
        #   where to start -> fineOffset

        nCoarseSteps = (self.adcVThreshold[ADCNum]-vIn)/self.coarseStep[ADCNum]
        coarseCode = np.ceil(nCoarseSteps)
        vOvershoot = (coarseCode - nCoarseSteps)*self.coarseStep[ADCNum]

        return 0

    # #___________________________________________________________________________
    # def e2vin(self,nElec):

    #     vIn     = 0.
    #     vSwitch = self.SwitchVoltage
    #     vStart  = self.StartVoltage
    #     vRange  = abs(vStart - vSwitch)

    #     fwD     = self.fullWellDiode
    #     fwC0    = self.fullWellC0
    #     fwC1    = self.fullWellC1
    #     fwC2    = self.fullWellC2

    #     if nElec <= self.cumuFullWellDiode:

    #         countedElec = nElec
    #         vIn = vStart - (vRange * (countedElec/fwD))# + vThres

    #     elif nElec <= self.cumuFullWellC0:

    #         countedElec = nElec-self.cumuFullWellDiode
    #         vIn = vStart - (vRange * (countedElec/fwC0))# + vThres

    #     elif nElec <= self.cumuFullWellC1:

    #         countedElec = nElec-self.cumuFullWellC0
    #         vIn = vStart - (vRange * (countedElec/fwC1))# + vThres

    #     elif nElec <= self.cumuFullWellC2:

    #         countedElec = nElec-self.cumuFullWellC1
    #         vIn = vStart - (vRange * (countedElec/fwC2))# + vThres

    #     else: # more electrons than full well of C2, saturated signal
    #         vIn = vSwitch

    #     return vIn

    # #___________________________________________________________________________
    # def e2gain(self,nElec):
    #     if nElec <= self.fullWellDiode:
    #         return self.gains[0]
    #     elif nElec <= self.fullWellC0:
    #         return self.gains[1]
    #     elif nElec <= self.fullWellC1:
    #         return self.gains[2]
    #     else:
    #         return self.gains[3]

    # #___________________________________________________________________________
    # def e2ADUcoarse(self,nElec):
    #     raise NotImplementedError
    #     leastSignificantBit = self.StartVoltage/31.
    #     vIn = self.e2vin(nElec)
    #     ADUc = 0


    #___________________________________________________________________________
    # methods to create frames will go here for now, but they will be in 
    # another module in the future

    #___________________________________________________________________________
    # methods to process frames will go here for now, but they will be in
    # another module in the future
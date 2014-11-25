#!/usr/bin/python
#!/dls_sw/prod/tools/RHEL6-x86_64/defaults/bin/dls-python
# testharness.py
#
# Author: Arvinder Palaha

# from pkg_resources import require
# require("numpy")

# import numpy as np
# import h5py

#   open/create file for test image datasets
#   check for datasets
#       if they don't exist, create them
#       if they do exist, read them
#           images for p2m and p13m
#           sample image with flat/ramp/noise
#           all sample images with asymmetric triangle shape
#           all sample images with four slices of different gain
#           conversion between digital and analogue
#           include calibration pixels (to be left empty)
#           all reset images w/ small values: mid-range of fine ADC w/ noise


import unittest
from pyprocessing.detector import detector


class CreatingFrames(unittest.TestCase):

#_______________________________________________________________________________
    def test_detector_has_default_parameters(self):
        
        detObj = detector()
        
        # settable parameters
        columns             = detObj.nCol
        rows                = detObj.nRow
        calibrationcolumns  = detObj.nColCal
        calibrationrows     = detObj.nRowCal
        
        self.assertEqual(1408,  columns)
        self.assertEqual(1484,  rows)
        self.assertEqual(8,     calibrationcolumns)
        self.assertEqual(7,     calibrationrows)

        cumuFullWellDiode   = detObj.cumuFullWellDiode
        cumuFullWellC0      = detObj.cumuFullWellC0
        cumuFullWellC1      = detObj.cumuFullWellC1
        cumuFullWellC2      = detObj.cumuFullWellC2

        self.assertEqual(2.64e4,cumuFullWellDiode)
        self.assertEqual(3.56e5,cumuFullWellC0)
        self.assertEqual(5.27e6,cumuFullWellC1)
        self.assertEqual(1.42e7,cumuFullWellC2)

        startVoltage    = detObj.startVoltage
        switchVoltage   = detObj.switchVoltage
        dbRefVoltage    = detObj.dbRefVoltage

        self.assertEqual([2,2,2,2],             startVoltage)
        self.assertEqual([.25,.25,.25,0.25],    switchVoltage)
        self.assertEqual(0.25,                  dbRefVoltage)

        gains = detObj.gains
        self.assertEqual(gains,[1,2,4,8])

        ncb     = detObj.nCoarseBits
        nfb     = detObj.nFineBits
        nforb   = detObj.nFineOverRangeBits

        self.assertEqual(ncb,   5)
        self.assertEqual(nfb,   7)
        self.assertEqual(nforb, 1)

        # calculated parameters
        fullWellDiode   = detObj.fullWellDiode 
        fullWellC0      = detObj.fullWellC0 
        fullWellC1      = detObj.fullWellC1
        fullWellC2      = detObj.fullWellC2

        self.assertEqual(2.64e4,fullWellDiode)
        self.assertEqual(3.56e5-2.64e4,fullWellC0)
        self.assertEqual(5.27e6-3.56e5,fullWellC1)
        self.assertEqual(1.42e7-5.27e6,fullWellC2)

        fgt = detObj.fineGainTarget
        fot = detObj.fineOffsetTarget
        cgt = detObj.coarseGainTarget
        cot = detObj.coarseOffsetTarget

        self.assertEqual(fgt, (2**nfb-1)/(2./(2**ncb-1)))
        self.assertEqual(fot, 0)
        self.assertEqual(cgt, -2./(2**ncb-1))
        self.assertEqual(cot, 2**ncb-1)

        fineGains       = detObj.adcFineGain
        fineOffsets     = detObj.adcFineOffset
        coarseGains     = detObj.adcCoarseGain
        coarseOffsets   = detObj.adcCoarseOffset

        self.assertTrue(len(fineGains)==len(fineOffsets)==len(coarseGains)==len(coarseOffsets)==7)


#_______________________________________________________________________________
    def test_arguments_passsed(self):

        detObj = detector(100,200,5,10)
        
        columns             = detObj.nCol
        rows                = detObj.nRow
        calibrationcolumns  = detObj.nColCal
        calibrationrows     = detObj.nRowCal
        
        self.assertEqual(100,   columns)
        self.assertEqual(200,   rows)
        self.assertEqual(5,     calibrationcolumns)
        self.assertEqual(10,    calibrationrows)

#_______________________________________________________________________________
    def test_convert_number_of_electrons_to_capaV(self):
        detObj = detector()

        startV  = detObj.startVoltage
        switchV = detObj.switchVoltage

        capaV = detObj.e2capaV(0)
        self.assertEqual(len(capaV),4)
        self.assertEqual(capaV,detObj.startVoltage)

        capaV = detObj.e2capaV(detObj.cumuFullWellDiode)
        self.assertTrue(capaV[0]<=detObj.switchVoltage[0])
        self.assertEqual(capaV[1],detObj.startVoltage[1])

        capaV = detObj.e2capaV(detObj.cumuFullWellDiode+100)
        self.assertEqual(capaV[0],detObj.switchVoltage[0])
        self.assertTrue(capaV[1]<detObj.startVoltage[1])

        capaV = detObj.e2capaV(detObj.cumuFullWellC1)
        self.assertEqual(capaV[1],detObj.switchVoltage[1]) # filled
        self.assertEqual(capaV[2],detObj.switchVoltage[2])
        self.assertEqual(capaV[3],detObj.startVoltage[3])

        capaV = detObj.e2capaV(detObj.cumuFullWellC2+1000)
        self.assertEqual(capaV,detObj.switchVoltage)

        capaV = detObj.e2capaV(0.5*detObj.cumuFullWellC2)
        self.assertEqual(capaV[2],detObj.switchVoltage[2])
        self.assertTrue(
            detObj.startVoltage[3]>capaV[3]>detObj.switchVoltage[3]
            )

#_______________________________________________________________________________
    def test_capaV_to_vIn_and_gain(self):
        detObj = detector()

        capaV = detObj.e2capaV(0) # zero electrons, capaV = startvoltage
        aduCode = detObj.capaV2adu(capaV)
        self.assertIsInstance(aduCode,int)
        self.assertLessEqual(aduCode,2**12-1)
        self.assertGreaterEqual(aduCode,0)


# #_______________________________________________________________________________
#     def test_convert_number_of_electrons_to_Vin(self):

#         detObj  = detector()

#         startV  = detObj.startVoltage
#         switchV = detObj.switchVoltage
        
#         self.assertEqual(startV,    0) # no signal, no change in diode voltage
#         self.assertEqual(switchV,   detObj.cumuFullWellDiode)
#         self.assertEqual(switchV,   detObj.cumuFullWellC0)
#         self.assertEqual(switchV,   detObj.cumuFullWellC1) # limit before switch
#         self.assertEqual(0,         detObj.cumuFullWellC2) # use 2v range
#         self.assertEqual(0,         detObj.cumuFullWellC2+1000) # saturation 
#         nElecs = [
#             detObj.cumuFullWellDiode-100,
#             detObj.cumuFullWellC0-100,
#             detObj.cumuFullWellC1-100,
#             detObj.cumuFullWellC2-100
#         ]

#         # for nElec in nElecs:
#         voltageIn = detObj.e2vin(nElecs[0])
#         self.assertTrue(
#             voltageIn       >= detObj.SwitchVoltage # 0.25
#             and voltageIn   <= detObj.StartVoltage) # 2.0
#         voltageIn = detObj.e2vin(nElecs[1])
#         self.assertTrue(
#             voltageIn       >= detObj.SwitchVoltage # 0.25
#             and voltageIn   <= detObj.StartVoltage) # 2.0
#         voltageIn = detObj.e2vin(nElecs[2])
#         self.assertTrue(
#             voltageIn       >= detObj.SwitchVoltage # 0.25
#             and voltageIn   <= detObj.StartVoltage) # 2.0
#         voltageIn = detObj.e2vin(nElecs[3])
#         self.assertTrue(
#             voltageIn       >= detObj.SwitchVoltage # 0.25
#             and voltageIn   <= detObj.StartVoltage) # 2.0

#         # zero electrons should give start voltage
#         voltageIn = detObj.e2vin(0)
#         self.assertEqual(detObj.StartVoltage,voltageIn)

#         # full well diode number of electrons should give Switch voltage
#         voltageIn = detObj.e2vin(detObj.cumuFullWellDiode)
#         self.assertEqual(detObj.SwitchVoltage,voltageIn)
#         voltageIn = detObj.e2vin(detObj.cumuFullWellC0)
#         self.assertEqual(detObj.SwitchVoltage,voltageIn)
#         voltageIn = detObj.e2vin(detObj.cumuFullWellC1)
#         self.assertEqual(detObj.SwitchVoltage,voltageIn)
#         voltageIn = detObj.e2vin(detObj.cumuFullWellC2)
#         self.assertEqual(detObj.SwitchVoltage,voltageIn)

#         # more than complete full well number of electrons should still give
#         # voltage for largest signal (vSwitch)
#         voltageIn = detObj.e2vin(detObj.cumuFullWellC2+1000)
#         self.assertEqual(detObj.SwitchVoltage,voltageIn)

# #_______________________________________________________________________________
#     def test_get_gain_from_number_of_electrons(self):

#         detObj = detector()
#         gains = detObj.gains

#         # no signal
#         gain = detObj.e2gain(0)
#         self.assertEqual(gain,gains[0])
#         # full well limits of diode/capacitors
#         gain = detObj.e2gain(detObj.fullWellDiode)
#         self.assertEqual(gain,gains[0])
#         gain = detObj.e2gain(detObj.fullWellC0)
#         self.assertEqual(gain,gains[1])
#         gain = detObj.e2gain(detObj.fullWellC1)
#         self.assertEqual(gain,gains[2])
#         gain = detObj.e2gain(detObj.fullWellC2)
#         self.assertEqual(gain,gains[3])
#         # saturated signal
#         gain = detObj.e2gain(detObj.fullWellC2+1000)
#         self.assertEqual(gain,gains[3])
#         # negative signal (?)
#         gain = detObj.e2gain(-1000)
#         self.assertEqual(gain,gains[0])

# #_______________________________________________________________________________
#     def test_electron_to_ADU_coarse_code(self):

#         detObj = detector()

#         # zero electrons should give ADU coarse code of 31
#         self.assertEqual(31,detObj.e2ADUcoarse(0))

#     # def test_change_detector_size(self):
#     #     detObj = detector()



if __name__ == '__main__':
    unittest.main(verbosity=2)
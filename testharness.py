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
        
        columns             = detObj.nCol
        rows                = detObj.nRow
        calibrationcolumns  = detObj.nColCal
        calibrationrows     = detObj.nRowCal
        
        self.assertEqual(1408,  columns)
        self.assertEqual(1484,  rows)
        self.assertEqual(8,     calibrationcolumns)
        self.assertEqual(7,     calibrationrows)

        fullWellDiode   = detObj.fullWellDiode
        fullWellC0      = detObj.fullWellC0
        fullWellC1      = detObj.fullWellC1
        fullWellC2      = detObj.fullWellC2

        self.assertEqual(2.64e4,fullWellDiode)
        self.assertEqual(3.56e5,fullWellC0)
        self.assertEqual(5.27e6,fullWellC1)
        self.assertEqual(1.42e7,fullWellC2)

        diodeStartVoltage       = detObj.diodeStartVoltage
        diodeThresholdVoltage   = detObj.diodeThresholdVoltage

        self.assertEqual(2,     diodeStartVoltage)
        self.assertEqual(0.25,  diodeThresholdVoltage)

        gains = detObj.gains
        self.assertEqual(gains,[1,2,4,8])

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
    def test_convert_number_of_electrons_to_Vin(self):

        detObj = detector()

        nElecs = [
            detObj.fullWellDiode-100,
            detObj.fullWellC0-100,
            detObj.fullWellC1-100,
            detObj.fullWellC2-100
        ]

        # for nElec in nElecs:
        voltageIn = detObj.e2vin(nElecs[0])
        self.assertTrue(
            voltageIn       >= detObj.diodeThresholdVoltage # 0.25
            and voltageIn   <= detObj.diodeStartVoltage)    # 2.0
        voltageIn = detObj.e2vin(nElecs[1])
        self.assertTrue(
            voltageIn       >= detObj.diodeThresholdVoltage # 0.25
            and voltageIn   <= detObj.diodeStartVoltage)    # 2.0
        voltageIn = detObj.e2vin(nElecs[2])
        self.assertTrue(
            voltageIn       >= detObj.diodeThresholdVoltage # 0.25
            and voltageIn   <= detObj.diodeStartVoltage)    # 2.0
        voltageIn = detObj.e2vin(nElecs[3])
        self.assertTrue(
            voltageIn       >= detObj.diodeThresholdVoltage # 0.25
            and voltageIn   <= detObj.diodeStartVoltage)    # 2.0

        # zero electrons should give start voltage
        voltageIn = detObj.e2vin(0)
        self.assertEqual(detObj.diodeStartVoltage,voltageIn)

        # full well diode number of electrons should give threshold voltage
        voltageIn = detObj.e2vin(detObj.fullWellDiode)
        self.assertEqual(detObj.diodeThresholdVoltage,voltageIn)
        voltageIn = detObj.e2vin(detObj.fullWellC0)
        self.assertEqual(detObj.diodeThresholdVoltage,voltageIn)
        voltageIn = detObj.e2vin(detObj.fullWellC1)
        self.assertEqual(detObj.diodeThresholdVoltage,voltageIn)
        voltageIn = detObj.e2vin(detObj.fullWellC2)
        self.assertEqual(detObj.diodeThresholdVoltage,voltageIn)

        # more than complete full well number of electrons should still give
        # voltage for largest signal (vThreshold)
        voltageIn = detObj.e2vin(detObj.fullWellC2+1000)
        self.assertEqual(detObj.diodeThresholdVoltage,voltageIn)

#_______________________________________________________________________________
    def test_get_gain_from_number_of_electrons(self):

        detObj = detector()
        gains = detObj.gains

        # no signal
        gain = detObj.e2gain(0)
        self.assertEqual(gain,gains[0])
        # full well limits of diode/capacitors
        gain = detObj.e2gain(detObj.fullWellDiode)
        self.assertEqual(gain,gains[0])
        gain = detObj.e2gain(detObj.fullWellC0)
        self.assertEqual(gain,gains[1])
        gain = detObj.e2gain(detObj.fullWellC1)
        self.assertEqual(gain,gains[2])
        gain = detObj.e2gain(detObj.fullWellC2)
        self.assertEqual(gain,gains[3])
        # saturated signal
        gain = detObj.e2gain(detObj.fullWellC2+1000)
        self.assertEqual(gain,gains[3])
        # negative signal (?)
        gain = detObj.e2gain(-1000)
        self.assertEqual(gain,gains[0])




    # def test_change_detector_size(self):
    #     detObj = detector()



if __name__ == '__main__':
    unittest.main()
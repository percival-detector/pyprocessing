# -*- coding: utf-8 -*-
"""
my own functions
"""
#%% imports

import math
import time # to have time
import struct # to unpack byte into int
import numpy # to have arrays (matlab-like operations)
import scipy
import pylab # to transform list in arrays
import matplotlib
import sys #command line argument values 
import h5py # deal with HDF5

'''
to remember:
pylab.concatenate((a,b), axis=0)
pylab.concatenate((a,b), axis=1)
'''



#%% my own generic function
#
''' byte (uint8) => list of 8 bits '''
def my_byte2bits(byteIn):
    ''' byte (uint8) => list of 8 bits '''
    bitArrayOut= [0] *8
    bitArray_str= list(bin(byteIn)[2:])
    for i_bit in range(len(bitArray_str)):
         bitArrayOut[i_bit] +=int(bitArray_str[-1-i_bit])
    return bitArrayOut
#
#
#
''' many bytes (uint8) => list of 8-bits '''
def my_ManyParallelByte2bits(byteListIn):
    ''' convert (byte => 8 bits) for many bits in parallel'''
    thisbitarray=numpy.zeros((len(byteListIn), 1)) # vertical array of 1 x 8 bits
    byteArray=numpy.array(byteListIn).reshape((len(byteListIn),1))
    #
    thisbitarray= byteArray%2
    bit8ArrayOut= numpy.copy(thisbitarray)
    #
    for iBits in range(1,8,1):
        byteArray= byteArray-thisbitarray
        byteArray=byteArray/2
        thisbitarray= byteArray%2
        bit8ArrayOut=numpy.concatenate((bit8ArrayOut,thisbitarray), axis=1)
    return bit8ArrayOut.tolist()
#
#
#    
#%% descrambling functions
#
'''data coming from FPGA is: 4 useless bytes, 80 useful, 4 useless byte, 80
useful ... for a total of 151200 bytes
this function deletes the useless'''
def my_overheadCutter(dataIn):
    '''TS1.0 descrambling: remove byte headers from byteStream'''
    dataOut= list(dataIn);    
    totalfilesize=151200;
    chunksize=84;
    chunksinafile=totalfilesize/chunksize;
        
    for i_chunk in range(chunksinafile-1,0-1,-1):
        chunkStart_index=  chunksize*i_chunk# this is the first index of chunk
        del dataOut[chunkStart_index: chunkStart_index+4]
    del i_chunk
    return dataOut
#
#
#
''' separate Sample from Reset images
% Sample Sample Reset Sample Reset Sample ... Reset Sample Reset Reset
% (30 reset & 30 sample)
% each group 2400 bit/channel, coupled in 160byte '''
def my_SRseparator(dataIn):
    '''TS1.0 descrambling: byteStream => Sample & Reset byteStreams'''
    groupsize=2400;
    groupsinanimage=30; # twice
    #
    dataOutSample= list([])
    dataOutReset= list([])
    myindex=0
    #
    dataOutSample += dataIn[myindex:myindex+groupsize]
    #
    myindex += groupsize;   
    for i_groups in range(0,groupsinanimage-1,1):
        dataOutSample += dataIn[myindex:myindex+groupsize]
        myindex += groupsize;
        #
        dataOutReset += dataIn[myindex:myindex+groupsize]
        myindex += groupsize;  
    del i_groups
    dataOutReset += dataIn[myindex:myindex+groupsize]
    #  
    return dataOutSample, dataOutReset
#
#
#
''' TS1.0 descrambling: ADC couple (Gain/Fine/Coarse) in a 8x20 group descrambled '''
def my_descrambleADCcouple_GoCoF(scrambledGroupStream, firstADCtodscr,secondADCtodscr, startingFrom, bits2descr):
#    ''' TS1.0 descrambling: ADC couple (Gain/Fine/Coarse) in a 8x20 group descrambled '''
#    localCount=numpy.ones((8,20)) *0 # zeros(8Rows,20Cols)
#    thisAddr=0
#    for iBit in range(bits2descr-1,-1,-1):      
#        for iCol in range(19,-1,-1):
#            localCount[firstADCtodscr][iCol] += (scrambledGroupStream[thisAddr+startingFrom])*(2**iBit)     
#            thisAddr += 1
#            localCount[secondADCtodscr][iCol] += (scrambledGroupStream[thisAddr+startingFrom])*(2**iBit)
#            thisAddr += 1
#    localList= localCount.tolist()
#    return localList
    #
    # made it parallel
    #
    localCount=numpy.zeros((8,20))
    bitMatrix= numpy.array(scrambledGroupStream[startingFrom:startingFrom+(2*20*bits2descr)]).reshape((bits2descr,40))
    totalVector=numpy.zeros(40)
    for iBit in range(bits2descr-1,-1,-1):
        totalVector+= (bitMatrix[bits2descr-iBit-1])*(2**iBit)
    totalVector= totalVector[::-1] # reverse the vector
    localCount[secondADCtodscr]=totalVector[0:40:2] # split ADC: 1st and 2nd are now reversed
    localCount[firstADCtodscr]=totalVector[1:40:2]  #
    localList= localCount.tolist()
    #
    return localList
#
#
#
''' TS1.0 descrambling: 1 Pad, 1Group (8x20): Gain/Fine/Coarse descrambled '''
def my_descramble1Group1Pad_GoCoF(scrambledGroupStream,startingFrom,bits2descr):
    ''' TS1.0 descrambling: 1 Pad, 1Group (8x20): Gain/Fine/Coarse descrambled (numpy array)'''
    localCount=numpy.ones((8,20)) *0 # zeros(8Rows,20Cols)
    
    firstADCtodscr= 2;  
    secondADCtodscr= 7;  
    localCount += my_descrambleADCcouple_GoCoF(scrambledGroupStream,firstADCtodscr,secondADCtodscr,startingFrom+0,bits2descr);
    firstADCtodscr= 1;  
    secondADCtodscr= 3;  
    localCount += my_descrambleADCcouple_GoCoF(scrambledGroupStream,firstADCtodscr,secondADCtodscr,startingFrom+600,bits2descr);
    firstADCtodscr= 4;  
    secondADCtodscr= 5;  
    localCount += my_descrambleADCcouple_GoCoF(scrambledGroupStream,firstADCtodscr,secondADCtodscr,startingFrom+1200,bits2descr);
    firstADCtodscr= 0;  #fake
    secondADCtodscr= 6;  
    localCount += my_descrambleADCcouple_GoCoF(scrambledGroupStream,firstADCtodscr,secondADCtodscr,startingFrom+1800,bits2descr);
    #
    return localCount
#
#
#
''' descrambleGroup Percival TS1'''
def my_descrambleGenericGroup(scrambledGroup, NCol, NRow, NADC):
    '''TS1.0 descrambling: scrambled group => descrambled group (numpy array)'''
    GainLength=2*40;
    FineLength=8*40;   
    Npad=8;
    
    myArray=pylab.array(scrambledGroup) # 2400Row, 8Col
    # print(len(myArray), len(myArray[0]))
    myArray= myArray.transpose() # 8 Row 2400Col myArray[i]= 2400 elements
    #print(len(myArray), len(myArray[0])) # at this point, myArray[i]= PADi 
    my2Dlist= myArray.tolist()
    #print(len(my2Dlist), len(my2Dlist[0])) # back to list
    
    # coarse
    startingFrom= GainLength+FineLength;
    AllPadsTransposedList=[]
    for i_PAD in range(Npad):
        myVector=my2Dlist[i_PAD]
        descrambledCoarseGroupThisPad= my_descramble1Group1Pad_GoCoF(myVector, startingFrom,5)
        descrambledCoarseGroupThisPad= numpy.delete(descrambledCoarseGroupThisPad,0,0); # del descrambledCoarseGroupThisPad[0] (1st row)
        # print(len(descrambledCoarseGroupThisPad), len(descrambledCoarseGroupThisPad[0]))
        if (i_PAD==0):
            descrambledCoarseGroupArr=numpy.copy(descrambledCoarseGroupThisPad)
        else:
            descrambledCoarseGroupArr=numpy.concatenate((descrambledCoarseGroupArr,descrambledCoarseGroupThisPad),axis=1) # add parallel columns
    #
    # fine
    startingFrom= GainLength;
    AllPadsTransposedList=[]
    for i_PAD in range(Npad):
        myVector=my2Dlist[i_PAD]
        descrambledFineGroupThisPad= my_descramble1Group1Pad_GoCoF(myVector, startingFrom,8)
        descrambledFineGroupThisPad= numpy.delete(descrambledFineGroupThisPad,0,0) # del descrambled...GroupThisPad[0] (1st row)
        # print(len(descrambledCoarseGroupThisPad), len(descrambledCoarseGroupThisPad[0]))
        if (i_PAD==0):
            descrambledFineGroupArr=numpy.copy(descrambledFineGroupThisPad)
        else:
            descrambledFineGroupArr= numpy.concatenate((descrambledFineGroupArr,descrambledFineGroupThisPad),axis=1) # add parallel columns
    #   
    # Gain
    startingFrom= 0;
    AllPadsTransposedList=[]
    for i_PAD in range(Npad):     
        myVector=my2Dlist[i_PAD]
        descrambledGainGroupThisPad= my_descramble1Group1Pad_GoCoF(myVector, startingFrom,2)
        descrambledGainGroupThisPad= numpy.delete(descrambledGainGroupThisPad,0,0) # del descrambled...GroupThisPad[0] (1st row)
        # print(len(descrambledCoarseGroupThisPad), len(descrambledCoarseGroupThisPad[0]))
        if (i_PAD==0):
            descrambledGainGroupArr= numpy.copy(descrambledGainGroupThisPad)
        else:
            descrambledGainGroupArr= numpy.concatenate((descrambledGainGroupArr,descrambledGainGroupThisPad),axis=1) # add parallel columns
    #
    return descrambledGainGroupArr, descrambledCoarseGroupArr, descrambledFineGroupArr
#
#
#
''' descrambleImage Percival TS1'''
def my_descrambleImage(scrambledDataFlow, NCol, NRow, NADC):
    '''TS1.0 descrambling: scrambled image => descrambled image (numpy array)'''
    NGroup= NRow/NADC # 210/7=30
    bytesInGroup=2400;
    FineList= []
    CoarseList= []
    GainList= []
    #
    for iGroup in range(0, NGroup, 1):
        thisScrambledGroup= scrambledDataFlow[bytesInGroup*iGroup:bytesInGroup*(iGroup+1)];
        #print("from {} to {}".format( bytesInGroup*iGroup, bytesInGroup*(iGroup+1)))
        (ThisGain,ThisCoarse,ThisFine)= my_descrambleGenericGroup(thisScrambledGroup, NCol, NRow, NADC)
        #
        if (iGroup==0):
            GainArr= numpy.copy(ThisGain)
            CoarseArr= numpy.copy(ThisCoarse)
            FineArr= numpy.copy(ThisFine)
        else:
            GainArr= numpy.concatenate((GainArr,ThisGain))
            CoarseArr= numpy.concatenate((CoarseArr,ThisCoarse))
            FineArr= numpy.concatenate((FineArr,ThisFine))
            #
    return GainArr,CoarseArr,FineArr
# 
#
#
''' descrambleFile Percival TS1'''
def my_descrambleFile(fileNameAndPath):
    '''TS1.0 descrambling: file => descrambled image (numpy array)'''
    NCol=160; NRow=210; NADC=7;
    thisfile= open(fileNameAndPath, 'rb')
    fileContent=thisfile.read()
    thisfile.close()
    #
    byteList= list(struct.unpack_from(str('B'*(len(fileContent))),fileContent[0:len(fileContent)])) # to list of int
    byteList=my_overheadCutter(byteList) # take out headers
    ScrambledSample, ScrambledReset= my_SRseparator(byteList)
    #
    BittedSample=my_ManyParallelByte2bits(ScrambledSample)
    BittedReset=my_ManyParallelByte2bits(ScrambledReset)
    #
    (GainSampleArr,CoarseSampleArr,FineSampleArr)= my_descrambleImage(BittedSample, NCol, NRow, NADC)
    (GainResetArr,CoarseResetArr,FineResetArr)= my_descrambleImage(BittedReset, NCol, NRow, NADC)
    #
    return GainSampleArr,CoarseSampleArr,FineSampleArr,GainResetArr,CoarseResetArr,FineResetArr
    #
#
#
#
#%% calibration functions
#
''' TS1.0 calibration: .h5 ADCcalib filepath,prefix => 4x numpy arrays (Crs/Fn, gain/offset)'''
def my_prepADCcalib_CrsFn(ADCcalibFilePath,ADCcalibFilePrefix,NGroup):
    ''' TS1.0 calibration: .h5 ADCcalib filepath,prefix => 4x numpy arrays (Crs/Fn, gain/offset)
    prefix is file name without _Coarse/Fine Gain/Offset Array.h5
    '''
    #
    # load data from h5
    ADCcalibFile_CoarseGain= ADCcalibFilePath + ADCcalibFilePrefix + '_CoarseGainArray.h5'
    ADCcalibFile_CoarseOffset= ADCcalibFilePath + ADCcalibFilePrefix + '_CoarseOffsetArray.h5'
    ADCcalibFile_FineGain= ADCcalibFilePath + ADCcalibFilePrefix + '_FineGainArray.h5'
    ADCcalibFile_FineOffset= ADCcalibFilePath + ADCcalibFilePrefix + '_FineOffsetArray.h5'
    #
    my5hfile= h5py.File(ADCcalibFile_CoarseGain, 'r')
    myh5dataset=my5hfile['/data/data/']
    my5hfile.close
    ADCcalib_CoarseGain_160x7Array= numpy.array(myh5dataset)
    #
    my5hfile= h5py.File(ADCcalibFile_CoarseOffset, 'r')
    myh5dataset=my5hfile['/data/data/']
    my5hfile.close
    ADCcalib_CoarseOffset_160x7Array= numpy.array(myh5dataset)
    #
    my5hfile= h5py.File(ADCcalibFile_FineGain, 'r')
    myh5dataset=my5hfile['/data/data/']
    my5hfile.close
    ADCcalib_FineGain_160x7Array= numpy.array(myh5dataset)
    #
    my5hfile= h5py.File(ADCcalibFile_FineOffset, 'r')
    myh5dataset=my5hfile['/data/data/']
    my5hfile.close
    ADCcalib_FineOffset_160x7Array= numpy.array(myh5dataset)
    #
    ADCcalibArr_CoarseGain= pylab.copy(ADCcalib_CoarseGain_160x7Array)
    ADCcalibArr_CoarseOffset= pylab.copy(ADCcalib_CoarseOffset_160x7Array)
    ADCcalibArr_FineGain= pylab.copy(ADCcalib_FineGain_160x7Array)
    ADCcalibArr_FineOffset= pylab.copy(ADCcalib_FineOffset_160x7Array)
    for iGroup in range(NGroup-1):
        # -1 because there is already a copy of it
        ADCcalibArr_CoarseGain= pylab.concatenate((ADCcalibArr_CoarseGain, ADCcalib_CoarseGain_160x7Array))
        ADCcalibArr_CoarseOffset= pylab.concatenate((ADCcalibArr_CoarseOffset, ADCcalib_CoarseOffset_160x7Array))
        ADCcalibArr_FineGain= pylab.concatenate((ADCcalibArr_FineGain, ADCcalib_FineGain_160x7Array))
        ADCcalibArr_FineOffset= pylab.concatenate((ADCcalibArr_FineOffset, ADCcalib_FineOffset_160x7Array))
    #
    return ADCcalibArr_CoarseGain, ADCcalibArr_CoarseOffset, ADCcalibArr_FineGain, ADCcalibArr_FineOffset
#
#
#
''' TS1.0 calibration: combine Coarse and Fine in a number; ignore Gain'''
def my_ADCcorr_NoGain(coarse,fine, coarseGain, coarseOffset, fineGain, fineOffset, NRow, NCol):
    ''' TS1.0 calibration: combine Coarse and Fine in numpy array image (ignore Gain)'''
    #
    idealOffset = numpy.zeros((NRow, NCol)) + (128.0 * 32.0);
    idealSlope  = (idealOffset / 1.5); # mapped over over 1.5V Vin span
    #
    overallADU = (fineGain / coarseGain) * (coarse +1.0)- (fine - fineOffset);
    normalizedADU = coarseOffset * (fineGain/coarseGain) - overallADU;
    normalizedADU = ( idealSlope / fineGain ) * normalizedADU;
    normalizedADU = idealOffset - normalizedADU;
    return (normalizedADU);
#
#
#
''' TS1.0 calibration: pedestal subtraction'''
def my_PedestalSubtract_NoGain(ArrayIn, PedSubFile):
    ''' TS1.0 calibration: pedestal subtraction (assume Gain=0)'''
    my5hfile= h5py.File(PedSubFile, 'r')
    myh5dataset=my5hfile['/data/data/']
    my5hfile.close
    PedSubArray= numpy.array(myh5dataset)
    #
    ArrayOut= ArrayIn-PedSubArray
    return ArrayOut
#
#
#
''' TS1.0 calibration: convert from ADU to e'''
def my_ADU2e_NoGain(ArrayIn, ADU2eFile):
    ''' TS1.0 calibration: convert from ADU to e (assume Gain=0)'''
    my5hfile= h5py.File(ADU2eFile, 'r')
    myh5dataset=my5hfile['/data/data/']
    my5hfile.close
    ADU2eArray= numpy.array(myh5dataset)
    #
    ArrayOut= ArrayIn * ADU2eArray
    return ArrayOut
#
#
#
#%% evaluation functions
#
#''' TS1.0 calibration: assume (Gain=0) in all images: avg, rmserr, peroprt it for quadrant '''
#def my_stats_NoGain(coarse,fine, coarseGain, coarseOffset, fineGain, fineOffset, NRow, NCol):





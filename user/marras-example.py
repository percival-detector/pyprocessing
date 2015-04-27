# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-
"""
MAIN TO BE PROFILED
"""
#
#%% imports
#
import math
import time # to have time
import struct # to unpack byte into int
import numpy # to have arrays (matlab-like operations)
import scipy
import pylab # to transform list in arrays
import matplotlib
import sys #command line argument values 
import h5py # deal with HDF5
import os # list files in a folder
import sys # print w/o newline

import cProfile
#
import TS1v0funs # my own functions
#
#%% main here
def main():
    #%% define generals
    #
    print("------------------------------")
    #
    timeId=time.strftime("%Y_%m_%d__%H:%M:%S")
    print("script beginning at "+timeId)
    print("--  --  --  --  --  --  --  --  ")
    #
    NCol=160
    NRow=210
    NGroup=30
    #
    #%% define paths here#
    #
    mainFolderDefault='E:/marras/PERCIVAL/PercivalPython/'
    print('I need the main folder path (the one where the archive/ and data/ subforlder stem from)')
    print('give me the main folder path (ending with /)')
    print('no path will be interpreted as my own default ({})'.format(mainFolderDefault))
    try:
        mainFolder= input('main folder path>>>')
    except SyntaxError:
        mainFolder = None
    if mainFolder is None:
        mainFolder= mainFolderDefault
    print('main folder path: {}'.format(mainFolder))
    print("--  --  --  --  --  --  --  --  ")
    #
    #
    ADCcalibFolder=mainFolder+'archive/ADCcalib/' #ADCcalibFolder='E:/marras/PERCIVAL/PercivalPython/archive/ADCcalib/'
    ADCcalibFilePrefix='ADC_tr6_W22_33_TS1BSI_PerB4V2_T+02_10j05_2015-03-25_13-52'
    print("will take ADC calibration parameters from: \n" + ADCcalibFolder + "\n" + ADCcalibFilePrefix + " _ Coarse/Fine Gain/Offset Array.h5" )
    #
    PedSubFolder=mainFolder+'archive/PedSub/' #PedSubFolder='E:/marras/PERCIVAL/PercivalPython/archive/PedSub/'
    PedSubFileName='auxil_NOpedestal.h5'
    PedSubFile=PedSubFolder+PedSubFileName
    print("will take pedestal parameters from: \n" + PedSubFolder + "\n" + PedSubFileName )
    #
    ADU2eFolder=mainFolder+'archive/ADU2e/' #ADU2eFolder='E:/marras/PERCIVAL/PercivalPython/archive/ADU2e/'
    ADU2eFileName='prelim_W22_33TS1BSI_PerB4V2_+35C_10j04_2015-03-08_11-36_perQuad_ADU2e.h5'
    ADU2eFile= ADU2eFolder+ADU2eFileName
    print("will take ADU=>e parameters from: \n" + ADU2eFolder + "\n" + ADU2eFileName )
    #
    folder2read=mainFolder+'data/2015_03_13__08_18_58_0to9/' #folder2read='E:/marras/PERCIVAL/PercivalPython/data/2015_03_13__08_18_58_0to9/'
    expectedFileSuffix='.data'
    print("will take image data from \n"+folder2read)
    #
    folder2write=mainFolder+'archive/auxil/'
    print("will save results into \n"+folder2write)
    print("--  --  --  --  --  --  --  --  ")
    #%% load data from h5
    (ADCcal_CrsG, ADCcal_CrsO, ADCcal_FnG, ADCcal_FnO)=TS1v0funs.my_prepADCcalib_CrsFn(ADCcalibFolder,ADCcalibFilePrefix,NGroup)
    #
    #%% list files in folder, select the ones with the right suffix, sicard images _0 and _1    
    allFileNameList=os.listdir(folder2read)
    dataFileNameList=[]
    for thisFile in allFileNameList:
        if (thisFile.endswith(expectedFileSuffix) and not(thisFile.endswith('_0.data') or thisFile.endswith('_1.data')) ):
            dataFileNameList.append(thisFile)
    del thisFile
    del allFileNameList
    NImage=len(dataFileNameList)
    print("{} meaningful data files found in the folder".format(NImage))
    #
    #%%  create Godzilla 3D Array
    SampleImageAlldata=numpy.ndarray((NImage,NRow,NCol))
    SampleImageAlldata.fill(0.0)
    SampleGainAlldata=numpy.ndarray((NImage,NRow,NCol))
    SampleGainAlldata.fill(0.0)
    ResetImageAlldata=numpy.ndarray((NImage,NRow,NCol))
    ResetImageAlldata.fill(0.0)
    #
    #%%  cycle through files
    print("processing files:")
    thisImage=0;
    for thisFile in dataFileNameList:
        ThisFileNamePath=folder2read+thisFile
        (SampleG,SampleC,SampleF,ResetG,ResetC,ResetF)= TS1v0funs.my_descrambleFile(ThisFileNamePath)
        SampleGainAlldata[thisImage,:,:]=numpy.copy(SampleG)
        SampleImageAlldata[thisImage,:,:]=numpy.copy(TS1v0funs.my_ADCcorr_NoGain(SampleC,SampleF , ADCcal_CrsG, ADCcal_CrsO, ADCcal_FnG, ADCcal_FnO, NRow, NCol))
        ResetImageAlldata[thisImage,:,:]=numpy.copy(TS1v0funs.my_ADCcorr_NoGain(ResetC,ResetF , ADCcal_CrsG, ADCcal_CrsO, ADCcal_FnG, ADCcal_FnO, NRow, NCol))
        #
        thisImage +=1
        sys.stdout.write(".")
        if (thisImage%20 ==0):
            print("{}".format(thisImage))
        #
    #%%  assume Gain=0 for all images: CDS, avg, pedestal-subtract, rms
    CDSImageAlldata= SampleImageAlldata[1:len(ResetImageAlldata)]- ResetImageAlldata[0:len(ResetImageAlldata)-1] # CDS= Sample[i]-Reset[i-1]
    myAVG=numpy.average(CDSImageAlldata, axis=0)                    #CDS, avg [ADU]
    myAVG= TS1v0funs.my_PedestalSubtract_NoGain(myAVG, PedSubFile)  #CDS, avg, PedSub [ADU]
    myRMSerr=numpy.std(CDSImageAlldata, axis=0)                     #CDS, rmserr [ADU]
    #    
    myAVG= TS1v0funs.my_ADU2e_NoGain(myAVG, ADU2eFile)              #CDS, avg, PedSub [e]
    myRMSerr= TS1v0funs.my_ADU2e_NoGain(myRMSerr, ADU2eFile)        #CDS, rmserr [e]
    #
    #%%  show it
    pylab.figure
    matplotlib.pyplot.figure(figsize=(12,6.4))
    matplotlib.pyplot.imshow(myAVG.tolist()); pylab.xlabel('col'); pylab.ylabel('row');  pylab.title('avg, pedestal-subtracted CDS [e]'); pylab.colorbar(); pylab.gca().invert_xaxis()
    #
    pylab.figure
    matplotlib.pyplot.figure(figsize=(12,6.4))
    matplotlib.pyplot.imshow(myRMSerr.tolist()); pylab.xlabel('col'); pylab.ylabel('row');  pylab.title('rms CDS [e]'); pylab.colorbar(); pylab.gca().invert_xaxis()
    #
    print("--  --  --  --  --  --  --  --  ")
    #
    #%% save as csv
    #
    outFileNamePath_avg=folder2write + 'avgExample.csv'
    outFileNamePath_rmserr=folder2write + 'avgExample.csv'
    #
    numpy.savetxt(outFileNamePath_avg,myAVG,fmt='%d',delimiter=',') 
    numpy.savetxt(outFileNamePath_rmserr,myRMSerr,fmt='%d',delimiter=',') 
    #
    print("avg, rms data saved in  \n"+outFileNamePath_avg + "\n" + outFileNamePath_rmserr)
    #
    #%% that's all folks
    #
    print("done")
    print("------------------------------")
    print("------------------------------")
    print("------------------------------")
# end of main
#
#
#%% profile it for timing optiization
#
#cProfile.run("main()")
#%% now run it    
main()
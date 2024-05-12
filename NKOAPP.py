#!/usr/bin/env python3
import ctypes
import sys
import os 
import numpy as np
from numpy import random
from math import sqrt
from scipy.stats import norm
import random 
import json
from NKOAPP_scripts import splineInterpolatorAk,splineInterpolatorAkSegmenter,glotInterpolator, dataAdder, targetNames, congealer, arithmetic_progression
from NKOAPP_JSON_Reader import glotValues, tractValues, brownian, rightDimTract
from NKOAPP_f0andIntensityExtractor import f0andIntensityReaderA,f0andIntensityReaderB
from datetime import datetime
# from tract2audio import vtlLibraryLoader
#_________________________________________________________________
# STARTUP CODE # 
# load up the speakerJD2.JSON file which has all the glottis geometries and tract values for all the utterances
with open('speakerJD2.json', 'r') as f:
  data = json.load(f)

#to get the current working directory
directory = os.getcwd()
directory = directory.replace(os.sep, '/') 

#_________________________________________________________________

glGeomOptions = {'GM':['Geometric glottis',11], '2M':['Two-mass model',6], 'TRI': ['Triangular glottis',6]}
#!# Choose the glottis/vocal tract model.
glChoice = glGeomOptions['GM']

gl = glotValues(data=data) # dictionary with all glottis modes
tr = tractValues(data=data) # dictionary with all the tract values for each utterance a,e,i+consonants etc..

#!# choose if we want to manually generate the tractSequence or use the f0 and intensity values from the praat script
manual = True # True: Goto Section A / False: Goto Section B
f0andIntFileName = directory + '/f0andIntensity/f0andInt_45e.txt' # put here the filename // if this gives an error, the file is not in the root directory 

#_________________________________________________________________
#!# Section A:

# OPTION A1:
  #custom input for glottis and tract targets (glOption,trOption) and the durations between them 
    # The amount of entries in glOption and trOption has to be greater than 3, and should always be of an uneven size N
    # The amount of entries in durModulation is: (N-1)/2
# #example (comment this out when working in this section) 
glOption = ['modGM', 'pressedGM','hrseGM','modGM','modGM','hrse2GM','modGM', 'modGM','modGM'] 
trOption = ['o','i','postalvlatI','u-raw','uvufricA','a','palfricA','a','i']
durModulation = [200,200,300,400] # in total 400ms

# # add your own values between '' for glOption, trOption and add durModulation (ms) (comment this out when working in this section)
# glOption = ['','',''] 
# trOption = ['','','']
# durModulation = [] # in milliseconds

# comment this out if you want to allow for the other options to work
targetsInfo = targetNames(gl=gl,tr=tr,glotModes=glOption, tractConfigs=trOption)

# OPTION A2: 
  #generate random interpolations between a set of chosen glottis and tract targets (glOption, trOption), and random durations
    # The amount of entries in glOption and trOption has to be greater than 3, and should always be of an uneven size N
    # The amount of entries in durModulation is: (N-1)/2
# # example (comment this out when working in this section)
# glOption = ['modGM', 'pressedGM','hrseGM','modGM','modGM','hrse2GM','modGM', 'modGM','modGM'] 
# trOption = ['o','i','postalvlatI','u-raw','uvufricA','a','palfricA','a','i']
# choose amount of total interpolations between targets(both for glottis as for vocal tract) 
# numA2 = 20
# durModulation = np.random.randint(200,800,int((numA2 - 1) / 2)) # in ms

# # add your own values between '' for glOption, trOption and add durModulation (ms) (comment this out when working in this section)
# glOption = ['','',''] 
# trOption = ['','','']
# choose amount of total interpolations between targets(both for glottis as for vocal tract) 
# numA2 = 100
# durModulation = np.random.randint(10,3000,int((numA2 - 1) / 2)) # in ms

# comment this out if you want to allow for the other options to work
# targetsInfo = targetNames(gl=gl,tr=tr,glotModes=random.choices(glOption,k=numA2), tractConfigs=random.choices(trOption, k=numA2))

# (do not comment this out)
if(manual==True):
  #. if const=True f0 and Intensity will be constant (100Hz at 17000Pa)
  fileName = 'Manual.txt'
  totalDurFact = 1 # make the total length longer by a factor
  sumDurModulation = sum(durModulation)*(44100/110000)*totalDurFact
  f0andIntArrEnd = f0andIntensityReaderB(totalAmFrames= int(sumDurModulation),f0=100,intensity=17000)
  totalNumFrames = len(f0andIntArrEnd)

#_________________________________________________________________
#!# Section B: 
#.
if (manual == False):
  fileName = f0andIntFileName # put here the filename of the .txt-file // if this gives an error, the file is not in the root directory
  with open(fileName, 'r') as f:
    f0data = f.readlines()
  #. if const=False f0 and Intensity are taken from the praat script
  f0andIntArrEnd = f0andIntensityReaderA(data=f0data)   
  #. if const is True, the length of the amount of synthesis blocks has to be updated (1 block = 2.5ms)
  totalNumFrames = len(f0andIntArrEnd)

# OPTION B1:
  # custom input of glottis and tract parameters, with f0 and intensity values from praat script
    # The amount of entries in glOption and trOption have to be greater than 3, and should always be of an uneven size N
    # The amount of entries in durModulation is: (N-1)/2. !! The values represent fractions of the length of the analysed audio file 
      # so if the recording is 10s long, and durModulation = [10,5,10], this means the first interpolation takes 4s (0.4*10), the second 2s (0.2*10) and the third also 4s 
# example (comment this out when working in this section)
# glOption = ['modGM', 'pressedGM','hrseGM','modGM','modGM','hrse2GM','modGM'] 
# trOption = ['o','i','postalvlatI','u-raw','uvufricA','a','palfricA']
# durModulation = [10,5,10]

# # add your own values between '' for glOption, trOption and add durModulation (fraction) (comment this out when working in this section)
# glOption = ['','',''] 
# trOption = ['','','']
# durModulation = [] # as fractions (normalizedSum)

# comment this out if you want to allow for Section A to work
# targetsInfo = targetNames(gl=gl,tr=tr,glotModes=glOption, tractConfigs=trOption)

# OPTION B2: 
  #generate random interpolations between a set of chosen glottis and tract targets (glOption, trOption), and random durations
    # The amount of entries in glOption and trOption has to be greater than 3, and should always be of an uneven size N
    # The amount of entries in durModulation is: (N-1)/2
# example (comment this out when working in this section)
# glOption = ['modGM', 'pressedGM','hrseGM','modGM','modGM','hrse2GM','modGM', 'modGM','modGM'] 
# trOption = ['o','i','postalvlatI','u-raw','uvufricA','a','palfricA','a','i']
# choose amount of total interpolations between targets(both for glottis as for vocal tract) 
# numB2 = 100
# durModulation = np.random.randint(10,3000,int((numB2 - 1) / 2)) # in ms

# # add your own values between '' for glOption, trOption and add durModulation (ms) (comment this out when working in this section)
# glOption = ['','',''] 
# trOption = ['','','']
# choose amount of total interpolations between targets(both for glottis as for vocal tract) 
# numB2 = 20
# durModulation = np.random.randint(10,3000,int((numB2 - 1) / 2)) # in ms


# comment this out if you want to allow for the other options to work
# targetsInfo = targetNames(gl=gl,tr=tr,glotModes=random.choices(glOption,k=numB2), tractConfigs=random.choices(trOption, k=numB2))
#_________________________________________________________________

glTargets = targetsInfo[0]
trTargets = targetsInfo[1]
glModes = targetsInfo[2]
trConfigs = targetsInfo[3]
num = len(glTargets)

#_________________________________________________________________
#!# GlOBAL DURATIONS MODIFICATIONS 
#. Change the durations between targets by proportioning the segments in different ways
valT = int((num - 1) / 2) # do not change

#--- long->short [::1] or slow-fast[::-1]
# durModulationG = arithmetic_progression(1,valT)[::1] #[::-1] 

#--- raising exponent of durations
durModulationExp = []
exponent = 1 # exponent > 1:shorter durations will be slower compared to longer durations and < 1 the opposite
for durInd, durVal in enumerate(durModulation):
  durModulationExp.append(durVal**exponent)
#_________________________________________________________________

# !ignore Important duration-2-frames conversion for tractSequence .txt-file
numStates = []
for stateInd, stateDur in enumerate(durModulationExp):
  numStates.append(int((stateDur/(110*1000))*44100))
# !ignore f0 and Intensity: normalize the sum so it will fit the amount of frames that the praat file contains
numStates = (numStates / np.linalg.norm(numStates, ord=1))*totalNumFrames
# !ignore typecast the array
numStates = numStates.astype(int) 
# !ignore now due to rounding errors we'll have to adjust the totalNumFrames to the sum of the segmented numStates arr. Maybe resulting ignoring some frames at the end of the f0 file
totalNumFrames = sum(numStates)

#_________________________________________________________________

# !ignore write the beginning of the tractSequence .txt file
fullString = dataAdder(beginString= '\n\n\n\n\n\n', numStates=totalNumFrames,glottisType=glChoice[0])

#_________________________________________________________________


#. Time discrete derivative of the splines - because it's a cubic polynomial, the max deriv=2 | so 3 options [0,1,2]: 0=no deriv, 1=1st deriv, 2=2nd deriv
derivativeGlot = 0
derivativeTract = 0

#. Uniform distribution factor to randomize the glottis parameters
devL = 1 # lower boundary for random number generation
devH = 1  # upper boundary for random number generation

#_________________________________________________________________

#.A Input the targets in the cubic interpolation functions
  #. Tract value generator   
toBeParsedTract = splineInterpolatorAk(vec=trTargets, amArticulators=19, interpList=numStates,derivative=derivativeTract)
toBeParsedTract = splineInterpolatorAkSegmenter(interpolatedArr=toBeParsedTract)
  # Glottis value generator   
toBeParsedGl = glotInterpolator(f0andIntArr=f0andIntArrEnd,vec=glTargets,amGlottisParams=len(glTargets[0]), interpNum=totalNumFrames, derivative=derivativeGlot, devL=devL,devH=devH)


#.B Or randomize the vocal tract shapes and glottis parameters

#. Vocal tract shapes: Brownian Interpolation between targets
    # randomTract: choose brownian interpolation

# delta = 0.5  # The Wiener process parameter.
# T = 4 # Total time.
# N = int(totalNumFrames) # Number of steps.
# dt = T/N # Time step size, watch out for too high N, or too low dt (possible overflow)
# tractParamAm = 19 Number of realizations to generate.
# x = np.empty((tractParamAm,N+1)) Create an empty array to store the realizations.
# x[:, 0] = 0 # Initial values of x
# brownianSeqTract = brownian(x[:,0], N, dt, delta, out=x[:,1:])
# toBeParsedTract =  rightDimTract(brownianSeqTract) # reshape the brownianSeqTract array

#. Glottis values: Brownian Interpolation between targets
    # randomGlottis: choose brownian interpolation

# glotParamAm = glChoice[1]
# y = np.empty((glotParamAm,N+1)) # Create an empty array to store the realizations.
# y[:, 0] = 0.4 # Initial values of x
# brownianSeqGl = brownian(y[:,0], N, dt, delta, out=y[:,1:])
# toBeParsedGl = rightDimTract(brownianSeqGl) # reshape the brownianSeqGl array

#_________________________________________________________________


# Congeal all the glottis and vocal tract parameters
fullString = fullString + congealer(toBeParsedGl,toBeParsedTract)
# Get the current time
current_time = datetime.now()
# Format the current time as a string
time_string = current_time.strftime("%Y-%m-%d_%H-%M-%S")

# FIND THE TRACT SEQUENCE FILE in the /TractSequence folder
tractFileName = directory + '/TractSequences/'+'{}'.format(time_string)+'_TractSequence'+'_ConstPressureAndf0_{}_'.format(glChoice[0]) +'n{}_'.format(num)+'normalDist{}'.format([devL,devH])+'_{}'.format([derivativeGlot,derivativeTract])+'_{}'.format(fileName)
# wavFileName = directory + '/Samples/'+'{}'.format(time_string)+'_TractSequence'+'_ConstPressureAndf0_{}_'.format(glChoice[0]) +'n{}_'.format(num)+'normalDist{}'.format([devL,devH])+'_{}'.format([derivativeGlot,derivativeTract])+'_{}'.format(fileName)+'.wav'
print(tractFileName)
f = open(tractFileName, 'w')
f.write(fullString)

# 1. Then open VTL
# 2. Choose the same glottis model as glChoice (see above): Synthesis models > Vocal folds model > Choose one of the three > then click on 'Use selected model for synthesis'
# 3. Then load the tractSequence file to audio: Synthesis from file > Tract sequence file to audio > Find the \TractSequences\ directory and choose the rendered txt-file
# 4. This can take long if the tractSequence file is more than 10s. Ignore the "The Program is not responding", it's just rendering





# IGNORE IGNORE IGNORE IGNORE IGNORE IGNORE IGNORE IGNORE #
# ------------------------------------------------------- #
# # # write it to a wav file
# # # to get the current working directory
# # directory = os.getcwd()
# # directory = directory.replace(os.sep, '/')
# # VTL = vtlLibraryLoader('E:/2021-2022/Documents/Praktischestuff/Sonology/2022-2023/Research Bach/Patches/VTL/VTLbackEnd/VocalTractLabBackend-dev/lib/Debug/VocalTractLabApi.dll')
# # # initialize vtl
# # speaker_file_name = ctypes.c_char_p('C:/Users/larry/AppData/Local/Programs/Python/Python310/Lib/site-packages/VocalTractLab/src/vocaltractlab-backend/JD3.speaker'.encode())
# # failure = VTL.vtlInitialize(speaker_file_name)
# # if failure != 0:
# #     raise ValueError('Error in vtlInitialize! Errorcode: %i' % failure)


# # # choose pathdirectories to tract sequence and wav file 
# # tract_sequence_file_name = ctypes.c_char_p((tractFileName).encode())
# # wav_file_name = ctypes.c_char_p((wavFileName).encode())


# # print("VTL.vtlTractSequenceToAudio...")
# # failure = VTL.vtlTractSequenceToAudio(tract_sequence_file_name, wav_file_name, None, None)
# # if failure != 0:
# #     raise ValueError('Error in vtlTractSequenceToAudio! Errorcode: %i' % failure)

# # failure = VTL.vtlClose()
# # if failure != 0:
# #     raise ValueError('Error in vtlClose! Errorcode: %i' % failure)

# # print('Finished.')


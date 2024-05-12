#!/usr/bin/env python3
import ctypes
import sys
import os 

def vtlLibraryLoader(path=''):
    VTL = ctypes.cdll.LoadLibrary(path)
    return VTL


#to get the current working directory
directory = os.getcwd()
directory = directory.replace(os.sep, '/')

# load vocaltractlab binary
VTL = ctypes.cdll.LoadLibrary("E:/2021-2022/Documents/Praktischestuff/Sonology/2022-2023/Research Bach/Patches/VTL/VTLbackEnd/VocalTractLabBackend-dev/lib/Debug/VocalTractLabApi.dll")

# get version / compile date
version = ctypes.c_char_p(b' ' * 64)
VTL.vtlGetVersion(version)
print('Compile date of the library: "%s"' % version.value.decode())

# initialize vtl
speaker_file_name = ctypes.c_char_p('C:/Users/larry/AppData/Local/Programs/Python/Python310/Lib/site-packages/VocalTractLab/src/vocaltractlab-backend/JD3.speaker'.encode())

failure = VTL.vtlInitialize(speaker_file_name)
if failure != 0:
    raise ValueError('Error in vtlInitialize! Errorcode: %i' % failure)


tract_sequence_file_name = ctypes.c_char_p((directory+'/TractSequences/2024-05-13_00-30-59_TractSequence_ConstPressureAndf0_Geometric glottis_n9_normalDist[1.0, 1.0]_[0, 0]_Manual.txt').encode())
wav_file_name = ctypes.c_char_p((directory+'/Samples/aaaa_f0231hz_InvariantsChangedGM.wav').encode())


print("VTL.vtlTractSequenceToAudio...")
failure = VTL.vtlTractSequenceToAudio(tract_sequence_file_name, wav_file_name, None, None)
if failure != 0:
    raise ValueError('Error in vtlTractSequenceToAudio! Errorcode: %i' % failure)

failure = VTL.vtlClose()
if failure != 0:
    raise ValueError('Error in vtlClose! Errorcode: %i' % failure)

print('Finished.')

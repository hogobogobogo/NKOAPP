import numpy as np
import pandas as pd
import random as rd
from numpy import random
import json
from scipy.interpolate import interp1d


def f0andIntensityReaderA(data):
	f0andIntArr = []
	# randVal= rd.choices([25,50,75,100,150,225,300,375],k=1)[0]
	for index, value in enumerate(data):	
		val1='' # for f0
		val2='' # for Intensity
		arr = []
		replacedVal = value.replace('\n',' ')
		count = 0
		for charInd, charVal in enumerate(replacedVal):
			if ord(charVal) != 32 and count == 0:
				val1 = val1 + charVal
			elif ord(charVal) != 32 and count == 1:
				val2 = val2 + charVal
			elif ord(charVal) == 32 and count == 0:
				count = 1
			# elif ord(charVal) == 32 and count == 1:
			else:	
				arr = [val1,val2]

		if val2 != '--undefined--':
			val2 = (float(val2)/100)*20000
			# print(val2)

		if val2 == '--undefined--':
			if index < 1:
				val2 = 1.0
			else: 
				val2 = (float(f0andIntArr[len(f0andIntArr)-1][1]))*0.7
				# print(val2)


		if val1 == -300.000 or val1 == '--undefined--':
			if index < 1:
				val1 = 100.0
			else: 
				val1 = (float(f0andIntArr[len(f0andIntArr)-1][0]))	
		
		# clip the values for both f0 and intensity
		val1 = max(1.0,float(val1))
		val2 = max(1.0, float(val2))
		# print([val1,val2])
		f0andIntArr.append([val1,val2]);
	return(f0andIntArr)

def f0andIntensityReaderB(totalAmFrames, f0, intensity):
	f0andIntArr = []
	for index in range(totalAmFrames):
		riseFrames = 3;
		if index < riseFrames:
			f0andIntArr.append([f0,(intensity/riseFrames)*index]);
		else:
			f0andIntArr.append([f0, intensity]);
			# 'hello'

	return(f0andIntArr)


# print(f0andIntensityReaderB(totalAmFrames=20,f0=100,intensity=17000))
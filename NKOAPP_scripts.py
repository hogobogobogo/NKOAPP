import numpy as np 
from numpy import random
import scipy
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.nonparametric.kernel_regression import KernelReg


a = [0.1667, -3.9392, 0, -4.1498 ,0.0718, 0.9937, 0.8, -0.1, 0.1524, -1.8333, 4.2474, -1.694, 2.5488, -0.675, -2.8371, -2.9034, 0.2064, 0.0384, 0.1488]
i = [1,-5.5284, -0.075, -2.0808, 0.0771, 0.9251, 0, -0.1, 2.6045, -0.6805, 4.642, -0.8664, 4, 0.521, 0.0607, -0.8657, 0.2476, 0.0548, -0.05]
u = [1, -6, 0, -3.8826, 1, 0.3446, 0.5872, -0.1, 0.5154, -0.9786, 3.2438, -0.7467, 1.8387, 0.6311, -0.4071, -2.6017, 0.292, 0, 0]
ttpostalvclos_a = [0.2273 ,-4.6458, 0, -3.2692, 0.0718, 0.9937, 0.8, -0.1, 1.6893, -2.4763, 4.2988, 0.6946, 2.5389, 0.0119, -1.8289, -2.4763, 0.2064, 0.05, 0]
lllabclos_a = [0.2657,-5.0554, 0 ,-3.04, 0.0718, -0.1129, 0.8, -0.1, -0.1616, -2.2942, 4.2381, -1.3232, 2.5237, -0.4736, -2.3879, -3.1643, 0.2064, 0.0384, 0.1488]



# 1. function which duplicates items
def duplicateFunc(am =  20, val=0):
	arr = []
	string = ''
	for count in range(am):
		arr.append(val)
		string = string + '{} '.format(val)
	# return arr
	return string

# print(duplicateFunc(am=40, val=2))

# 2. what line in the tubesequence text file do you need to be when given the certain time in ms
def calcPosTxtFile(time=40):
	durOneFrame = 110*(1/44100)
	return 'go to line: {}'.format(time/durOneFrame)

# print(calcPosTxtFile(time=0.04))


# 2.1 write VTL tract parameters to Script readable format (CharToArray)

def charToArr(char='10.02 4.2 3.5'): 
	newChar  = char + ' '
	# print(newChar)
	arr = []
	tempArr =[]
	fullArr = []
	for index, value in enumerate(newChar):
		newVal = ord(value)
		if newVal == 32:
			arr.append(tempArr)
			tempArr = []
		else:
			# print(newVal)
			tempArr.append(newVal) 	
	# arr = chr(arr[0][0])

	for index, value in enumerate(arr):
		temp = ""
		for index2, value2 in enumerate(value):
			temp = temp + '{}'.format(chr(value2))
		fullArr.append(list(temp))
		# print(fullArr)
	
	bigTemp=[]
	for index, value in enumerate(fullArr):
		temp = ''  
		for item in value:
			temp = temp + '{}'.format(item)
		bigTemp.append(temp)

	out = []	
	for item in bigTemp:
		out.append(float(item))

	return out

# print(charToArr('0.846604 -5.29455 -0.0339041 -3.10914 0.0187849 0.26087 0.353995 -0.1 2.12247 -0.967413 4.38962 -1.1317 3.87142 0.0257301 -0.554286 -1.2662 0.253148 0.0349201 -0.017284'))  


# cubic interpolation: a)CubicSpline, b)Akima1DInterpolator

""" Do it on a 1d vector, 19 values"""
from scipy.interpolate import CubicSpline
from scipy.interpolate import Akima1DInterpolator
# so work with 

# x = np.linspace(0, 3, num=3)
# y = [i[0],a[0], u[0]]
# a) CubicSpline
# spl = CubicSpline(x, y)
# b) Akima1D
# spl =  Akima1DInterpolator(x,y)
# import matplotlib.pyplot as plt
# xnew = np.linspace(0, len(y), num=10)

# print(spl(xnew, ))
# plt.plot(x,y, '*', label='data')
# plt.plot(xnew, spl(xnew), '-', label='linear interp')
# plt.legend(loc= 'best')
# plt.show()

# 3. we can't choose the duration in between subtargets
def splineInterpolator(vec,amArticulators=19,interpNum=50, derivative=0):
	interpolatedArr = []
	amountTargets = len(vec)
	x = np.linspace(0, amountTargets, num=amountTargets)
	tempIndex =0
	for index in range(amArticulators): # don't do len(vec1) - 1
		y =[]
		for targetIndex in range(len(vec)):		
			y.append(vec[targetIndex][index])
			tempIndex = targetIndex
		spl = CubicSpline(x,y).derivative(nu=derivative) # or cubic interpol
		xnew = np.linspace(0,len(y), num = interpNum) # fix the piecewise amount of points in numInterps array
		interpolatedArr.append(np.round(spl(xnew),4))
		tempIndex = tempIndex + 1
	# 1 array met 19 nested arrays die elk een interpNum aantal waardes bevatten, have to round of to 4 decimals AND Transpose the matrix to fit the VTL tractSequence format
	return np.transpose(np.round(interpolatedArr,4))
	 
# so now we get a cubic interpolated series between the chosen phonemes
interpolatedSplines = splineInterpolator([a,i,u,a,i,u,i],amArticulators = 19,interpNum = 15, derivative=0)
# print(len(interpolatedSplines))

# 4. and we can work in terms of values of 3 targets. 
def splineInterpolatorAk(vec, amArticulators=19, interpList=[], derivative=0):
	# numInterps between each triplet or two targets ex. a->e->y
	numTargets =len(vec)
	numTriplets = int((numTargets - 1)/2)

	interpolatedArr = []
	x = np.linspace(0, 3, num=3)
	for index in range(numTriplets):
		for index2 in range(amArticulators):
			y = []
			for index3 in range(3):
				y.append(vec[index3+(index*2)][index2]) # choose articulator and add the targetvalues to the y array but after each triplet, shift two indexes 
			spl = Akima1DInterpolator(x,y).derivative(nu=derivative)
			xnew =  np.linspace(0, 3, num = interpList[index])
			interpolatedArr.append(np.round(spl(xnew),4))
	return interpolatedArr

splinee = splineInterpolatorAk(vec=[a,i,u,a,i,u,i],amArticulators=19,interpList=[5,5,5], derivative=0) # amout of numInterps inputs is (len(vec)-1) / 2; the amount of utterances has to > 3 and an uneven number

# 5. a function to split the array in even chunks of 19 
def splineInterpolatorAkSegmenter(interpolatedArr):
	arr = []
	length = int((len(interpolatedArr)/19))
	# print(length)
	for index in range(length):
		arr.append(np.transpose(interpolatedArr[19*index:19*(index+1)]))	
		# print(np.transpose(interpolatedArr[19*index:19*(index+1)]))
	conc = np.concatenate(arr[0:length])
	return conc 

segment = splineInterpolatorAkSegmenter(splinee)
# print(segment)


# 6. segmenter
def parser(segmentedArray, glottis = '101.594 8000 0.05 0.05 -0.25 1'):
	parsedArrString = ''
	for index, value in enumerate(segmentedArray):
		newVal = np.round(value,4)
		# print(newVal.flatten())
		# break
		length = len(newVal)
		# print(length)
		for index2, value2 in enumerate(newVal):
			# print'check {}'.format(value2)
			parsedArrString = parsedArrString + '{}'.format(glottis)+'\n' 
			for index3, value3 in enumerate(value2):
				parsedArrString = parsedArrString + '{} '.format(value3)
			parsedArrString = parsedArrString + '\n'
	return parsedArrString

# print(parser(segment))

# 7. interpolator between glottis types
modalGl = [101.594, 8000, 0.00495, 0.0004, 0, 1]
openGl = [101.594, 8000, 0.05, 0.05, -0.25, 1]
stopGl = [101.594, 8000, -0.03, -0.03, -0.25, 1]

def glotInterpolator(vec, amGlottisParams=6,interpNum=100, derivative=0, devL=1.0,devH=1.0, f0andIntArr =[[]], frameDifference=0):
	interpolatedArr = []
	amountTargets = len(vec)
	x = np.linspace(0, amountTargets, num=amountTargets)
	for index in range(amGlottisParams): # don't do len(vec1) - 1
		y =[]
		for targetIndex in range(len(vec)):		
			y.append(vec[targetIndex][index])
		spl = Akima1DInterpolator(x,y).derivative(nu=derivative) # or cubic interpol
		xnew = np.linspace(0,len(y), num = interpNum) # fix the piecewise amount of points in numInterps array
			# change values randomly by random factor
		fact = spl(xnew)
			# convert into pandas object to multiply -- see for loop
		s = pd.Series(fact)
		s = (s * (random.uniform(devL, devH))).tolist()

		# s[0] =  
		interpolatedArr.append(s)
	
	# replace f0 and subglottal pressure
	for interpIndex in range(len(interpolatedArr[0])-1):
		f0Value = f0andIntArr[interpIndex][0] 
		# print(f0Value)
		intValue = f0andIntArr[interpIndex][1]
		# print(intValue)
		interpolatedArr[0][interpIndex] = f0Value
		interpolatedArr[1][interpIndex] = intValue
		

	# # smooth out
	# lenf0Arr = len(interpolatedArr[0])
	# lenIntArr = len(interpolatedArr[1])
	# xf0 = np.linspace(0.0,1.0,lenf0Arr)
	# xInt = np.linspace(0.0,1.0,lenIntArr)

	# krf0 = KernelReg(interpolatedArr[0],xf0,'c')
	# krInt = KernelReg(interpolatedArr[1],xInt,'c')
	
	# f0_avg, f0_std = krf0.fit(xf0)
	# int_avg, int_std = krInt.fit(xInt)
	
	# interpolatedArr[0] = f0_avg
	# interpolatedArr[1] = int_avg 

	endArr =np.transpose(np.round(interpolatedArr,4))
	# 1 array met 19 nested arrays die elk een interpNum aantal waardes bevatten, have to round of to 4 decimals AND Transpose the matrix to fit the VTL tractSequence format
	# print(endArr)
	return endArr

# glotInterpolator(vec=[openGl,modalGl,openGl,stopGl],amGlottisParams=6, interpNum= 20, derivative=0, f0andIntArr=[[40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 200],[40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 200]])
# print([40.0]*20)

# 8. data adder for the txt file
def dataAdder(beginString='', numStates=1000,glottisType=''):
	add = beginString + glottisType + '\n' + '{}\n'.format(numStates)
	return add

# 9. now input the glottis and tract targets
def targetNames(gl,tr,glotModes=[],tractConfigs=[]):
	glotModesChar = ''
	tractConfigsChar = '' 
	glTargets = []
	trTargets = [] 
	for index, value in enumerate(glotModes):
		glTargets.append(gl[value])
		glotModesChar = glotModesChar + '{}'.format(value)
	for index, value in enumerate(tractConfigs):
		trTargets.append(tr[value])
		tractConfigsChar = tractConfigsChar + '{}'.format(value)
	return [glTargets,trTargets,glotModesChar, tractConfigsChar]

# 10. congealer function: adding 
def congealer(toBeParsedGl,toBeParsedTract):
	parsedArr = ''
	for index in range(len(toBeParsedTract)):
		for index2 in range(len(toBeParsedGl[index])):
			parsedArr = parsedArr + '{} '.format(toBeParsedGl[index][index2])
		parsedArr = parsedArr +'\n'
		for index2 in range(len(toBeParsedTract[index])):
			parsedArr = parsedArr + '{} '.format(toBeParsedTract[index][index2])
		parsedArr = parsedArr + '\n' 
	return parsedArr

# congealer(toBeParsedGl,toBeParsedTract)

# 11. arithmetic series generator

def arithmetic_progression(n, x):
  return list(range(n, x + 1, n))



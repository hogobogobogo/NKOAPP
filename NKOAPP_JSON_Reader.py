import json
from math import sqrt
from scipy.stats import norm
import numpy as np 
from numpy import random as rd

with open('speakerJD2.json', 'r') as f:
  data = json.load(f)

# values = print(list(data['speaker']['vocal_tract_model']['shapes']['shape'][0]['param'][0].values())[1])
# print(data['speaker']['vocal_tract_model']['shapes']['shape']) # 69 different positionings 
# print(len(data['speaker']['vocal_tract_model']['shapes']['shape'][0]['param'])) # 19 articulator parameters
# print(data['speaker']['vocal_tract_model']['shapes']['shape'][0]['_name']) # the respective name of one of the 69 

def utteranceList(data='',utterance= 0, articulator=0):
	tempDat = list(data['speaker']['vocal_tract_model']['shapes']['shape'][utterance]['param'][articulator].values())[1]
	nameUtterance = data['speaker']['vocal_tract_model']['shapes']['shape'][utterance]['_name']
	return [tempDat, nameUtterance]

# print(len(data['speaker']['vocal_tract_model']['shapes']['shape']))
def tractValues(data=''):
	fullData = []
	tractNames = []
	diction = {}
	for index in range(len(data['speaker']['vocal_tract_model']['shapes']['shape'])):
		tempDat = []
		tractNamesTemp = []
		for index2 in range(19):
			uttL = utteranceList(data=data, utterance=index, articulator=index2)
			tempDat.append(float(uttL[0]))
			tractNamesTemp.append(uttL[1])
		diction.update({tractNamesTemp[0] : tempDat}) #add(key=tractNamesTemp[0],value=tempDat)
		# add the the 19 values to the 'fulData' array and also the names of the utterances into tractNames
		fullData.append(tempDat)
		tractNames.append(tractNamesTemp)
	return diction#[fullData,tractNames]

# print(utteranceList(data, 0))
# diction  =  tractValues(data)
# print(diction)
# print(diction['a'])


def glotList(data='',glotGeom=0, glotMode=0, value=0):
	shared = data['speaker']['glottis_models']['glottis_model'][glotGeom]
	tempDat  = list(shared['shapes']['shape'][glotMode]['control_param'][value].values())[1] # there are 13 different glottisconfigs, modal-breathy-hoarsy 
	nameGlottisGeom =  shared['_type'] 
	namesGlottisMode =  shared['shapes']['shape'][glotMode]['_name']
	return [tempDat,namesGlottisMode]

# print(glotList(data=data, glotGeom=0, glotMode=0, value=2))

def glotValues(data=''):
	amGlotParams = [11,6,6]	
	amGlotModes = [13,4,8] # 13 for geometric glottis, 4 for two mass model, 8 for triangular model
	fullData = []
	glotGeomNames = []
	diction = {}
	for index in range(3):
		glotArr = []
		for index2 in range(amGlotModes[index]):
			glotValArr = []
			glotNameArr = []
			for index3 in range(amGlotParams[index]):
				uttL = glotList(data=data,glotGeom=index,glotMode=index2,value=index3)
				glotValArr.append(float(uttL[0]))
				glotNameArr.append(uttL[1])
			fullData.append(glotValArr)
			glotGeomNames.append(glotNameArr)
			diction.update({glotNameArr[0] : glotValArr})
	
	# output een dictionary 
	for index, value in enumerate(fullData):
		diction.update({glotGeomNames[index][0]:value})
	return diction


# print(glotValues(data=data)) # dit is geometric glottis, default mode (in totaal 24 modes over de drie glottis geometrien)

#pretty indentation
#for tract
# print(json.dumps(data=glotValues(data=data), indent = 0, sort_keys=False)) 

# for glottis
# print(json.dumps(data=tractValues(data=data), indent = 4, sort_keys=False))

# print(glotValues(data=data)['voiceless-plosiveGM'])




values = data['speaker']['vocal_tract_model']['anatomy']['param']
print(values)
def minmaxFunc(valueArr=[]):
  minmaxArr = []
  for index in range(len(valueArr)):
    val = valueArr[index]
    minmaxArr.append([val['_min'],val['_max']])
  return minmaxArr


def randMinMaxFloat(minmaxArr=[]):
  result = []
  for index in range(len(minmaxArr)):
    # print(minmaxArr[index][0])
    result.append(round(rd.uniform(float(minmaxArr[index][0]), float(minmaxArr[index][1])), 4))
  return result

minmaxArr = minmaxFunc(valueArr= values)
rangedRandVal =  randMinMaxFloat(minmaxArr=minmaxArr)
print(minmaxArr)


# ##########################################################
# ---------------------------------------------------------- 
# ##########################################################

"""
brownian() implements one dimensional Brownian motion (i.e. the Wiener process).
"""

# File: brownian.py



def brownian(x0, n, dt, delta, out=None, min=0.0,max=0.0, numFrames=2):
    """
    Generate an instance of Brownian motion (i.e. the Wiener process):

        X(t) = X(0) + N(0, delta**2 * t; 0, t)

    where N(a,b; t0, t1) is a normally distributed random variable with mean a and
    variance b.  The parameters t0 and t1 make explicit the statistical
    independence of N on different time intervals; that is, if [t0, t1) and
    [t2, t3) are disjoint intervals, then N(a, b; t0, t1) and N(a, b; t2, t3)
    are independent.
    
    Written as an iteration scheme,

        X(t + dt) = X(t) + N(0, delta**2 * dt; t, t+dt)


    If `x0` is an array (or array-like), each value in `x0` is treated as
    an initial condition, and the value returned is a numpy array with one
    more dimension than `x0`.

    Arguments
    ---------
    x0 : float or numpy array (or something that can be converted to a numpy array
         using numpy.asarray(x0)).
        The initial condition(s) (i.e. position(s)) of the Brownian motion.
    n : int
        The number of steps to take.
    dt : float
        The time step.
    delta : float
        delta determines the "speed" of the Brownian motion.  The random variable
        of the position at time t, X(t), has a normal distribution whose mean is
        the position at time t=0 and whose variance is delta**2*t.
    out : numpy array or None
        If `out` is not None, it specifies the array in which to put the
        result.  If `out` is None, a new numpy array is created and returned.

    Returns
    -------
    A numpy array of floats with shape `x0.shape + (n,)`.
    
    Note that the initial value `x0` is not included in the returned array.
    """
    for index in range(numFrames):  
      x0 = np.asarray(x0)

      # For each element of x0, generate a sample of n numbers from a
      # normal distribution.
      r = norm.rvs(size=x0.shape + (n,), scale=delta*sqrt(dt))

      # If `out` was not given, create an output array.
      if out is None:
          out = np.empty(r.shape)

      # This computes the Brownian motion by forming the cumulative sum of
      # the random samples. 
      np.cumsum(r, axis=-1, out=out)

      # Add the initial condition.
      out += np.expand_dims(x0, axis=-1)

    return out

def rightDimTract(brownianSeq=[]):
  amParams = len(brownianSeq)
  amStates = len(brownianSeq[0])
  brownianSeqFull = []
  # print('{}_'.format(amParams) + '{}'.format(amStates))
  for index in range(amStates):
    brownianSeqTemp = []
    for index2 in range(amParams): 
      if (index2 == 0 and (amParams== 11 or amParams== 6)):
      	brownianSeqTemp.append(90) # constant f0
      elif (index2 == 1 and (amParams== 11 or amParams== 6)):		
      	brownianSeqTemp.append(14000) # constant pressure
      else:
      	brownianSeqTemp.append(round(brownianSeq[index2][index], 6))
    brownianSeqFull.append(brownianSeqTemp)
  return brownianSeqFull

import time
import os
import timeit
import subprocess

## Time limit in seconds
timeLimit = 30

## Problem directory
instanceDir = "mini"

for filename in os.listdir('data_dzn/'+instanceDir+'/'):
	if filename.endswith(".dzn"): 
		os.system('timeout ' + str(timeLimit) + ' minizinc CPS.mzn data_dzn/' + instanceDir + '/' + filename + ' -a -s')


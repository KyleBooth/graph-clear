## Translate problem files to .dzn required format
## Author: Kyle E. C. Booth, kbooth@mie.utoronto.ca

import time
import os
import timeit
import subprocess
from subprocess import PIPE,Popen
import multiprocessing

## Problem directory
instanceDir = "mini"

for filename in os.listdir('data/'+instanceDir+'/'):
	if filename.endswith(".gcinput"): 

		output_string = []
		## 1. Read data from original file.
		fname = "data/"+instanceDir+"/"+filename
		content = []
		with open(fname) as f:
			for line in f:
				content.append(line.strip())

		T = content[0].split(",")[0]
		a = content[1].split(" ")
		for i in range(2, len(content)):
			if (i == 2):
				m_ = content[i].split(",")
			else:
				m_.extend(content[i].split(","))
		m = []
		for item in m_:
			m.append(item.split(" "))

		## 2. Output to .dzn file for MiniZinc
		f = open("data_dzn/"+instanceDir+"/"+filename.replace(".gcinput", "")+'.dzn', 'w')
		f.write('n='+T+';\n')
		f.write('a=[')
		for i in range(len(a)):
			if i < len(a)-1:
				f.write(a[i]+",")
			else:
				f.write(a[i])
		f.write('];\n')
		f.write('b=[')
		for i in range(len(m)):
			for item in m[i]:
				f.write(item+",")
		f.seek(-1, os.SEEK_END)
		f.write('];\n')
		f.close() 

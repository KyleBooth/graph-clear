## Graph-clear solution checker
## Author: Kyle E. C. Booth, kbooth@mie.utoronto.ca
import os
import re
import numpy as np

def partitionString(line, left):
	right = line.partition(left)[2].strip().replace("[","").replace("]","").replace(";","").replace(" ", "").split(",")
	return right

def parseInstanceFile(inst_dir, filename_instance):
	n = 0
	a = []
	b = []
	f = open(inst_dir+filename_instance)
	for line in f: 
		if "n=" in line:
			n = int(re.search('n=(\d+);', line).group(1)) 
		elif "a=" in line:
			a = partitionString(line, "a=")
			a = [int(x) for x in a]
		elif "b=" in line:
			b = partitionString(line, "b=")
			b = [int(x) for x in b]
	f.close()
	return n, a, b
		
def parseSolutionFile(sol_dir, filename_solution):
	robots = []
	sequence = [] 
	f = open(sol_dir+filename_solution)
	for line in f: 
		if "Robots:" in line:
			robots.append(int(re.search('Robots: (\d+);', line).group(1)))
			sequence.append(partitionString(line, "Sequence:"))
	robots = robots[-1]
	sequence = sequence[-1]
	f.close()
	return robots, sequence

def enforceAllDifferent(sequence):
	check = True
	if (len([x for x in sequence if sequence.count(x) > 1])):
		check = False
	return check

def enforceFleetSize(sequence, robots, n, a, b):
	check = True
	max_req = 0
	sequence = [int(x)-1 for x in sequence]
	for t in sequence:
		step_req = 0
		step_req = a[t] + np.array([b[(t)*n+i] for i in range(n)]).sum() \
			+ np.array([b[(t_)*n+j] for t_ in sequence[:sequence.index(t)] for j in range(n)]).sum() \
			- (np.array([b[(t_)*n+(t)] + np.array([b[(t_)*n+(t__)] for t__ in sequence[:sequence.index(t)] if t__ != t_]).sum() for t_ in sequence[:sequence.index(t)]]).sum())
		max_req = max(max_req, step_req)
	if (max_req > robots):
		check = False
	return check

if __name__ == '__main__':
	sol_dir = 'solutions/'
	mini_str = ["n5", "n6", "n7", "n8", "n9", "n10"]
	for filename_solution in os.listdir(sol_dir):
		if filename_solution.endswith(".sol"):
			filename_instance = filename_solution.replace(".sol",".dzn")
			if any(x in filename_instance for x in mini_str):
				inst_dir = "data_dzn/mini/"
			else:
				inst_size = int(re.search('yi_n(\d+)', filename_instance).group(1)) 
				inst_dir = "data_dzn/small/"+str(inst_size)+"/"
			n, a, b = parseInstanceFile(inst_dir, filename_instance)
			robots, sequence = parseSolutionFile(sol_dir, filename_solution)
			if enforceAllDifferent(sequence):
				if enforceFleetSize(sequence, robots, n, a, b):
					print filename_solution + " << FEASIBLE! >>"
				else:
					print filename_solution + " << INVALID >> (by fleet size)"
			else:
				print filename_solution + " << INVALID >> (by allDifferent)"
			
				
			
					
	

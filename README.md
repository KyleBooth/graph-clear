**Graph Clear:** MiniZinc Implementations  
**Author:** Kyle E. C. Booth (kbooth@mie.utoronto.ca)  
**Paper:** Morin et al (2018), "[Intruder Alert! Optimization Models for Solving the Mobile Robot Graph-Clear Problem](http://tidel.mie.utoronto.ca/pubs/GCP_Constraints_2018.pdf)", Constraints, Vol. 23 (3), 335-354, 2018.  
(Note: This code is a Python/MiniZinc implementation for graph-clear intended to introduce researchers to the problem. The research paper results are based on a C++/CP Optimizer implementation.)

**Citation:**
```
@article{morin2018intruder,
  title={Intruder alert! Optimization models for solving the mobile robot graph-clear problem},
  author={Morin, Michael and Castro, Margarita P and Booth, Kyle EC and Tran, Tony T and Liu, Chang and Beck, J Christopher},
  journal={Constraints},
  volume={23},
  number={3},
  pages={335--354},
  year={2018},
  publisher={Springer}
}
```

### File/directory descriptions:

*"data":* contains original problem instances.

*"data_dzn":* contains problem instances used in MiniZinc models, as automatically translated using 'translator.py'.

*"solutions":* this is where your solution files (.sol) should be stored.

*"autorun.py":* allows running a batch of experiments by specifying the directory of instances to be run. 

*"CPN.mzn":* CPN model from Constraints paper. 
 
*"CPS.mzn":* CPS model from Constraints paper. 

*"translator.py":* used to translate original problem instances to format required by MiniZinc models. 

*"checker.py":* checks .sol files in the "solutions" directory for feasbility. Outputs any solutions that are invalid (valid solutions have no output). 

### Running a model:

First, ensure you have [MiniZinc](http://www.minizinc.org/) installed!

From the "graph-clear" directory, the following command line example solves the "randomErdosRenyi_n5_p0.5_seed14121.dzn" with the CPN model and outputs the solution file to the "solutions" directory.

```console
minizinc CPN.mzn data_dzn/mini/randomErdosRenyi_n5_p0.5_seed14121.dzn -a -s -o solutions/randomErdosRenyi_n5_p0.5_seed14121.sol
```

In general, the command line structure to be used looks like:

```console
minizinc `<your_model>` data_dzn/`<path_to_instance>` -a -s -o solutions/`<your_solution_file>`
```

where:
* "-a" indicates you want to see all solutions as they're found 
* "-s" shows you the # of choice points for those solutions 
* "-o" specifies the output file that the solutions are stored in (important for checker.py to work properly).

The MiniZinc solver will run until: i) the optimal solution is found and proved, or ii) you terminate the process with cntl+C in your terminal. Solutions will be stored to the .sol file you specified when they are found.

### Solution file (.sol) format:

The format of one of your solution files (logged in the "solutions" directory) should look something like the following (for problem randomErdosRenyi_n5_p0.5_seed14121.dzn):

```text
Robots: 25; Sequence: [5, 4, 3, 2, 1]
%
% 203 choice points explored.
%
----------
Robots: 23; Sequence: [5, 4, 2, 3, 1]
%
% 390 choice points explored.
%
----------
Robots: 19; Sequence: [5, 2, 4, 3, 1]
%
% 583 choice points explored.
%
----------
Robots: 18; Sequence: [4, 2, 5, 3, 1]  <-- The solution checker will evaluate this solution
%
% 767 choice points explored.
%
----------
==========
```

The "==========" indicates the optimal solution to your model was found. Each solution is in the format: "Robots: int; Sequence: list". For the CPS model, we can express this at the end of our MiniZinc code as follows:

`output ["Robots: ", show(Z), "; Sequence: ", show(W)]`

Where Z is the objective value, and W is the sequence of nodes cleared. The output also shows us the total choice points (decisions) our models encountered (due to the "-s" option). Also, there are multiple solutions displayed (due to the "-a" terminal option). The checking script (explained next) will only look at the last, and thus best, solution in your solution files.

### Checking solutions:

Assuming you have run your model on a number of instances, you should now have solution files (.sol) in the "solutions" directory. To check if these solutions are feasible solutions to graph-clear, run the following in terminal from the "graph-clear" directory:

```console
python checker.py
```

The checker script will notify you of any solution files that are infeasible, as well as why they are infeasible.


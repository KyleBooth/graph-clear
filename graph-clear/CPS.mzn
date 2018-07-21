% Graph Clear: CPS Model (model #1), MiniZinc Implementation
% Author: Kyle E. C. Booth (kbooth@mie.utoronto.ca)
% Paper: Morin et al (2018), "Intruder Alert! Optimization Models for Solving the Mobile Robot Graph-Clear Problem."

include "alldifferent.mzn";

% Parameters
% (Note: key assumption |H|=n, one node cleared per time step)
int: n;
set of int: H = 1..n;
set of int: V = 1..n;
set of int: E = 1..n*n;
array[V] of int: a; % node weights
array[E] of int: b; % edge weights

% Variable definitions
var int: Z;
array[H] of var V: W; 

% Constraint (12)
constraint alldifferent(W);

% Constraint (13)
constraint
	forall(t in H)(
		Z >= a[W[t]] + sum(i in V)(b[(W[t]-1)*n+i]) 
					 + sum(t_ in 1..t-1, j in V)(b[(W[t_]-1)*n+j]) 
					 - sum(t_ in 1..t-1)(b[(W[t_]-1)*n+W[t]] + sum(t__ in 1..t-1)(if t__ != t_ then b[(W[t_]-1)*n+W[t__]] else 0 endif))
	);

% Objective Function (CPS)

%solve satisfy;
solve minimize Z;
%solve :: int_search(W, input_order, indomain, complete) minimize Z; 

% Solution Output
output ["Robots: ", show(Z), "; Sequence: ", show(W)]


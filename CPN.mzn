% Graph Clear: CPN Model (model #2), MiniZinc Implementation
% Author: Kyle E. C. Booth (kbooth@mie.utoronto.ca)
% Paper: Morin et al (2018), "Intruder Alert! Optimization Models for Solving the Mobile Robot Graph-Clear Problem."

include "alldifferent.mzn";
include "maximum.mzn";
include "inverse.mzn";

% Parameters
% (Note: key assumption |H|=n, one node cleared per time step)
int: n;
set of int: H = 1..n; 
set of int: V = 1..n; 
set of int: E = 1..n*n; 
set of int: E_t = 1..n*n*n; % extended set for I[i,j,t]
array[V] of int: a; % node weights
array[E] of int: b; % edge weights

% Variable definitions
var int: Z; 
array[V] of var H: T; % Step node cleared
array[E] of var H: L; % Step edge blocked
array[E] of var H: U; % Step edge released
array[H] of var int: S; % Sweeping cost of step
array[H] of var int: B; % Blocking cost of step
array[H] of var int: SB; % Total cost of step
array[E_t] of var 0..1: I; % Binary whether blocking edge necessary at time t
array[H] of var V: W; % Node cleared at step (redundant, book-keeping)

% Constraint (16)
constraint maximum(Z, SB); 

% Constraint (16')
constraint forall(t in H)(
	SB[t] = S[t] + B[t]
	);

% Constraint (17)
constraint
	forall(i in V, t in H)(
		T[i] = t -> S[t] = a[i] + sum(j in V)(b[(i-1)*n+j])
	);

% Constraint (18)
constraint alldifferent(T);

% Constraint (19)
constraint
	forall(i in V, j in V)(
		T[i] < T[j] -> L[(i-1)*n+j] = T[i]
	);

% Constraint (20)
constraint
	forall(i in V, j in V)(
		T[i] < T[j] -> U[(i-1)*n+j] = T[j]
	);

% Constraint (21)
constraint
	forall(i in V, j in V, t in H)(
		(L[(i-1)*n+j] <= t /\ U[(i-1)*n+j] >= t) /\ (T[i] != t /\ T[j] != t) -> I[(t-1)*n*n+(i-1)*n+j] = 1
	);

% Constraint (22)
constraint
	forall(t in H)(
		B[t] = sum(i in V, j in V)(b[(i-1)*n+j]*I[(t-1)*n*n+(i-1)*n+j])
	);

% Constraint (for output)
constraint inverse(W, T);

% Objective Function (CPN)

%solve satisfy;
solve minimize Z;

% Solution Output
output ["Robots: ", show(Z), "; Sequence: ", show(W)]


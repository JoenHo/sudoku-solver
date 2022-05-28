
<center><h1>Sudoku AI Solver</h1></center>




---


Constraint Propagation (AC-3 Algorithm)
AC-3 algorithm will propagate the constraints and reduce the domain size of the variables by ensuring all possible (future) assignments consistent. 


Backtracking Search Algorithm
The backtracking algorithm will be implemented using the minimum remaining value (MRV) heuristic. The order of values to be attempted for each variable can be arbitrary. When a variable is assigned, forward checking will be applied to further reduce variables domains.
At each unassigned variable, it will iterate through the values in order 1-9 (or in
odometer order if you are doing Monster Sudoku). It will assign each value in turn to that
variable. If the assignment does not violate any constraints it will proceed to the next variable. If
the assignment does violate a constraint it will undo that assignment and proceed to the next
value. If the values for that variable become exhausted it will backtrack to the previous variable,
undo its current assignment, and proceed to its next value.


Minimum Remaining Heuristic (MRV)
The next unassigned variable
chosen is one that has the fewest remaining possible values in its domain (there may be
several variables that have the same minimum number of possible values remaining).
Ties are broken arbitrarily, or by DH if DH also was specified.

Degree heuristic: assign a value to the variable that is involved in the largest number of constraints on other unassigned variables. 
Minimum remaining values (MRV): choose the variable with the fewest possible values.

<center><b><h2>Sudoku AI Solver</h2></b></center>

---
This program uses AC-3, Backtracking Search, Forward Checking, MRV and Degree Heuristics to solve 9 x 9 Sudoku puzzles.<br/>
Program Flow:
1. Read Sudoku problems from file
2. Solve problem via:
    - Constraint Propagation (use AC-3 algorithm)<br/>
    Remove all non-valid domain values given the initial sudoku layout
    - Backtracking Search (BT) extended by Forward Checking (FC) + MRV and Degree Heuristics<br/>
    Traverse blank cells to assign possible value in its domain. After a blank cell is assigned a value, verify the validity by forward checking. If the one conflicts with another value, go back to previous state and try another possible value.
    Heuristics are used to determine which blank cell to assign next.
3. Display solution to the terminal
<br/><br/>

---
<!-- <b><h3>Techniques Used</h3></b>
<details>
<summary>AC-3</summary>
description
<pre>
<code>
</code>
</pre>
</details>

<details>
<summary>Backtracking Search (BT)</summary>
description
<pre>
<code>
</code>
</pre>
</details>


<details>
<summary>Forward Checking (FC)</summary>
description
<pre>
<code>
</code>
</pre>
</details>


<details>
<summary>Minimum Remaining Heuristic (MRV)</summary>
description
<pre>
<code>
</code>
</pre>
</details>


<details>
<summary>Degree Heuristic</summary>
description
<pre>
<code>
</code>
</pre>
</details>

<br/>

--- -->

<b><h3>Instructions</h3></b>

<b>Prepare Input File</b><br/>
- Name input file as <code>sudoku-puzzles.csv</code><br/>
- 9 x 9 sudoku board is represented as 81 consecutive numbers<br/>
- Format sudoku puzzles as <code> [puzzle] {[puzzle solution]} </code><br/>
    * <code>0</code> represents an empty cell <br/>
    * puzzle solution is optional (if solution is provided, program will display solution at the end) <br/>
    * multiple puzzles can be added to input file (in that case, program will select puzzle randomly) <br/>
<pre>
<code>
Example with solution
030604250200300100009250008000700090902005031740100006090070604001060000526800903 837614259254398167619257348183726495962485731745139826398572614471963582526841973
<br/>
Example without solution
008605010000000420010700000000010530000000080300800009040900000097001600030024000
</code>
</pre>
<br/>

<b>Run Program</b><br/>
Type command <code>python3 solver.py</code> to start program
<br/>

---

<b><h3>Output Example</h3></b>
![output-example](https://user-images.githubusercontent.com/59863142/183360877-1c22c498-6847-4066-be47-dda4445eac19.png)

<br/>

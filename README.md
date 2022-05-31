
<center><b><h2>Sudoku AI Solver</h2></b></center>

---

This program consist of following steps:
1. Read Sudoku problems from file
2. Solve problem via:
- [x] Constraint Propagation (use AC-3 algorithm)<br/>
    Remove all non-valid domain values given the initial sudoku layout
- [x] Backtracking Search (BT) extended by Forward Checking (FC) + MRV and Degree Heuristics<br/>
    Traverse blank cells to assign possible value in its domain. After a blank cell is assigned a value, verify the validity by forward checking. If the one conflicts with another value, go back to previous state and try another possible value.
    Heuristics are used to determine which blank cell to assign next.
3. Display solution to terminal
<br/><br/>

---
<b><h3>Techniques Used</h3></b>
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

---

<b><h3>Instructions</h3></b>

<details>
<summary>Prepare Input File</summary>
<br>
<pre>
<code>
</code>
</pre>
</details>
<br/>

<details>
<summary>Run Program</summary>
<br>
<pre>
<code>
</code>
</pre>
</details>
<br/>

---

<br/>

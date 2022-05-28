import csv
from math import degrees
import numpy as np

# ---  Global Variables --- #
# Sudoku Database (pair: problem, solution)
puzzles = []

# Sudoku Dataset CSV Path
csv_path = "sudoku-puzzles.csv"

# Current Sudoku Puzzle
puzzle = np.zeros((9,9), dtype=int)

# Solution to Current Sudoku Puzzle
puzzle_sol = np.zeros((9,9), dtype=int)

# Domain of each cell in a puzzle (initial domain for each cell is 1 to 9)
domains = [[{1,2,3,4,5,6,7,8,9} for _ in range(9)] for _ in range(9)]

# Degree of each cells (degree = number of unassigned cells in row col and square)
deg_heu = np.zeros((9,9), dtype=int)
# ------------------------- #


def print_puzzle_board(board):
    bar = '\033[94m-------------------------\033[0m\n'
    lnf = '\033[94m|\033[0m' +(' {:}'*3 + ' \033[94m|\033[0m')*3 + '\n'
    bft = bar + (lnf*3+bar)*3
    print(bft.format(*(el for rw in board for el in rw)))


def construct_puzzles():
    # read sudoku data set from csv file
    file = open(csv_path)
    csvreader = csv.reader(file)
    rows = []
    for row in csvreader:
            rows.append(row)
    file.close()

    # reshape into problem solution pair of 9x9 matrix 
    for row in rows:
        if len(row[0]) >= 81:
            problem = np.reshape(np.array([int(x) for x in row[0][0:81]]),(9,9))
        if len(row[0]) >= 163:
            solution = np.reshape(np.array([int(x) for x in row[0][82:]]),(9,9))
        puzzles.append([problem, solution])


def random_generate_puzzle():
    global puzzle, puzzle_sol
    np.random.seed()
    i = np.random.randint(len(puzzles))
    puzzle = puzzles[i][0]
    puzzle_sol = puzzles[i][1]


def ini_constraint():
    global puzzle, domains

    # reduce domains where the cell already has fixed value  
    for i in range(9):
        for j in range(9):
            if(puzzle[i][j] != 0):
                domains[i][j] = {puzzle[i][j]}

    # for cells with domain size > 1, do constraint propagation
    for i in range(9):
        for j in range(9):
            if(len(domains[i][j]) > 1):
                constraint_propagation(i, j)


def constraint_propagation(i, j):
    global domains

    # reduce domain for cell(i,j)
    d_all = {1,2,3,4,5,6,7,8,9}                                 # domain of all possible value

    diff_row = d_all.difference(puzzle[i,:])                    # difference between d_all and i th row
    diff_col = d_all.difference(puzzle[:,j])                    # difference between d_all and j th column
    r = i // 3 * 3
    c = j // 3 * 3
    diff_squ = d_all.difference(puzzle[r:r+3,c:c+3].flatten())  # difference between d_all and square of cell(i,j) belongs to
    intersection = diff_row.intersection(diff_col,diff_squ)     # intersection between all three differences
    
    # set new domain
    domains[i][j] = intersection

    # fill the puzzle if only one value left in the domain
    if len(intersection):
        puzzle[i][j] = list(intersection)[0]


def update_degree():
    global deg_heu

    # reset degree heuristics
    deg_heu.fill(0)

    # for empty cells, count the degree to other unassigned cells in row col and square
    for i in range(9):
        for j in range(9):
            if(puzzle[i][j] == 0):
                n_row = np.count_nonzero(puzzle[i,:]==0) - 1    # number of 0 in i th row - 1
                n_col = np.count_nonzero(puzzle[i,:]==0) - 1    # number of 0 in j th row - 1
                r = i // 3 * 3
                c = j // 3 * 3
                sub_squ = puzzle[r:r+3,c:c+3]
                sub_squ = np.delete(sub_squ, abs(r-i), 0)
                sub_squ = np.delete(sub_squ, abs(c-j), 1)
                n_squ = np.count_nonzero(sub_squ==0)            # number of 0 in square after removing i row and j column
                # update degree
                deg_heu[i][j] = n_row + n_col + n_squ



def backtracking_search():
    
    # stop searching when all cells are filled or after 100 iterations
    num_ite = 0
    while(np.count_nonzero(puzzle == 0) != 0 and num_ite < 100):
        # update degree heuristic
        update_degree()

        # find the index of cell with highest degree
        max_index = np.unravel_index(deg_heu.argmax(), deg_heu.shape)

        # 
        # constraint_propagation(max_index[])
        num_ite += 1



def main():

    # Create Sudoku Puzzles from Input File
    construct_puzzles()

    # Generate Sudoku Puzzle
    random_generate_puzzle()

    # Print Sudoku Puzzle Board
    print("\033[1;33m Sudoku Problem \033[0m")
    print_puzzle_board(puzzle)

    # Initial Constraints Propagation
    ini_constraint()

    print("\033[1;33m After Initial Constraint Propagation \033[0m")
    print_puzzle_board(puzzle)
    print("num of 0 = ",np.count_nonzero(puzzle == 0))
    
    ini_constraint()

    print("\033[1;33m After Second Constraint Propagation \033[0m")
    print_puzzle_board(puzzle)
    print("num of 0 = ",np.count_nonzero(puzzle == 0))

    ini_constraint()
    print("\033[1;33m After Third Constraint Propagation \033[0m")
    print_puzzle_board(puzzle)
    print("num of 0 = ",np.count_nonzero(puzzle == 0))

    # Start Backtracking Search with Forward Checking
    # backtracking_search()
    

    # MRV


    # Display Result



if __name__ == '__main__':
    main()



# 81 vars - initial D is from 1-9
# before doing degree heuristics, do constraints propagation
# choose the best degree heuristic var, assign a number from its domain
# fill the priority queue for MRV (keep it updated), pick the best ?? from priority queue
# if the domain become empty, it is failure, so stop and backtrack to previous value picking
# use stack to keep track of which to backtrack
# degree: number of empty cells in neighbors
# MRV number options in the domain
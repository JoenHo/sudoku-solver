import csv
import numpy as np
import copy
from collections import deque

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
domains = np.array([[{1,2,3,4,5,6,7,8,9} for _ in range(9)] for _ in range(9)])

# Minimum Remaining Value (MRV) list
mrv = np.zeros((9,9), dtype=int)

# Degree of each cells (degree = number of unassigned cells in row col and square)
deg_heu = np.zeros((9,9), dtype=int)

# Keep track of number of recursion to avoid infinite loop caused by bad input
num_tries = 0
max_num_tries = 100000
# ------------------------- #


def print_puzzle_board(board):
    bar = '\033[94m-------------------------\033[0m\n'
    lnf = '\033[94m|\033[0m' +(' {:}'*3 + ' \033[94m|\033[0m')*3 + '\n'
    bft = bar + (lnf*3+bar)*3
    print(bft.format(*(el for rw in board for el in rw)))


def construct_puzzles():
    global puzzles
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
        else:
            solution = np.reshape(np.array([int(0) for x in range(81)]),(9,9))
        puzzles.append([problem, solution])


def random_generate_puzzle():
    global puzzle, puzzle_sol
    np.random.seed()
    i = np.random.randint(len(puzzles))
    puzzle = copy.deepcopy(puzzles[i][0])
    puzzle_sol = copy.deepcopy(puzzles[i][1])


def ini_constraint():
    global puzzle, domains

    # reduce domains where the cell already has fixed value  
    for i in range(9):
        for j in range(9):
            if(puzzle[i][j] != 0):
                domains[i][j] = {puzzle[i][j]}


def AC3() -> bool:
    global domains
    queue = deque([])
    
    # put all constraints to queue
    for i in range(9):
        for j in range(9):
            if len(domains[i][j]) > 1:
                queue.append([i,j])

    # while queue is not empty
    while(queue):
        # pop one from queue
        indx = queue.popleft() 

        # reduce domain
        d_len = len(domains[indx[0]][indx[1]])  # original len of domain
        ret = apply_arc_consistency(indx[0], indx[1])
        if(ret == False): return False

        # if domain reduced
        if(d_len != len(domains[indx[0]][indx[1]])):
            
            # get neighbors (cells in same row, colum or square)
            neighbors = get_neighbors(indx[0], indx[1])

            # add blank neighbors to queue
            for neighbor in neighbors:
                if(puzzle[neighbor[0]][neighbor[1]] == 0):
                    queue.append([neighbor[0], neighbor[1]])
    
    return  True



def get_neighbors(i, j):
    # get neighbors (in same row, colum or square) of cell at row i and column j
    neighbors = set()

    # append neighbors in row i except itself
    for x in range(9):
        if(x != j):
            neighbors.add((i, x))

    # append neighbors in column j except itself
    for x in range(9):
        if(x != i):
            neighbors.add((x, j))

    # append neighbors in the same square except itself
    r = i // 3 * 3
    c = j // 3 * 3
    for x in range(3):
        for y in range(3):
            if(r + x != i and c + y != j):
                neighbors.add((r+x, c+y))

    return neighbors
    

def check_neighbors_arc_consistency(i, j) -> bool:

    # for all neighbors of (i,,j), check if they satisfy arc consistency
    neighbors = get_neighbors(i, j)
    for neighbor in neighbors:
        if(puzzle[neighbor[0]][neighbor[1]] == 0):
            if(False == apply_arc_consistency(neighbor[0], neighbor[1])):
                return False
    return True


def apply_arc_consistency(i, j) -> bool:
    global domains, puzzle

    # if puzzle board at (i,j) is already filled, return true
    if(puzzle[i][j] != 0): return True

    # get domain for cell(i,j)
    intersection = get_domain(i, j)
    
    # if no value remains, fail
    if(len(intersection) < 1):
        return False

    # set new domain
    domains[i][j] = set.copy(intersection)

    # fill the puzzle if only one value left in the domain
    if(len(intersection) == 1):
        puzzle[i][j] = list(intersection)[0]
    
    return True


def get_domain(i, j):

    if(puzzle[i][j] != 0):
        return {puzzle[i][j]}

    # update domain for cell(i,j)
    d_all = {1,2,3,4,5,6,7,8,9}                                 # domain of all possible value

    diff_row = d_all.difference(puzzle[i,:])                    # difference between d_all and i th row
    diff_col = d_all.difference(puzzle[:,j])                    # difference between d_all and j th column
    r = i // 3 * 3
    c = j // 3 * 3
    diff_squ = d_all.difference(puzzle[r:r+3,c:c+3].flatten())  # difference between d_all and square of cell(i,j) belongs to
    intersection = diff_row.intersection(diff_col,diff_squ)     # intersection between all three differences

    return intersection


def update_degree():
    global deg_heu

    # reset degree heuristics
    deg_heu.fill(0)

    # for empty cells, count the degree to other unassigned cells in row col and square
    for i in range(9):
        for j in range(9):
            if(puzzle[i][j] == 0):
                n_row = np.count_nonzero(puzzle[i,:]==0) - 1    # number of 0 in i th row - itself
                n_col = np.count_nonzero(puzzle[i,:]==0) - 1    # number of 0 in j th row - itself
                r = i // 3 * 3
                c = j // 3 * 3
                sub_squ = puzzle[r:r+3,c:c+3]
                sub_squ = np.delete(sub_squ, abs(r-i), 0)
                sub_squ = np.delete(sub_squ, abs(c-j), 1)
                n_squ = np.count_nonzero(sub_squ==0)            # number of 0 in square after removing i row and j column
                # update degree
                deg_heu[i][j] = n_row + n_col + n_squ


def update_mrv():
    global mrv

    # reset mrv list
    mrv.fill(0)

    # for all cells, count the number of possible value in its domain
    for i in range(9):
        for j in range(9):
            if(puzzle[i][j] != 0):
                num = 10  # to not consider filled cells, assign 10 which is greater than max domain num 
            else:
                num = len(domains[i][j])                 
            mrv[i][j] = num


def get_next_variable():

    # update MRV list and pick one with fewest domain values (min of MRV)
    update_mrv()
    min_arr = np.nonzero(mrv == mrv.min())
    r = min_arr[0][0]   # min_arr[0] is list of row indices 
    c = min_arr[1][0]   # min_arr[1] is list of column indices 

    # if there is a tie
    if(len(min_arr[0]) != 1):
        # update degree heuristic list
        update_degree()
        max_degree = deg_heu[r][c]
        # among mrv cells, pick one with the highest degree heuristics
        for n in range(len(min_arr[0])):
            i = min_arr[0][n]
            j = min_arr[1][n]
            if max_degree < deg_heu[i][j]:
                max_degree = deg_heu[i][j]
                r = i
                c = j
    return [r,c]


def backtracking_search() -> bool:
    global puzzle, domains, num_tries

    # recursion base cases
    if(np.count_nonzero(puzzle == 0) == 0):
        # found solution
        return True

    num_tries += 1
    if(num_tries >= max_num_tries):
        # no solution found after max_num_tries recursions
        print("Solution not found after", max_num_tries, "iterations!")
        return False

    # get next variable to process
    next_index = get_next_variable()
    row_index = next_index[0]
    col_index = next_index[1]

    # pick a value from its domain, and do forward checking
    for val in (domains[row_index][col_index]).copy():

        ret = is_valid_assignment(val, row_index, col_index)
        if(ret == True):
            # assign value to puzzle board
            puzzle[row_index][col_index] = val

            # call recursively 
            if backtracking_search():
                # update domain
                d = get_domain(row_index, col_index)
                domains[row_index][col_index] = d
                return True

        # rollback
        puzzle[row_index][col_index] = 0
        
    return False


def is_valid_assignment(val, i, j):
    global domains, puzzle

    # if puzzle board at (i,j) is already filled, return true
    if(puzzle[i][j] != 0):
        return True

    # get domain for cell(i,j)
    intersection = get_domain(i, j)
    if(len(intersection) < 1):
        return False

    # check if val is possible assignment
    if val in intersection:
        return True

    return False


def main():
    
    # create sudoku puzzles from input file
    construct_puzzles()

    # generate sudoku puzzle
    random_generate_puzzle()

    # print sudoku puzzle board
    print("\n\033[1;33m     Sudoku Problem     \033[0m")
    print_puzzle_board(puzzle)
    print("\033[0;36m Number of Blanks:", np.count_nonzero(puzzle == 0), "\033[0m\n")

    # initial constraints propagation
    ini_constraint()

    # constraint propagation with Arc-Consistency
    ret = AC3()
    print("\n\033[1;33m        After AC3       \033[0m")
    print_puzzle_board(puzzle)
    print("\033[0;36m  Number of Blanks:", np.count_nonzero(puzzle == 0), "\033[0m\n")

    # backtracking with MRV heuristic and forward checking
    ret = backtracking_search()
    print("\n\033[1;33m   After Backtracking   \033[0m")
    print_puzzle_board(puzzle)
    print("\033[0;36m  Number of Blanks:", np.count_nonzero(puzzle == 0), "\033[0m\n")

    # Display Solution (if provided)
    if(np.count_nonzero(puzzle_sol==0) == 0):
        print("\n\033[1;33m       Solution        \033[0m")
        print_puzzle_board(puzzle_sol)


if __name__ == '__main__':
    main()
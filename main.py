import csv
import numpy as np
import copy

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
max_num_tries = 800
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
    puzzle = puzzles[i][0]
    puzzle_sol = puzzles[i][1]


def ini_constraint():
    global puzzle, domains

    # reduce domains where the cell already has fixed value  
    for i in range(9):
        for j in range(9):
            if(puzzle[i][j] != 0):
                domains[i][j] = {puzzle[i][j]}


def constraint_propagation():      
        
    # do constraint propagation to reduce domains until no more reduction is possible
    i = 0
    while(True):
        num_unassigned = np.count_nonzero(puzzle == 0)

        # reduce domains
        reduce_domains()

        print("\033[1;33m Constraint Propagation #", i, "\033[0m")
        print_puzzle_board(puzzle)
        print("num of 0 = ", np.count_nonzero(puzzle == 0), "\n")
        i+=1

        # if the number of unassigned cell is same as previous time, stop
        if(num_unassigned == np.count_nonzero(puzzle == 0)):
            break 


def reduce_domains():

    # for all unassigned cells, do constraint propagation
    for i in range(9):
        for j in range(9):
            if(puzzle[i][j] == 0):
                # apply_arc_consistency(cp_puz, cp_dom, i, j)
                apply_arc_consistency(i, j)


def apply_arc_consistency(i, j) -> bool:
    global domains, puzzle

    # reduce domain for cell(i,j)
    d_all = {1,2,3,4,5,6,7,8,9}                                 # domain of all possible value

    diff_row = d_all.difference(puzzle[i,:])                    # difference between d_all and i th row
    diff_col = d_all.difference(puzzle[:,j])                    # difference between d_all and j th column
    r = i // 3 * 3
    c = j // 3 * 3
    diff_squ = d_all.difference(puzzle[r:r+3,c:c+3].flatten())  # difference between d_all and square of cell(i,j) belongs to
    intersection = diff_row.intersection(diff_col,diff_squ)     # intersection between all three differences
    
    if(len(intersection) < 1):
        return False

    # set new domain
    domains[i][j] = intersection

    # fill the puzzle if only one value left in the domain
    if(len(intersection) == 1):
        puzzle[i][j] = list(intersection)[0]
    
    return True


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
    if(len([min_arr[0]]) != 1):
        # update degree heuristic list and pick one with the highest degree heuristics
        update_degree()
        max_degree = deg_heu[r][c]
        for n in range(len(min_arr[0])):
            i = min_arr[0][n]
            j = min_arr[1][n]
            if max_degree < deg_heu[i][j]:
                max_degree = deg_heu[i][j]
                r = i
                c = j
    return [r,c]



def backtracking_search() -> bool:
    global num_tries, puzzle, domains

    #update number of tries
    num_tries += 1

    # recursion base cases
    if(np.count_nonzero(puzzle == 0) == 0):
        # found solution
        print("SOLUTION FOUND!!!")
        return True
    if(num_tries >= max_num_tries):
        # no solution found after max_num_tries recursions
        print("SOLUTION COULD NOT FOUND!!!")
        return False

    # get next variable to process
    next_index = get_next_variable()
    row_index = next_index[0]
    col_index = next_index[1]

    # pick a value from its domain, and do forward checking
    d = (domains[row_index][col_index]).copy()
    for val in d:
        # backup current state of puzzle / domains
        bk_puzzle = copy.deepcopy(puzzle)
        bk_domains = copy.deepcopy(domains)

        # assign value to puzzle board
        puzzle[row_index][col_index] = val

        # remove other values from its domain
        for x in d:
            if x != val:
                domains[row_index][col_index].discard(x)

        # apply arc consistency
        ret = apply_arc_consistency(row_index, col_index)
        if(ret==True):
            backtracking_search()
            return True
        else:
            # rollback to previous state
            puzzle = bk_puzzle
            domains = bk_domains
        
    return False


def main():

    # try:
    is_solved = False
    
    # create sudoku puzzles from input file
    construct_puzzles()

    # generate sudoku puzzle
    random_generate_puzzle()

    # print sudoku puzzle board
    print("\033[1;33m Sudoku Problem \033[0m")
    print_puzzle_board(puzzle)

    # initial constraints propagation
    ini_constraint()

    # constraint propagation with Arc-Consistency
    constraint_propagation()
        
    # backtracking with MRV heuristic and forward checking
    backtracking_search()

    # Display Result
    print("\033[1;33m Result \033[0m")
    print_puzzle_board(puzzle)
    print("num of 0 = ", np.count_nonzero(puzzle == 0), "\n")
    print("num of recursion = ",num_tries , "\n")



    # except Exception as e:
    #     print("\n \033[1;37;41m", e ,"\033[0m")


if __name__ == '__main__':
    main()
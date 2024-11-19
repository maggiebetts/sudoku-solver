# File: pa4.py
# Author: Maggie Betts and Kera Hernandez
# Date: May 16th, 2024
# Description: Solves a Sudoku board of either 9, 16, or 25

import copy
import math

class Cell:
    def __init__(self, fixed_value, position):
        self.fixed_value = fixed_value
        self.possible_values = []
        self.position = position

    def get_fixed_value(self):
        return self.fixed_value
    
    def get_possible_values(self):
        return self.possible_values
    
    def remove_possible_value(self, value):
        if value in self.possible_values:        
            self.possible_values.remove(value)
            
    def get_position(self):
        return self.position
    
    def set_possible_values(self, val):
        self.possible_values.append(val)

    def set_fixed_value(self, val):
        self.fixed_value = val

    def make_option(self, val):
        self.possible_values = [val]
    

class Board:

    def __init__(self, size):
        self.size = size
        self.values = {9 : "123456789", 16 : "123456789ABCDEFG", 25 : "ABCDEFGHIJKLMNOPQRSTUVWXY"}
        self.board = self.create_empty_board()

    def create_empty_board(self):
        board = []

        # Create board with all zero values
        for i in range(self.size):
            row = []
            for j in range(self.size):

                empty_cell = Cell("0", (i,j))
                for item in self.values[self.size]:             #initializes possible values to all values
                    empty_cell.set_possible_values(item)
                row.append(empty_cell)
                
            board.append(row)
        return board
    
    def define_cell(self, fixed_value, row, col):
        self.board[row][col] = Cell(fixed_value, (row, col))
    
    def get_cell(self, row, column):
        return self.board[row][column]
    
    def get_board(self):
        return self.board
    
    def get_values(self):
        return self.values
    
    def __str__(self):
        board_str = ''
        for row in self.board:
            board_str += ' '.join(str(cell) for cell in row) + '\n'
        return board_str



class Sudoku:
    def __init__(self, size, filename):
        self.size = size
        self.filename = filename
        self.nodes_generated = 0
        self.unique_cells = []
        self.unsolved_cells = []
        self.problem = False

        # Create board
        self.board = Board(self.size)

        # Open file
        with open(self.filename) as f:
            for line in f:
                vals = line.split()
                row, col, value = int(vals[0]) - 1, int(vals[1]) - 1, vals[2]
                cell = self.board.get_cell(row, col)
                cell.set_fixed_value(value)



    def compute_unsolved_cells(self):
        #iterate through the board and get the empty cells
        for r in range(self.size):
            for c in range(self.size):
                if self.board.get_cell(r, c).get_fixed_value() == "0":
                    self.unsolved_cells.append(self.board.get_cell(r,c))



    def possible_values(self, cell):
        r = cell.get_position()[0]
        c = cell.get_position()[1]
        existing_vals = set()

        for col in range(self.size):
            val = self.board.get_cell(r, col).get_fixed_value()
            if val != "0":
                existing_vals.add(val)

        for row in range(self.size):
            val = self.board.get_cell(row, c).get_fixed_value()
            if val != "0":
                existing_vals.add(val)

        sub_matrix_size = int(math.sqrt(self.size))
        starting_row = (r // sub_matrix_size) * sub_matrix_size
        starting_column = (c // sub_matrix_size) * sub_matrix_size 
        for i in range(starting_row, starting_row + sub_matrix_size):
            for j in range(starting_column, starting_column + sub_matrix_size):
                val = self.board.get_cell(i,j).get_fixed_value()
                if val != "0":
                    existing_vals.add(val)

        for item in existing_vals:
            cell.remove_possible_value(item)

            
        if len(cell.get_possible_values()) == 1 and cell not in self.unique_cells:
            self.unique_cells.append(cell)



    def handle_unique_cells(self):

        while len(self.unique_cells) != 0: 

            #remove the cell from list and fix value
            cell = self.unique_cells.pop()

            if len(cell.get_possible_values()) == 0:
                self.problem = True                    

            cell.set_fixed_value(cell.get_possible_values()[0])
            self.unsolved_cells.remove(cell)   
            

            r = cell.get_position()[0]
            c = cell.get_position()[1]

            for row in range(self.size):
                self.update_potential_values(self.board.get_cell(row, c), cell.get_fixed_value())

            for col in range(self.size):
                self.update_potential_values(self.board.get_cell(r, col), cell.get_fixed_value())

            sub_matrix_size = int(math.sqrt(self.size))
            starting_row = (r // sub_matrix_size) * sub_matrix_size
            starting_column = (c // sub_matrix_size) * sub_matrix_size 
            for i in range(starting_row, starting_row + sub_matrix_size):
                for j in range(starting_column, starting_column + sub_matrix_size):
                    self.update_potential_values(self.board.get_cell(i, j), cell.get_fixed_value()) 
            
            self.find_unique_values(self.board)



    def update_potential_values(self, cell, fixed_value):
        if fixed_value in cell.get_possible_values():
            cell.remove_possible_value(fixed_value)
            if len(cell.get_possible_values()) == 1 and cell not in self.unique_cells and cell in self.unsolved_cells:
                self.unique_cells.append(cell)
        

    def find_unique_values(self, board):
        for cell in self.unsolved_cells:
            r = cell.get_position()[0]
            c = cell.get_position()[1]
       
            existing_vals = set()
            found = False
            #print(cell.get_position())

            if len(cell.get_possible_values()) != 1:
                for col in range(self.size):
                    if col != c and board.get_cell(r,col).get_fixed_value() == "0":
                        vals = board.get_cell(r,col).get_possible_values()
                        for val in vals:
                            existing_vals.add(val)
                for option in cell.get_possible_values():
                    if option not in existing_vals:
                        cell.make_option(option)
                        self.unique_cells.append(cell)
                        found = True
                        #print(cell.get_possible_values())
                existing_vals = set()

                if found != True:
                    for row in range(self.size):
                        if row != r and board.get_cell(row, c).get_fixed_value() == "0":
                            vals = board.get_cell(row, c).get_possible_values()
                            for val in vals:
                                existing_vals.add(val)
                    for option in cell.get_possible_values():
                        if option not in existing_vals:
                            cell.make_option(option)
                            self.unique_cells.append(cell)
                            found = True
                            #print(cell.get_possible_values())
                    existing_vals = set()


                if found != True:
                    sub_matrix_size = int(math.sqrt(self.size))
                    starting_row = (r // sub_matrix_size) * sub_matrix_size
                    starting_column = (c // sub_matrix_size) * sub_matrix_size 
                    for i in range(starting_row, starting_row + sub_matrix_size):
                        for j in range(starting_column, starting_column + sub_matrix_size):
                            if i != r or j != c:                                            #make sure this isn't the cell we're currently looking at
                                vals = board.get_cell(i,j).get_possible_values()
                                if board.get_cell(i,j).get_fixed_value() == "0":
                                    for val in vals:
                                        existing_vals.add(val)
                    for option in cell.get_possible_values():
                        if option not in existing_vals:
                            cell.make_option(option)
                            self.unique_cells.append(cell)
                            #(cell.get_possible_values())



    def solve(self):

        self.compute_unsolved_cells()       #keeps track of what cells are unsolved in a list unsolved_cells
        for cell in self.unsolved_cells:    #determines the possible_values for each cell
            self.possible_values(cell)

        #TODO: this is causing an index out of bounds error when the problem should have already returned a None
        self.find_unique_values(self.board)

        self.handle_unique_cells()

        if len(self.unsolved_cells) == 0:
            solution_board = []
            for row in self.board.get_board():
                solution_row = []
                for cell in row:
                    solution_row.append(cell.get_fixed_value())
                solution_board.append(solution_row)
            return solution_board, self.nodes_generated
        else:
            self.unsolved_cells.sort(key=lambda cell: len(cell.get_possible_values()))
            solution = self.recurse_to_solve()
            if solution[0] is None:
                return None, self.nodes_generated
            return solution



    def recurse_to_solve(self):
        # return current board 
        if len(self.unsolved_cells) == 0:
            solution_board = []
            for row in self.board.get_board():
                solution_row = []
                for cell in row:
                    solution_row.append(cell.get_fixed_value())
                solution_board.append(solution_row)
            return solution_board, self.nodes_generated
        
        else:
            trial_unsolved = copy.deepcopy(self.unsolved_cells)  #Make a copy of the list of unassigned cells
            trial_board = copy.deepcopy(self.board)              #Make a copy of the board

            cell = self.unsolved_cells[0]                       #Get the first element from the list of empty cells, not the copy of the list
            possible_values = cell.get_possible_values()

            for value in possible_values:                       #Iterate through the list of candidates for the cell, recall that the candidates is a set, so convert the set to a list and iterate through it. This is the part where we make a “guess” on the value that the cell should have
                cell.set_fixed_value(value)                     #Set the value of the cell to this candidate
                self.unsolved_cells.remove(cell)                #Now that it’s fixed, remove the position (row, col) from the list of empty cells
                self.nodes_generated += 1

                r = cell.get_position()[0]
                c = cell.get_position()[1]

                #TODO: make sure syntax for this is right
                for row in range(self.size):                    #Update candidates in the row, col, and submatrix by removing the value you just fixed
                    self.update_potential_values(self.board.get_cell(row, c), cell.get_fixed_value())

                for col in range(self.size):
                    self.update_potential_values(self.board.get_cell(r, col), cell.get_fixed_value())

                sub_matrix_size = int(math.sqrt(self.size))
                starting_row = (r // sub_matrix_size) * sub_matrix_size
                starting_column = (c // sub_matrix_size) * sub_matrix_size 
                for i in range(starting_row, starting_row + sub_matrix_size):
                    for j in range(starting_column, starting_column + sub_matrix_size):
                        self.update_potential_values(self.board.get_cell(i, j), cell.get_fixed_value())         

                self.find_unique_values(self.board)
                self.handle_unique_cells()                      #Handle unique cells again.


                # TODO: need to find a way to return if this isn't working so we can have an if here
                if self.problem != False:
                    result = self.recurse_to_solve()                  # *Only if handling unique cells was successful, go onto the next recursion level
                    if result[0] is not None:
                        return result
                
                else:
                    self.board = trial_board
                    self.unsolved_cells = trial_unsolved
                    self.problem = False
                    for r in range(self.size):
                        for c in range(self.size):
                            self.possible_values(self.board.get_cell(r,c)) #to reset vals

            return None, self.nodes_generated

def solve(size, filename):
    """
    Solves the Sudoku problem specified in input file filename.
    The size of the problem is size.  (For example, for a 9 x 9 Sudoku,
    size is 9.)
    Returns a tuple of size 2.  The first element is a nested list containing
    the solution to the problem (row is the first index, col the second).
    The second element of the tuple is the number of nodes in the state space
    tree that were generated by your solution.
    """
    sudoku = Sudoku(size, filename)

    return sudoku.solve()

if __name__ == "__main__":
    SIZE = 9
    FILENAME = "p1.txt"
    SOLUTION_FILENAME = "p1Sol.txt"
    solution = solve(SIZE, FILENAME)
    if not solution[0]:
        print("No solution")
    else:
        print(solution[0])
    print(f"Nodes generated = {solution[1]}")
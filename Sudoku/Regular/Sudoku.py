from SudokuReader import readSudoku
import SudokuSolver as ss

def dots_to_grid(dot_str):

  grid = [[0 for _ in range(9)] for _ in range(9)]

  for i in range(len(dot_str)):

    if dot_str[i] != '.':
      grid[i // 9][i % 9] = int(dot_str[i])
      
  return grid

# sudoku = readSudoku("Grid1.txt")

sudoku = dots_to_grid(input())

ss.solveSudoku(sudoku)
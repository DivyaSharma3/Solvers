def validInRow(sudoku, number, row):

    for column in range(9):
        if (sudoku[row][column] == number):
            return False
    return True

def validInColumn(sudoku, number, column):

    for row in range(9):
        if (sudoku[row][column] == number):
            return False
    return True

def validInSquare(sudoku, number, row, column):

    squareRowStart = row - (row % 3)
    squareColStart = column - (column % 3)

    for r in range(3):
        for c in range(3):
            if(sudoku[r + squareRowStart][c + squareColStart] == number):
                return False
    return True

def validSpace(sudoku, number, row, column):
    return ( (validInRow(sudoku, number, row)) and (validInColumn(sudoku, number, column)) and (validInSquare(sudoku, number, row, column)) )

def findEmpty(sudoku):

    for row in range(9):
        for col in range(9):
            if (sudoku[row][col] == 0):
                return row, col
    return -1, -1

def solveSudoku(sudoku, row = 0, column = 0):

    row, column = findEmpty(sudoku)

    if (row == -1):
        for row in sudoku:
            print(" ".join(map(str,row)))
        
        return True

    for number in range(1, 10):
        if (validSpace(sudoku, number, row, column)):
            sudoku[row][column] = number

            if (solveSudoku(sudoku, row, column)):
                return True

            sudoku[row][column] = 0
    return False
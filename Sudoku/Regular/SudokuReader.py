def readSudoku(fn):

    sudoku = []

    file = open(fn, 'r')
    temp = file.read().splitlines()

    for line in temp:
        tempLine = []
        
        for number in line:
            tempLine.append(int(number))
            
        sudoku.append(tempLine) 

    file.close()
    return sudoku

print(readSudoku("Grid1.txt"))

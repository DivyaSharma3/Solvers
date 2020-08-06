class Node:

  def __init__(self, row, col):

    self.up = self.down = self.left = self.right = self
    self.col = col
    self.row = row

  def remove(self):
    self.up.down = self.down
    self.down.up = self.up
    self.col.size -= 1

  def add_back(self):
    self.up.down = self
    self.down.up = self
    self.col.size += 1

  def link_left(self, n):
    self.left = n
    self.left.right = self

  def __repr__(self):
    return f"Row: {self.row}, Col: {self.col.name}"


class ColumnNode(Node):

  def __init__(self, name):

    super().__init__(row=-1, col=self)
    self.name = name
    self.size = 0

  def remove(self):
    self.right.left = self.left
    self.left.right = self.right

  def add_back(self):
    self.right.left = self
    self.left.right = self

  def __repr__(self):
    return f"Column Header: {self.name}. Size: {self.size}"


class Matrix:

  def __init__(self, sudoku):

    self.root        = ColumnNode(0)
    self.column_list = self.make_column_list()

    self.sudoku_to_matrix(sudoku)

  def make_column_list(self, cols=324):

    head = self.root
    columns = [head] + [ ColumnNode(i) for i in range(1, cols + 1) ]

    # Create left/right links between column headers
    columns[-1].right = head
    columns[-1].left  = columns[-2]

    for i in range(cols):
      columns[i].right = columns[i + 1]
      columns[i].left  = columns[i - 1]

    return [ [col] for col in columns ]

  def sudoku_to_matrix(self, sudoku):
    
    size = len(sudoku)

    # Iterate through sudoku grid
    for i in range(size):
      for j in range(size):

        # If the square has a value, it only adds the row for that value
        # Otherwise, add 9 rows correspond to that cell having values 1-9
        square = sudoku[i][j]
        values = [square - 1] if square else range(size)

        for val in values:

          # Calculate row and columns for each constraint
          row_idx = (i * 81) + (j * 9) + val

          cell = (i * 9) + j
          row  = 81 + (i * 9) + val
          col  = 162 + (j * 9) + val
          box  = 243 + ( (i // 3) * 27 ) + ( (j // 3) * 9 ) + val
          
          cols  = [cell, row, col, box]
          nodes = [ Node(row_idx, self.column_list[x + 1][0]) for x in cols ]

          # Link all row nodes together and append to columns
          for k in range(4):
            nodes[k].link_left(nodes[k-1])

            self.column_list[cols[k] + 1].append(nodes[k])
            nodes[k].col.size += 1

    # Make all vertical links between nodes
    for column in self.column_list[1:]:

      for r in range(-1, column[0].size - 1):

        column[r].up      = column[r - 1]
        column[r].down    = column[r + 1]
        column[r].up.down = column[r]
        column[r].down.up = column[r]


class DLX():

  def __init__(self, matrix):
    self.solution = []
    self.matrix = matrix

  def choose_column(self):

    smallest = 792
    column   = None
    current  = self.matrix.root.right

    # Pick column with least rows
    while current != self.matrix.root:

      if current.size < smallest:

        column = current
        smallest = current.size

      current = current.right

    return column

  # Remove column from matrix, in addition to all rows in said column
  def cover(self, column):

    column.remove()
    r = column.down

    # Iterate down through rows in column
    while r != column:
      c = r.right

      # Remove all nodes from each row
      while c != r:
        c.remove()
        c = c.right

      r = r.down

  # Add column, and rows in column, back into the matrix
  def uncover(self, column):

    column.add_back()
    r = column.up

    # Iterate up through rows in column
    while r != column:
      c = r.left

      # Add back all nodes in each row
      while c != r:
        c.add_back()
        c = c.left

      r = r.up

  def solve(self):

    # If there are no columns left, the sudoku is solved
    if self.matrix.root == self.matrix.root.right:
      return True

    # Choose a columnd deterministically
    column = self.choose_column()
    self.cover(column)

    # Choose a row such that matrix[row][column] = 1
    i = column.down

    while i != column:


      j = i.right

      while j != i:
        self.cover(j.col)
        j = j.right

      if self.solve():
        self.solution.append(i)
        return True

      j = i.left

      while j != i:
        self.uncover(j.col)
        j = j.left
      
      i = i.down

    self.uncover(column)
    return False
  
  def solution_to_sudoku(self):

    # Make empty grid for result
    res = [[None for _ in range(9)] for _ in range(9)]

    for node in self.solution: 
      
      value   = node.row % 9 + 1
      row_idx = (node.row // 81)
      col_idx = int( (node.row - value + 1 - (row_idx * 81)) / 9 )

      res[row_idx][col_idx] = value

    return res

  def dance(self):

    if self.solve():
      return self.solution_to_sudoku()
    
    return []


def dots_to_grid(dot_str):

  grid = [[None for _ in range(9)] for _ in range(9)]

  for i in range(len(dot_str)):

    if dot_str[i] != '.':
      grid[i // 9][i % 9] = int(dot_str[i])
      
  return grid

if __name__ == "__main__":
    
    sudoku = input("Enter the sudoku string:\n")
    sudoku = dots_to_grid(sudoku)
    dlx    = DLX(Matrix(sudoku))
    res    = dlx.dance()
    for row in res:
      print(row)
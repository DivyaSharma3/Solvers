import numpy as np

def handle_input(inputs):

  width, height, columns, rows = inputs.split("\n")
  m, n = int(width), int(height)
  col_clues = [[int(n) for n in line.split(",")] for line in columns[1:-1].split('","')]
  row_clues = [[int(n) for n in line.split(",")] for line in rows[1:-1].split('","')]

  return n, m, row_clues, col_clues


class PicrossSolver():

  def __init__(self, n, m, rc, cc):
    
    self.picross = np.zeros([n, m])
    self.row_clues = rc
    self.col_clues = cc
    self.rows = n
    self.cols = m
    self.permutations = {}

  
  def make_row_split(self, clues, last, gaps):
  
    # Returns a list containing rows where only one clue is filled
    # For when multiple clues > gaps
    result = []

    # For each clue, make a row where only that clue is filled in
    for i in range(last + 1):

      # This clue won't have enough info to fill any squares
      if clues[i] <= gaps:
        continue

      row = []

      for j in range(last + 1):
        current = clues[j]

        # Only fills the clue that we want
        if i == j:
          row += [1] * current

        else:
          row += [0] * current

        # Add 1 square gap between clues
        # Or if it's the last clue, fill the row with gaps
        extra = 1 if j != last else gaps
        row += [0] * (extra)

      result.append(row)

    return result

  def match(self, fwd, bwd):
    # Performs logical and between elements of two rows
    return [x and y for x, y in zip(fwd, bwd)]

  def merge(self, clue, last, gaps):

    # Merges forwards and backwards pass 
    # (made with make_row_split) to find any
    # squares that can be filled with certainty

    fwd = self.make_row_split(clue, last, gaps)
    bwd = [i[::-1] for i in self.make_row_split(clue[::-1], last, gaps)][::-1]
    res = [self.match(f, b) for f, b in zip(fwd, bwd)]

    current = res[0]

    for i in res[1:]:
      temp = [x or y for x, y in zip(current, i)]
      current = temp

    return current

  def find_permutations(self, clue, m):

    # Find all permutations of a row for a given clue

    if (repr(clue), m) not in self.permutations:

      # clue size greater than permutation size
      if sum(clue) > m:
        return []

      # No clues, i.e. remainder of permutation filled with blanks
      if not clue:
        p = ["0" * m]
        return p

      # Only one clue left, and it fits the permutation size
      if len(clue) == 1 and m == clue[0]:
        p = ["1" * m]
        self.permutations[(repr(clue[0]), m)] = [x for x in p]
        return p

      start  = "1" * clue[0] + "0"
      filled = [ start + x for x in self.find_permutations(clue[1:], m - len(start)) ]
      gaps   = ["0" + x for x in self.find_permutations(clue, m - 1) ]

      if filled or gaps:
        self.permutations[(repr(clue), m)] = filled + gaps

      return filled + gaps

    else:
      return self.permutations[(repr(clue), m)]

  def solve_valid_perms(self, row, clue, size):

    current_perms = self.find_permutations(clue, size)
    valid_perms   = []
    
    for perm in current_perms:
      curr = [int(y) for y in perm]

      for w, x in zip(row, curr):

        # Invalid
        if (w == 1) and (w != x):
          break
        if w == -1 and x != 0:
          break

      # Valid permutation
      else:
        valid_perms.append(curr)

    res = valid_perms[0]

    # If square is filled/blank in all valid perms,
    # it must be part of the solution.
    for perm in valid_perms[1:]:
      res = [old if old == new else -1 for old, new in zip(res, perm)]

    # swap 0s and -1s; 
    # 0 should be unknown but represented "off" when making permutations
    res = [-1 if c == 0 else 0 if c == -1 else c for c in res]
    return res

  def solve_clues(self, picross, all_clues, n, m):

    for i in range(n):

      clues = all_clues[i]
      last  = len(clues) - 1
      info  = sum(clues)
      gaps  = m - info - last

      # Not enough info to fill new squares
      if info < (m + 1) / 2 or max(clues) <= gaps:
        continue

      # Entire row filled
      if info == m:
        res = np.ones(m)

      # Not enough info to fill whole row,
      # but some squares can be filled with certainty
      elif gaps:
        res = self.merge(clues, last, gaps)

      # Enough info to fill entire row
      else:
        res = []

        for j in range(last + 1):
          res += [1] * clues[j]

          if j != last:
            res.append(-1)

      row        = picross[i]
      result     = [q if p == 0 or q == -1 else p for p, q in zip(row, res)]
      picross[i] = result

    return picross

  def solve_picross(self):

    # Solve row and column clues
    pic = self.solve_clues(self.picross,self.row_clues, self.rows, self.cols)
    self.picross = self.solve_clues(pic.T, self.col_clues, self.cols, self.rows).T

    print("Clues solved")

    while 0 in self.picross:

      # Update rows
      for i in range(self.rows):
        row = self.picross[i]
        
        # Row already solved
        if 0 not in row:
          continue

        clue = self.row_clues[i]
        new  = self.solve_valid_perms(row, clue, self.cols)

        for j in range(self.cols):
          if new[j] != 0 and self.picross[i][j] != new[j]:
            self.picross[i][j] = new[j]

        if (sum(row) + (row == -1).sum()) == sum(clue):
          self.picross[i] = np.array([current if current != 0 else -1 for current in row])

      # Update columns
      for j in range(self.cols):
        col = self.picross.T[j]

        if 0 not in col:
          continue

        clue     = self.col_clues[j]
        new_col  = self.solve_valid_perms(col, clue, n)

        for i in range(self.rows):
          if new_col[i] != 0 and self.picross[i][j] != new_col[i]:
            self.picross[i][j] = new_col[i]

        if (sum(col) + (col == -1).sum()) == sum(clue):
          self.picross[:,j] = np.array([current if current != 0 else -1 for current in col])


    # picross = picross.astype('U1') 

    # Smart indexing! Replace -1 with 0 when displaying blanks in picross
    self.picross[self.picross == -1] = 0
    return self.picross.astype(int) 


if __name__ == "__main__":

  p1 = '''5
5
"5","2,2","1,1","2,2","5"
"5","2,2","1,1","2,2","5"'''

  p2 = '''8
11
"0","9","9","2,2","2,2","4","4","0"
"0","4","6","2,2","2,2","6","4","2","2","2","0"'''

  p3 = '''30
20
"1","1","2","4","7","9","2,8","1,8","8","1,9","2,7","3,4","6,4","8,5","1,11","1,7","8","1,4,8","6,8","4,7","2,4","1,4","5","1,4","1,5","7","5","3","1","1"
"8,7,5,7","5,4,3,3","3,3,2,3","4,3,2,2","3,3,2,2","3,4,2,2","4,5,2","3,5,1","4,3,2","3,4,2","4,4,2","3,6,2","3,2,3,1","4,3,4,2","3,2,3,2","6,5","4,5","3,3","3,3","1,1"'''

  p4 = '''30
30
"9,9","10,9","10,5,3","10,3,1","10,2,3","11,3","13,6","15,7","15,7","14,7","14,7","14,2,4","14,1,4","14,2,3","13,3,1","13,3","13,4","9,6,1","9,6,2","8,1,1,1,2,1","7,6,1","7,6","7,8","6,9","2,1,9","1,9","1,8","1,8","1,7","1,4,6"
"30","25","24,1","24,1","25,1","24,1","23","20,3,2","19,8","16,8","12,8","11,10","11,11","7,10","2,9","1,7","1,2,2","3","3","6","7","4,7","5","5,4","3,5","3,5","2,8","3,11","3,10,1","13,4"'''

  puzzles = [p1, p2, p3, p4]

  for p in puzzles:

    n, m, rc, cc = handle_input(p)
    ps = PicrossSolver(n, m, rc, cc)
    print(ps.solve_picross())
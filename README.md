# Solvers
Stuff I've written to solve puzzles.

## Picross

This program works by first solving the clues. Once the picross grid has been filled in with this informations, it goes through the rows and columns trying to fill in new squares. It does this by finding all valid permutations for the given rol/column, then finding which squares were filled in ALL valid permutations; these must be in the final solution.

## Sudoku

There are two programs for solving a Sudoku

### DLX

This program solves the sudoku by reducing it to an exact cover problem. It then uses [Dancing Links](https://en.wikipedia.org/wiki/Dancing_Links) and [Algorithm X](https://en.wikipedia.org/wiki/Knuth%27s_Algorithm_X) to solve it by backtracking. [Knuth's Paper.](https://arxiv.org/abs/cs/0011047v1)

### Regular

This program uses backtracking and brute force to solve the sudoku.

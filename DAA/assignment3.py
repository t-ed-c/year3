# Function to print the chessboard with queens placed
def print_board(board, n):
    for row in board:
        line = ""
        for col in range(n):
            line += "Q " if col == row else ". "
        print(line)
    print()

# Function to check if a queen can be safely placed
def is_safe(position, row, col):
    for i in range(row):
        # Check same column or diagonal conflicts
        if position[i] == col or \
           position[i] - i == col - row or \
           position[i] + i == col + row:
            return False
    return True

# Recursive backtracking function to place queens
def solve_n_queens_util(position, row, n, solutions):
    if row == n:
        # All queens placed successfully
        solutions.append(position[:])
        return
    for col in range(n):
        if is_safe(position, row, col):
            position[row] = col  # Place queen
            solve_n_queens_util(position, row + 1, n, solutions)

# Main function to start solving the problem
def solve_n_queens(n):
    position = [-1] * n  # Initialize positions
    solutions = []  # Store all valid solutions
    solve_n_queens_util(position, 0, n, solutions)
    print(f"Total solutions for {n}-Queens: {len(solutions)}")
    for sol in solutions:
        print_board(sol, n)  # Print each solution

# Input number of queens
n = int(input("Enter number of queens (n): "))
solve_n_queens(n)

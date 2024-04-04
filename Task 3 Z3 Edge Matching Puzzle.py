from z3 import *
import random

def generate_puzzle(n):
    """
    Generates a random edge matching puzzle of size n x n.
    Returns:
    edges: List of tuples representing edges (top, right, bottom, left)
    """
    edges = []
    for i in range(n):
        for j in range(n):
            top = random.randint(0, 1)
            right = random.randint(0, 1)
            bottom = random.randint(0, 1)
            left = random.randint(0, 1)
            edges.append((top, right, bottom, left))
    return edges

def solve_puzzle(edges, n):
    """
    Solves the edge matching puzzle using Z3.
    Args:
    edges: List of tuples representing edges (top, right, bottom, left)
    n: Size of the puzzle (n x n)
    """
    # Create a solver instance
    solver = Solver()

    # Define variables for each edge
    edge_vars = [[Bool(f"e_{i}_{j}") for j in range(n)] for i in range(n)]

    # Add constraints for matching edges
    for i in range(n):
        for j in range(n):
            top, right, bottom, left = edges[i*n + j]

            # Top edge constraint
            if i > 0:
                solver.add(edge_vars[i][j] == edge_vars[i-1][j] == (1 - top))

            # Right edge constraint
            if j < n - 1:
                solver.add(edge_vars[i][j] == edge_vars[i][j+1] == (1 - right))

            # Bottom edge constraint
            if i < n - 1:
                solver.add(edge_vars[i][j] == edge_vars[i+1][j] == (1 - bottom))

            # Left edge constraint
            if j > 0:
                solver.add(edge_vars[i][j] == edge_vars[i][j-1] == (1 - left))

    # Check if the solver can find a solution
    if solver.check() == sat:
        model = solver.model()
        solution = [[model.evaluate(edge_vars[i][j]) for j in range(n)] for i in range(n)]
        return solution
    else:
        return None

def print_solution(solution):
    """
    Prints the solution of the puzzle.
    Args:
    solution: List representing the solved puzzle
    """
    if solution is None:
        print("No solution found!")
        return
    for row in solution:
        print("".join("#" if cell else " " for cell in row))

# Example usage
n = 3  # Size of the puzzle
edges = generate_puzzle(n)
print("Generated puzzle:")
for i in range(n):
    for j in range(n):
        print(edges[i*n + j], end=" ")
    print()

print("\nSolving puzzle...")
solution = solve_puzzle(edges, n)
print("\nSolution:")
print_solution(solution)

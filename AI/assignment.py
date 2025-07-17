#we use backtracking to assign each guest to a table
# such that no two guests who cannot sit together are at the same table
def layout(N, C, L):
    from collections import defaultdict

    # Build an adjacency list to represent conflict relationships between guests
    # Each guest is mapped to a list of guests they cannot sit with
    conflict_graph = defaultdict(list)
    for a, b in L:
        conflict_graph[a].append(b)
        conflict_graph[b].append(a)

    # Dictionary to store the final assignment: guest -> table number
    assignment = {}

    # Helper function to check if assigning a guest to a table is valid
    def is_valid(guest, table):
        # Check all guests that current guest conflicts with
        for neighbor in conflict_graph[guest]:
            # If any conflicting guest is already on this table, it's not valid
            if assignment.get(neighbor) == table:
                return False
        return True

    # Backtracking function to try assigning tables to each guest
    def backtrack(guest_index):
        # Base case: all guests have been assigned successfully
        if guest_index == N:
            return True

        # Try placing the guest at each table from 0 to C-1
        for table in range(C):
            if is_valid(guest_index, table):
                # Assign this table to the guest
                assignment[guest_index] = table

                # Recursively assign the next guest
                if backtrack(guest_index + 1):
                    return True

                # If it didn’t work out, backtrack (remove the assignment)
                del assignment[guest_index]

        # If no table works for this guest, return False to trigger backtracking
        return False

    # Start the backtracking process from guest 0
    if backtrack(0):
        return assignment  # Return the valid assignment
    else:
        return False  # No valid arrangement is possible
# Example usage
print(layout(4, 2, [(0, 1), (1, 2), (2, 3)]))
# Expected output: A valid mapping like {0: 0, 1: 1, 2: 0, 3: 1}

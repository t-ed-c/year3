def layout(N, C, L):
    """
    Assign N guests to C tables such that conflicting guests don't sit together.
    
    Args:
        N: Number of guests (0, 1, 2, ..., N-1)
        C: Number of tables available
        L: List of conflict pairs [(guest1, guest2), ...]
    
    Returns:
        Dictionary {guest: table} or False if impossible
    """
    
    # Build conflict relationships - who can't sit with whom
    conflicts = {}
    for guest in range(N):
        conflicts[guest] = set()
    
    for a, b in L:
        conflicts[a].add(b)
        conflicts[b].add(a)
    
    # Track current table assignments
    tables = {}
    
    def can_sit_at_table(guest, table):
        """Check if guest can sit at table without conflicts"""
        for assigned_guest, assigned_table in tables.items():
            if assigned_table == table and assigned_guest in conflicts[guest]:
                return False
        return True
    
    def assign_guest(guest):
        """Try to assign current guest to a table"""
        if guest == N:  # All guests assigned successfully
            return True
            
        # Try each table for this guest
        for table in range(C):
            if can_sit_at_table(guest, table):
                tables[guest] = table
                
                if assign_guest(guest + 1):  # Try next guest
                    return True
                    
                del tables[guest]  # Backtrack - remove assignment
        
        return False  # No valid table found for this guest
    
    # Start with guest 0
    return tables if assign_guest(0) else False


# Test the function
print("Testing simplified layout function:")
result = layout(4, 2, [(0, 1), (1, 2), (2, 3)])
print(f"Result: {result}")

# Let's trace through this example:
# Guests: 0, 1, 2, 3
# Tables: 0, 1
# Conflicts: (0,1), (1,2), (2,3)
# 
# This means:
# - Guest 0 conflicts with Guest 1
# - Guest 1 conflicts with Guest 2  
# - Guest 2 conflicts with Guest 3
#
# Possible solution: {0: 0, 1: 1, 2: 0, 3: 1}
# Table 0: Guests 0, 2 (no conflict between them)
# Table 1: Guests 1, 3 (no conflict between them)

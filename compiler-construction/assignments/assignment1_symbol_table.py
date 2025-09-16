# Symbol Table Implementation using Python Dictionaries
# Compiler Construction - Assignment 1
# Date: September 16, 2025

class SymbolTable:
    def __init__(self):
        # Dictionary to hold symbols and their attributes
        self.table = {}

    def insert(self, name, symbol_type, scope, value=None):
        """Insert a new symbol into the table"""
        if name in self.table:
            print(f"Error: Symbol '{name}' already declared.")
        else:
            self.table[name] = {
                "type": symbol_type,
                "scope": scope,
                "value": value
            }
            print(f"Symbol '{name}' inserted successfully.")

    def lookup(self, name):
        """Retrieve symbol details"""
        return self.table.get(name, f"Error: Symbol '{name}' not found.")

    def update(self, name, value):
        """Update the value of an existing symbol"""
        if name in self.table:
            self.table[name]["value"] = value
            print(f"Symbol '{name}' updated successfully.")
        else:
            print(f"Error: Cannot update undeclared symbol '{name}'.")

    def delete(self, name):
        """Remove a symbol from the table"""
        if name in self.table:
            del self.table[name]
            print(f"Symbol '{name}' deleted successfully.")
        else:
            print(f"Error: Symbol '{name}' not found for deletion.")

    def display(self):
        """Display the symbol table"""
        print("\n" + "="*50)
        print("SYMBOL TABLE")
        print("="*50)
        if not self.table:
            print("Table is empty.")
        else:
            print(f"{'Symbol':<15} {'Type':<10} {'Scope':<10} {'Value':<15}")
            print("-"*55)
            for name, attrs in self.table.items():
                value = str(attrs["value"]) if attrs["value"] is not None else "None"
                print(f"{name:<15} {attrs['type']:<10} {attrs['scope']:<10} {value:<15}")
        print("="*50 + "\n")

    def get_symbols_by_scope(self, scope):
        """Get all symbols in a specific scope"""
        symbols = {name: attrs for name, attrs in self.table.items() 
                  if attrs["scope"] == scope}
        return symbols

    def get_symbols_by_type(self, symbol_type):
        """Get all symbols of a specific type"""
        symbols = {name: attrs for name, attrs in self.table.items() 
                  if attrs["type"] == symbol_type}
        return symbols


def main():
    """Demonstration of symbol table operations"""
    print("Compiler Construction - Assignment 1")
    print("Symbol Table Implementation\n")
    
    # Create symbol table instance
    st = SymbolTable()
    
    print("1. Inserting symbols:")
    # Insert symbols
    st.insert("x", "int", "global", 10)
    st.insert("y", "float", "local", 3.14)
    st.insert("func1", "function", "global")
    st.insert("z", "char", "local", 'A')
    st.insert("array1", "int[]", "global", [1, 2, 3, 4, 5])
    
    # Try to insert duplicate
    st.insert("x", "double", "local", 5.0)  # Should show error
    
    # Display table
    st.display()
    
    print("2. Looking up symbols:")
    # Lookup operations
    print("Looking up 'x':", st.lookup("x"))
    print("Looking up 'y':", st.lookup("y"))
    print("Looking up 'undeclared':", st.lookup("undeclared"))  # Should show error
    print()
    
    print("3. Updating symbol values:")
    # Update operations
    st.update("y", 6.28)
    st.update("z", 'B')
    st.update("undeclared", 100)  # Should show error
    
    # Display updated table
    st.display()
    
    print("4. Filtering symbols:")
    # Filter by scope
    print("Global symbols:", st.get_symbols_by_scope("global"))
    print("Local symbols:", st.get_symbols_by_scope("local"))
    print()
    
    # Filter by type
    print("Integer symbols:", st.get_symbols_by_type("int"))
    print("Function symbols:", st.get_symbols_by_type("function"))
    print()
    
    print("5. Deleting a symbol:")
    st.delete("z")
    st.delete("nonexistent")  # Should show error
    
    # Final display
    st.display()


if __name__ == "__main__":
    main()

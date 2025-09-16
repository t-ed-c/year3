# Assignment 1: Symbol Table Implementation

## Overview
Implement a symbol table using Python dictionaries to store and manage identifiers during the compilation process.

## Objective
- Understand the role of symbol tables in compiler design
- Implement basic symbol table operations
- Practice working with Python dictionaries for data management

## Requirements

### Core Operations
1. **Insert**: Add new symbols with their attributes
2. **Lookup**: Search for symbols and retrieve their information
3. **Update**: Modify existing symbol values
4. **Display**: Show the current state of the symbol table
5. **Delete**: Remove symbols from the table

### Symbol Attributes
Each symbol should store:
- **Name**: The identifier name
- **Type**: Data type (int, float, char, function, etc.)
- **Scope**: Where the symbol is accessible (global, local, etc.)
- **Value**: The current value (optional)

## Implementation Details

### Class Structure
```python
class SymbolTable:
    def __init__(self)
    def insert(self, name, symbol_type, scope, value=None)
    def lookup(self, name)
    def update(self, name, value)
    def delete(self, name)
    def display(self)
    def get_symbols_by_scope(self, scope)
    def get_symbols_by_type(self, symbol_type)
```

### Features Implemented
- ✅ Basic CRUD operations (Create, Read, Update, Delete)
- ✅ Error handling for duplicate declarations
- ✅ Error handling for undefined symbols
- ✅ Formatted table display
- ✅ Filtering by scope and type
- ✅ Comprehensive test cases

## Usage
```bash
python assignment1_symbol_table.py
```

## Sample Output
```
Compiler Construction - Assignment 1
Symbol Table Implementation

1. Inserting symbols:
Symbol 'x' inserted successfully.
Symbol 'y' inserted successfully.
Symbol 'func1' inserted successfully.
...

==================================================
SYMBOL TABLE
==================================================
Symbol          Type       Scope      Value     
--------------------------------------------------
x               int        global     10        
y               float      local      3.14      
func1           function   global     None      
...
```

## Test Cases
The program demonstrates:
1. Successful symbol insertion
2. Duplicate declaration error handling
3. Symbol lookup operations
4. Symbol value updates
5. Symbol deletion
6. Filtering operations
7. Error handling for undefined symbols

## Learning Outcomes
- Understanding symbol table data structures
- Practice with Python dictionaries
- Error handling in compiler components
- Basic compiler design principles

## Extension Ideas
- Implement nested scopes with scope stack
- Add type checking functionality
- Support for complex data types
- Integration with lexical analyzer output

## Files
- `assignment1_symbol_table.py` - Main implementation
- `README.md` - This documentation file

## Submission Requirements
- Working Python code with all required operations
- Proper error handling
- Test cases demonstrating functionality
- Code documentation and comments

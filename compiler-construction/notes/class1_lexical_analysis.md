# Class 1: Basic Lexical Analysis

## Overview
Lexical analysis is the first phase of compilation where the source code is broken down into tokens. A lexer (or scanner) reads the input character by character and groups them into meaningful tokens.

## What is a Token?
A token is the smallest meaningful unit in a programming language. Examples include:
- **Keywords**: `if`, `else`, `while`, `for`
- **Operators**: `+`, `-`, `*`, `/`, `=`
- **Identifiers**: Variable names, function names
- **Literals**: Numbers, strings
- **Delimiters**: `(`, `)`, `{`, `}`, `;`

## Basic Lexer Implementation

```python
def lexical_scanner(source_code):
    length = len(source_code)
    i = 0

    while i < length:
        current_char = source_code[i]

        # Skip whitespace
        if current_char.isspace():
            i += 1
            continue

        # Check for operators
        if current_char == '+':
            print("Token: PLUS Operator")
            i += 1
        elif current_char == '-':
            print("Token: MINUS Operator")
            i += 1
        elif current_char == '=':
            print("Token: ASSIGNMENT Operator")
            i += 1

        # Check for identifiers (keywords or variables)
        elif current_char.isalpha():
            identifier = ""
            while i < length and (source_code[i].isalnum()):  # Capture alphanumeric characters
                identifier += source_code[i]
                i += 1

            if identifier == "if":
                print("Token: IF Keyword")
            elif identifier == "else":
                print("Token: ELSE Keyword")
            else:
                print(f"Token: IDENTIFIER ({identifier})")

        # Check for numbers
        elif current_char.isdigit():
            number = ""
            while i < length and source_code[i].isdigit():  # Capture number
                number += source_code[i]
                i += 1
            print(f"Token: NUMBER ({number})")

        # Handle unrecognized characters
        else:
            print(f"Error: Unrecognized character '{current_char}'")
            i += 1

# Sample input for testing
source_code = "if x = 10 + y - 5 else q = m & 20 "
print("Lexical analysis of the source code:")
lexical_scanner(source_code)
```

## Explanation

### 1. Whitespace Handling
- **Purpose**: Skip over whitespace characters (spaces, tabs, newlines)
- **Implementation**: Python's `isspace()` method is used to identify whitespace
- **Action**: Increment position counter and continue to next character

```python
if current_char.isspace():
    i += 1
    continue
```

### 2. Token Identification
- **Structure**: Uses Python's `if-elif` structure to identify different token types
- **Categories**: 
  - Operators (`+`, `-`, `=`)
  - Keywords (`if`, `else`)
  - Identifiers (variable names)
  - Numbers (integer literals)

### 3. Identifiers and Numbers
- **Identifiers**: 
  - Use `isalpha()` to check if character starts an identifier
  - Use `isalnum()` to capture alphanumeric characters sequentially
  - Check against keyword list to distinguish keywords from variables

```python
elif current_char.isalpha():
    identifier = ""
    while i < length and (source_code[i].isalnum()):
        identifier += source_code[i]
        i += 1
```

- **Numbers**:
  - Use `isdigit()` to identify numeric characters
  - Read sequentially until non-digit character is found

```python
elif current_char.isdigit():
    number = ""
    while i < length and source_code[i].isdigit():
        number += source_code[i]
        i += 1
```

### 4. Error Handling
- **Purpose**: Handle unrecognized symbols
- **Action**: Report error and move to next character
- **Benefit**: Allows lexer to continue processing after encountering errors

```python
else:
    print(f"Error: Unrecognized character '{current_char}'")
    i += 1
```

## Sample Output
For the input: `"if x = 10 + y - 5 else q = m & 20 "`

```
Lexical analysis of the source code:
Token: IF Keyword
Token: IDENTIFIER (x)
Token: ASSIGNMENT Operator
Token: NUMBER (10)
Token: PLUS Operator
Token: IDENTIFIER (y)
Token: MINUS Operator
Token: NUMBER (5)
Token: ELSE Keyword
Token: IDENTIFIER (q)
Token: ASSIGNMENT Operator
Token: IDENTIFIER (m)
Error: Unrecognized character '&'
Token: NUMBER (20)
```

## Key Concepts

### 1. Sequential Processing
- The lexer processes input character by character from left to right
- Position is tracked using an index variable
- Characters are grouped into tokens based on their type

### 2. Lookahead
- For multi-character tokens (identifiers, numbers), the lexer looks ahead
- Continues reading until it finds a character that doesn't belong to the current token

### 3. Token Classification
- **Keywords vs Identifiers**: Keywords are reserved words with special meaning
- **Operators**: Single-character symbols with specific operations
- **Literals**: Constant values like numbers

## Limitations of This Basic Lexer

1. **Limited Operator Set**: Only handles `+`, `-`, `=`
2. **No String Literals**: Cannot process quoted strings
3. **Integer Only**: No support for floating-point numbers
4. **No Multi-character Operators**: Cannot handle `==`, `<=`, `>=`
5. **No Comments**: No support for comment recognition

## Extensions and Improvements

### 1. Enhanced Operator Support
```python
# Multi-character operators
if current_char == '=' and i + 1 < length and source_code[i + 1] == '=':
    print("Token: EQUALITY Operator")
    i += 2
```

### 2. Floating-Point Numbers
```python
# Handle decimal points in numbers
elif current_char.isdigit():
    number = ""
    has_decimal = False
    while i < length and (source_code[i].isdigit() or 
                         (source_code[i] == '.' and not has_decimal)):
        if source_code[i] == '.':
            has_decimal = True
        number += source_code[i]
        i += 1
```

### 3. String Literals
```python
# Handle quoted strings
elif current_char == '"':
    string_literal = ""
    i += 1  # Skip opening quote
    while i < length and source_code[i] != '"':
        string_literal += source_code[i]
        i += 1
    i += 1  # Skip closing quote
    print(f"Token: STRING ({string_literal})")
```

## Practice Exercises

1. **Extend the lexer** to recognize multiplication (`*`) and division (`/`) operators
2. **Add support for parentheses** `(` and `)`
3. **Implement floating-point number recognition**
4. **Add more keywords** like `while`, `for`, `return`
5. **Handle string literals** enclosed in quotes

## Next Steps
- Study regular expressions for pattern matching
- Learn about finite automata in lexical analysis
- Explore lexer generators like Lex/Flex
- Understand token data structures and attributes

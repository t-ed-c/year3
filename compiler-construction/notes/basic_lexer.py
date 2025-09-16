#!/usr/bin/env python3
"""
Basic Lexical Scanner - Class 1 Example
Compiler Construction Course

This is a simple lexer that recognizes:
- Keywords: if, else
- Operators: +, -, =
- Identifiers: variable names
- Numbers: integer literals
"""

def lexical_scanner(source_code):
    """
    Basic lexical scanner that tokenizes source code
    
    Args:
        source_code (str): The input source code to tokenize
    """
    length = len(source_code)
    i = 0
    tokens = []  # Store tokens for potential further processing

    print(f"Input: '{source_code}'")
    print("=" * 50)
    
    while i < length:
        current_char = source_code[i]

        # Skip whitespace
        if current_char.isspace():
            i += 1
            continue

        # Check for operators
        if current_char == '+':
            print("Token: PLUS Operator")
            tokens.append(("PLUS", "+"))
            i += 1
        elif current_char == '-':
            print("Token: MINUS Operator")
            tokens.append(("MINUS", "-"))
            i += 1
        elif current_char == '=':
            print("Token: ASSIGNMENT Operator")
            tokens.append(("ASSIGNMENT", "="))
            i += 1

        # Check for identifiers (keywords or variables)
        elif current_char.isalpha():
            identifier = ""
            start_pos = i
            while i < length and (source_code[i].isalnum() or source_code[i] == '_'):
                identifier += source_code[i]
                i += 1

            if identifier == "if":
                print("Token: IF Keyword")
                tokens.append(("IF", identifier))
            elif identifier == "else":
                print("Token: ELSE Keyword")
                tokens.append(("ELSE", identifier))
            else:
                print(f"Token: IDENTIFIER ({identifier})")
                tokens.append(("IDENTIFIER", identifier))

        # Check for numbers
        elif current_char.isdigit():
            number = ""
            while i < length and source_code[i].isdigit():
                number += source_code[i]
                i += 1
            print(f"Token: NUMBER ({number})")
            tokens.append(("NUMBER", number))

        # Handle unrecognized characters
        else:
            print(f"Error: Unrecognized character '{current_char}' at position {i}")
            tokens.append(("ERROR", current_char))
            i += 1
    
    print("=" * 50)
    return tokens


def main():
    """Main function to demonstrate the lexical scanner"""
    print("Basic Lexical Scanner - Class 1")
    print("Compiler Construction Course")
    print()
    
    # Test cases
    test_cases = [
        "if x = 10 + y - 5 else q = m & 20",
        "if score = 95 + bonus",
        "else result = total - deduction",
        "variable_name = 123 + another_var",
        "if total = x + y - z else final = 0"
    ]
    
    for i, source_code in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        tokens = lexical_scanner(source_code)
        print(f"Generated {len([t for t in tokens if t[0] != 'ERROR'])} valid tokens")
        error_count = len([t for t in tokens if t[0] == 'ERROR'])
        if error_count > 0:
            print(f"Found {error_count} error(s)")
        print()


if __name__ == "__main__":
    main()

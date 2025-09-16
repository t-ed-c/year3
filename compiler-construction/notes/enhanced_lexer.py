#!/usr/bin/env python3
"""
Enhanced Lexical Scanner - Extended Version
Compiler Construction Course

This enhanced lexer recognizes:
- Keywords: if, else, while, for, return, int, float
- Operators: +, -, *, /, =, ==, !=, <, >, <=, >=
- Identifiers: variable names (with underscores)
- Numbers: integers and floating-point
- Delimiters: (, ), {, }, ;
- String literals: "text"
"""

class Token:
    """Token class to represent lexical tokens"""
    def __init__(self, token_type, value, position):
        self.type = token_type
        self.value = value
        self.position = position
    
    def __repr__(self):
        return f"Token({self.type}, '{self.value}', pos:{self.position})"


class EnhancedLexer:
    """Enhanced lexical analyzer with more features"""
    
    def __init__(self):
        self.keywords = {
            'if': 'IF',
            'else': 'ELSE', 
            'while': 'WHILE',
            'for': 'FOR',
            'return': 'RETURN',
            'int': 'INT_TYPE',
            'float': 'FLOAT_TYPE'
        }
        
        self.operators = {
            '+': 'PLUS',
            '-': 'MINUS',
            '*': 'MULTIPLY',
            '/': 'DIVIDE',
            '=': 'ASSIGN',
            '==': 'EQUAL',
            '!=': 'NOT_EQUAL',
            '<': 'LESS_THAN',
            '>': 'GREATER_THAN',
            '<=': 'LESS_EQUAL',
            '>=': 'GREATER_EQUAL'
        }
        
        self.delimiters = {
            '(': 'LPAREN',
            ')': 'RPAREN',
            '{': 'LBRACE',
            '}': 'RBRACE',
            ';': 'SEMICOLON',
            ',': 'COMMA'
        }
    
    def scan(self, source_code):
        """Tokenize the source code"""
        tokens = []
        i = 0
        length = len(source_code)
        
        while i < length:
            # Skip whitespace
            if source_code[i].isspace():
                i += 1
                continue
            
            # Check for two-character operators first
            if i + 1 < length:
                two_char = source_code[i:i+2]
                if two_char in self.operators:
                    tokens.append(Token(self.operators[two_char], two_char, i))
                    i += 2
                    continue
            
            # Single character operators
            if source_code[i] in self.operators:
                char = source_code[i]
                tokens.append(Token(self.operators[char], char, i))
                i += 1
                continue
            
            # Delimiters
            if source_code[i] in self.delimiters:
                char = source_code[i]
                tokens.append(Token(self.delimiters[char], char, i))
                i += 1
                continue
            
            # String literals
            if source_code[i] == '"':
                start_pos = i
                i += 1  # Skip opening quote
                string_value = ""
                while i < length and source_code[i] != '"':
                    string_value += source_code[i]
                    i += 1
                if i < length:
                    i += 1  # Skip closing quote
                    tokens.append(Token('STRING', string_value, start_pos))
                else:
                    tokens.append(Token('ERROR', f'Unterminated string at position {start_pos}', start_pos))
                continue
            
            # Numbers (integers and floats)
            if source_code[i].isdigit():
                start_pos = i
                number = ""
                has_decimal = False
                
                while i < length and (source_code[i].isdigit() or 
                                    (source_code[i] == '.' and not has_decimal)):
                    if source_code[i] == '.':
                        has_decimal = True
                    number += source_code[i]
                    i += 1
                
                token_type = 'FLOAT' if has_decimal else 'INTEGER'
                tokens.append(Token(token_type, number, start_pos))
                continue
            
            # Identifiers and keywords
            if source_code[i].isalpha() or source_code[i] == '_':
                start_pos = i
                identifier = ""
                
                while i < length and (source_code[i].isalnum() or source_code[i] == '_'):
                    identifier += source_code[i]
                    i += 1
                
                # Check if it's a keyword
                token_type = self.keywords.get(identifier, 'IDENTIFIER')
                tokens.append(Token(token_type, identifier, start_pos))
                continue
            
            # Unrecognized character
            tokens.append(Token('ERROR', source_code[i], i))
            i += 1
        
        return tokens
    
    def print_tokens(self, tokens, source_code):
        """Print tokens in a formatted way"""
        print(f"Source: '{source_code}'")
        print("-" * 60)
        print(f"{'Type':<15} {'Value':<15} {'Position':<10}")
        print("-" * 60)
        
        for token in tokens:
            print(f"{token.type:<15} {token.value:<15} {token.position:<10}")
        
        valid_tokens = [t for t in tokens if t.type != 'ERROR']
        error_tokens = [t for t in tokens if t.type == 'ERROR']
        
        print("-" * 60)
        print(f"Total tokens: {len(tokens)} | Valid: {len(valid_tokens)} | Errors: {len(error_tokens)}")
        if error_tokens:
            print("Errors found:")
            for error in error_tokens:
                print(f"  - {error.value} at position {error.position}")
        print()


def main():
    """Demonstrate the enhanced lexer"""
    print("Enhanced Lexical Scanner")
    print("Compiler Construction Course")
    print("=" * 60)
    
    lexer = EnhancedLexer()
    
    test_cases = [
        'if (x == 10.5) { return x + y; }',
        'while (i < count) { sum = sum + arr[i]; }',
        'float result = (a * b) / c;',
        'if (name == "John") { print("Hello"); }',
        'for (int i = 0; i <= 100; i++) { total += i; }'
    ]
    
    for i, source in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        tokens = lexer.scan(source)
        lexer.print_tokens(tokens, source)


if __name__ == "__main__":
    main()

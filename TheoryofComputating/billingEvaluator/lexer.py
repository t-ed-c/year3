import ply.lex as lex

# List of token names
tokens = (
    'ID', 'NUMBER',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'ASSIGN',
    'LPAREN', 'RPAREN',
    'QUESTION', 'COLON',
    'LT', 'GT', 'LE', 'GE', 'EQ', 'NE',
    'AND', 'OR', 'NOT', 'COMMA',
)

# Regular expressions for simple tokens
t_PLUS     = r'\+'
t_MINUS    = r'-'
t_TIMES    = r'\*'
t_DIVIDE   = r'/'
t_ASSIGN   = r'='
t_LPAREN   = r'\('
t_RPAREN   = r'\)'
t_QUESTION = r'\?'
t_COLON    = r':'
t_LT       = r'<'
t_GT       = r'>'
t_LE       = r'<='
t_GE       = r'>='
t_EQ       = r'=='
t_NE       = r'!='
t_AND      = r'&&'
t_OR       = r'\|\|'
t_NOT      = r'!'
t_COMMA    = r','


# Rules for identifiers and numbers
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

# Ignore spaces and tabs
t_ignore = ' \t'

# Track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Test code
if __name__ == '__main__':
    data = 'total = base + (units * rate) + (isPeak ? surcharge : 0);'
    lexer.input(data)
    for token in lexer:
        print(token)

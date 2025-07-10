import ply.yacc as yacc
from lexer import tokens
from graphviz import Digraph

symbol_table = {}
graph = Digraph(format='png')
node_count = 0

def fetchTariff():
    return 12.5  # Placeholder value for testing

def forecast(units):
    return units * 1.1 + 50  # Simulated formula for prediction

def new_node(label):
    global node_count
    node_id = f"node{node_count}"
    graph.node(node_id, label)
    node_count += 1
    return node_id

def p_statement_assign(p):
    'statement : ID ASSIGN expression'
    symbol_table[p[1]] = p[3][1]
    print(f"{p[1]} = {p[3][1]}")
    root = new_node(f"{p[1]} =")
    graph.edge(root, p[3][0])
    graph.render('expression_tree', view=True)

def p_statement_expr(p):
    'statement : expression'
    print(p[1][1])
    graph.render('expression_tree', view=True)

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression GT expression
                  | expression LT expression
                  | expression GE expression
                  | expression LE expression
                  | expression EQ expression
                  | expression NE expression
                  | expression AND expression
                  | expression OR expression'''
    result = eval_binary(p[2], p[1][1], p[3][1])
    node = new_node(p[2])
    graph.edge(node, p[1][0])
    graph.edge(node, p[3][0])
    p[0] = (node, result)

def p_expression_ternary(p):
    'expression : expression QUESTION expression COLON expression'
    result = p[3][1] if p[1][1] else p[5][1]
    node = new_node('?')
    graph.edge(node, p[1][0])
    graph.edge(node, p[3][0])
    graph.edge(node, p[5][0])
    p[0] = (node, result)

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    node = new_node(str(p[1]))
    p[0] = (node, p[1])

def p_expression_id(p):
    'expression : ID'
    value = symbol_table.get(p[1], 0)
    node = new_node(p[1])
    p[0] = (node, value)

def p_expression_not(p):
    'expression : NOT expression'
    result = not p[2][1]
    node = new_node('!')
    graph.edge(node, p[2][0])
    p[0] = (node, result)

def p_expression_function_call(p):
    'expression : ID LPAREN expression RPAREN'
    func_name = p[1]
    arg_value = p[3][1]
    
    if func_name == 'fetchTariff':
        result = fetchTariff()
    elif func_name == 'forecast':
        result = forecast(arg_value)
    else:
        print(f"⚠️ Error: Unknown function '{func_name}'")
        result = 0

    node = new_node(f"{func_name}()")
    graph.edge(node, p[3][0])
    p[0] = (node, result)
    
def p_expression_function_call_no_args(p):
    'expression : ID LPAREN RPAREN'
    func_name = p[1]

    if func_name == 'fetchTariff':
        result = fetchTariff()
    else:
        print(f"⚠️ Error: Unknown function '{func_name}'")
        result = 0

    node = new_node(f"{func_name}()")
    p[0] = (node, result)


def p_error(p):
    print(f"Syntax error at {p.value}" if p else "Syntax error at EOF")

def eval_binary(op, left, right):
    try:
        # Auto-convert bool to int for arithmetic
        if isinstance(left, bool): left = int(left)
        if isinstance(right, bool): right = int(right)

        # Promote to float if any operand is float
        if isinstance(left, float) or isinstance(right, float):
            left = float(left)
            right = float(right)

        if op == '+': return left + right
        if op == '-': return left - right
        if op == '*': return left * right
        if op == '/':
            if right == 0:
                print("⚠️ Error: Division by zero")
                return 0
            return left / right
        if op == '>': return left > right
        if op == '<': return left < right
        if op == '>=': return left >= right
        if op == '<=': return left <= right
        if op == '==': return left == right
        if op == '!=': return left != right
        if op == '&&': return bool(left) and bool(right)
        if op == '||': return bool(left) or bool(right)
    except Exception as e:
        print(f"Runtime Error: {e}")
        return 0


# Build parser
parser = yacc.yacc()

# Run loop
if __name__ == '__main__':
    while True:
        try:
            s = input('>>> ')
        except EOFError:
            break
        if not s: continue
        graph = Digraph(format='png')  # Reset graph per expression
        node_count = 0
        parser.parse(s)

# Based on example from https://github.com/dabeaz/ply/blob/3.11/README.md
# Uses "ply" - Python Lex Yacc
# Install with: python -m pip install ply

import ply.lex as lex
import ply.yacc as yacc

class grammar:
    tokens = (
        'NUMBER',
        'PLUS','TIMES',
        'LPAREN','RPAREN',
        'NEWLINE',
        )

    # Tokens

    t_PLUS   = r'\+'
    t_TIMES  = r'\*'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_NEWLINE = r'[\r\n]+'

    def t_NUMBER(t):
        r'\d+'
        t.value = int(t.value)
        return t

    # Ignored characters
    t_ignore = r" "

    def t_error(t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Precedence rules for the arithmetic operators
    precedence = (
        ('left','TIMES','PLUS'),
        )

    def p_root_expr(p):
        'root : list'
        p[0] = p[0] = p[1]

    def p_list_expr(p):
        '''list : expression NEWLINE list
                | expression NEWLINE
                | expression'''
        if len(p) > 3:
            p[0] = p[1] + p[3]
        else:
            p[0] = p[1]

    def p_expression_binop(p):
        '''expression : expression PLUS expression
                      | expression TIMES expression'''
        if p[2] == '+':
            p[0] = p[1] + p[3]
        elif p[2] == '*':
            p[0] = p[1] * p[3]
        else:
            assert False

    def p_expression_group(p):
        'expression : LPAREN expression RPAREN'
        p[0] = p[2]

    def p_expression_number(p):
        'expression : NUMBER'
        p[0] = p[1]

    def p_error(p):
        if p is None:
            print("Syntax error (p is None)")
        else:
            print("Syntax error at '%s'" % p.value)

def calculate(expr):
    lex.lex(module=grammar)
    yacc.yacc(debug=False, module=grammar)
    return yacc.parse(expr)

if __name__ == "__main__":
    print(calculate(open("input", "rt").read()))

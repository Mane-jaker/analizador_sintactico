from ply import yacc

def p_for_statement(p):
    'for_statement : FOR LPAREN init_statement condition_statement increment_statement RPAREN BLOCK'
    print("Bucle 'for' encontrado")

def p_init_statement(p):
    'init_statement : ID ASSIGN NUMBER SEMICOLON'
    print("Instrucción de inicialización encontrada")

def p_condition_statement(p):
    'condition_statement : ID LEQ NUMBER SEMICOLON'
    print("Instrucción de condición encontrada")

def p_increment_statement(p):
    'increment_statement : ID ASSIGN ID PLUS PLUS SEMICOLON'
    print("Instrucción de incremento encontrada")

def p_BLOCK(p):
    'BLOCK : LBRACE statements RBRACE'
    pass

def p_statements(p):
    'statements : statement statements'
    pass

def p_statement(p):
    '''statement : ID ASSIGN NUMBER SEMICOLON
                   | ID PRINTF LPAREN STRING RPAREN SEMICOLON'''
    pass

def p_STRING(t):
    r'"[^"]+"'
    return t

def p_error(p):
    print("Error de sintaxis en '%s'" % p.value)

parser = yacc.yacc()
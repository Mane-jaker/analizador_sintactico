from ply import lex
from ply import yacc
from difflib import SequenceMatcher

# Palabras reservadas originales
reserved = {
    'for': 'FOR',
    'int': 'INT',
    'system': 'SYSTEM',
    'out': 'OUT',
    'println': 'PRINTLN'
}

tokens = [
    'ID',
    'NUMBER',
    'LPAREN',
    'RPAREN',
    'SEMICOLON',
    'LBRACE',
    'RBRACE',
    'ASSIGN', 
    'LTE',
    'PLUS',
    'DOT',
    'DOUBLEQUOTE',
    'COLON'
] + list(reserved.values())

t_NUMBER = r'[0-9]+'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMICOLON = r';'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_ASSIGN = r'='
t_LTE = r'<='
t_PLUS = r'\+'
t_DOT = r'\.'
t_DOUBLEQUOTE = r'"'
t_COLON = r':'

def t_id(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t

def similar_to_reserved(word):
    all_reserved = set(python_reserved) | set(java_reserved) | set(cpp_reserved) | set(reserved.values())
    for reserved_word in all_reserved:
        if SequenceMatcher(None, word, reserved_word).ratio() > 0.8:
            return True
    return False

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# Definición del analizador sintáctico
def p_program(p):
    '''program : declaration statement
               | statement'''
    p[0] = p[1:]

def p_declaration(p):
    'declaration : INT ID SEMICOLON'
    parser_state.symbols[p[2]] = 'int'
    p[0] = ('declaration', p[2])

def p_statement_for(p):
    'statement : FOR LPAREN ID ASSIGN NUMBER SEMICOLON ID LTE NUMBER SEMICOLON ID PLUS PLUS RPAREN LBRACE SYSTEM DOT OUT DOT PRINTLN LPAREN ID RPAREN SEMICOLON RBRACE'
    if p[3] not in parser_state.symbols:
        semantic_error_msg = f"Error: variable '{p[3]}' no declarada"
        print(semantic_error_msg)
        parser_state.last_semantic_error = semantic_error_msg
        return
    elif parser_state.symbols[p[3]] != 'int':
        semantic_error_msg = f"Error: variable '{p[3]}' no es de tipo int"
        print(semantic_error_msg)
        parser_state.last_semantic_error = semantic_error_msg
        return
    print("Se reconoció una sentencia for.")
    p[0] = "Se reconoció una sentencia for."

def p_statement_println(p):
    'statement : SYSTEM DOT OUT DOT PRINTLN LPAREN ID RPAREN SEMICOLON'
    if p[7] not in parser_state.symbols:
        semantic_error_msg = f"Error: variable '{p[7]}' no declarada"
        print(semantic_error_msg)
        parser_state.last_semantic_error = semantic_error_msg
        return
    p[0] = ('println_statement', p[7])
    
def p_error(p):
    if p:
        error_msg = f"Error de sintaxis en '{p.value}' en la línea {p.lineno} y posición {p.lexpos}"
        print(error_msg)
        parser_state.last_error = error_msg
    else:
        error_msg = "Error de sintaxis al final del archivo"
        print(error_msg)
        parser_state.last_error = error_msg

# Clase ParserState
class ParserState:
    def __init__(self):
        self.lexer = lex.lex()
        self.parser = yacc.yacc()
        self.last_error = None
        self.last_semantic_error = None
        self.symbols = {}
    
    def reset_lexer(self):
        self.lexer.lineno = 1

    def parse(self, text):
        self.reset_lexer() 
        self.lexer.input(text)
        self.last_error = None
        self.last_semantic_error = None
        self.symbols.clear()
        try:
            result = self.parser.parse(lexer=self.lexer)
            return result
        except Exception as e:
            self.last_error = str(e)
            return None

# Inicialización del parser
parser_state = ParserState()



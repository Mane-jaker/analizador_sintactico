from ply import lex
from difflib import SequenceMatcher

# Palabras reservadas comunes a Python, Java y C++
common_reserved = {
    'if', 'else', 'for', 'while', 'break', 'continue', 'return', 'do'
}

# Lista ampliada de palabras reservadas específicas de Python
python_reserved = {
    'def', 'import', 'pass', 'raise', 'True', 'False', 'None', 'lambda', 'try', 'except', 'finally', 'as', 'with'
} | common_reserved

# Lista ampliada de palabras reservadas específicas de Java
java_reserved = {
    'class', 'public', 'static', 'void', 'true', 'false', 'null', 'try', 'catch', 'finally', 'interface', 'extends', 'implements'
} | common_reserved

# Lista ampliada de palabras reservadas específicas de C++
cpp_reserved = {
    'include', 'using', 'namespace', 'template', 'true', 'false', 'nullptr', 'class', 'try', 'catch', 'throw'
} | common_reserved

# Tus palabras reservadas originales
reserved = {
    'for': 'FOR',
    'if': 'IF',
    'do': 'DO',
    'while': 'WHILE',
    'else': 'ELSE',
    'programa': 'PROGRAMA' ,
    'read': 'READ', 
    'int' : 'INT',
    'printf': 'PRINTF'
}

tokens = [
    'ID',
    'LPAREN',
    'RPAREN',
    'SEMICOLON',
    'COMMA',
    'LBRACE',
    'RBRACE',
    'ERROR',
    'PYTHON_RESERVED',  # Token para palabras reservadas de Python
    'JAVA_RESERVED',    # Token para palabras reservadas de Java
    'CPP_RESERVED'      # Token para palabras reservadas de C++
] + list(reserved.values())

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMICOLON = r';'
t_COMMA = r','
t_LBRACE = r'\{'
t_RBRACE = r'\}'

def t_id(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    elif t.value in python_reserved:
        t.type = 'PYTHON_RESERVED'
    elif t.value in java_reserved:
        t.type = 'JAVA_RESERVED'
    elif t.value in cpp_reserved:
        t.type = 'CPP_RESERVED'
    else:
        t.type = 'ID'
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

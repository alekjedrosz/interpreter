import ply.lex as lex

from errors import error


reserved = {
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT',
    'true': 'BOOL',
    'false': 'BOOL',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'do': 'DO',
    'print': 'PRINT',
    'readint': 'READINT',
    'readstr': 'READSTR',
    'substring': 'SUBSTR',
    'length': 'LEN',
    'position': 'POS',
    'concatenate': 'CONCAT',
    'begin': 'BEGIN',
    'end': 'END',
    'exit': 'EXIT'
}

tokens = ['PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',
          'EQUALS', 'LT', 'LE', 'GT', 'GE', 'NE',
          'STREQ', 'STRNOTEQ',
          'LPAREN', 'RPAREN', 'SEMI', 'COMMA',
          'ASSIGN',
          'NUM', 'IDENT', 'STRING'
          ] + list(set(reserved.values()))

t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
t_EQUALS = r'='
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_NE = r'<>'
t_STREQ = r'=='
t_STRNOTEQ = r'!='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMI = r';'
t_COMMA = r','
t_ASSIGN = r':='

t_ignore = ' \t'


def t_NUM(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t


def t_STRING(t):
    r'\".*?\"'
    t.value = t.value[1:-1]
    return t


def t_BOOL(t):
    r'true|false'
    t.value = True if t.value == 'true' else False
    return t


def t_IDENT(t):
    r'[_A-Za-z][_A-Za-z0-9]*'
    t.type = reserved.get(t.value, 'IDENT')
    return t


def t_newline(t):
    r'\n'
    t.lexer.lineno += 1


def t_eof(t):
    return None


def t_error(t):
    error(t.lexer.lineno, f"Invalid character '{t.value}'")
    t.lexer.skip(1)


lex.lex()

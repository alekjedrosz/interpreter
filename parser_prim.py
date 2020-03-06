import ply.yacc as yacc

import lexer_prim
import ast
from errors import error

tokens = lexer_prim.tokens

# Lowest to highest precedence

precedence = (
    ('nonassoc', 'ELSE'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'EQUALS', 'LT', 'LE', 'GT', 'GE', 'NE'),
    ('right', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
    ('right', 'UMINUS'),
    ('right', 'NOT')
)


# Program

def p_program(p):
    '''program : instr'''
    p[0] = ast.Program(p[1])


# Instructions

def p_instr_chain(p):
    '''instr : instr SEMI simple_instr'''
    p[0] = p[1]
    p[0].simple_instr_list.append(p[3])


def p_instr_single(p):
    '''instr : simple_instr'''
    p[0] = ast.Instr([p[1]])


def p_simple_instr(p):
    '''simple_instr : assign_stmt
                    | if_stmt
                    | while_stmt
                    | output_stmt'''
    p[0] = p[1]


def p_simple_instr_exit(p):
    '''simple_instr : EXIT'''
    p[0] = ast.ExitStmt()


def p_simple_instr_block(p):
    '''simple_instr : BEGIN instr END'''
    p[0] = ast.InstrBlock(p[2])


# Assign statement

def p_assign_stmt(p):
    '''assign_stmt : IDENT ASSIGN expr'''
    p[0] = ast.AssignStmt(p[1], p[3])


# Expressions

def p_expr(p):
    '''expr : num_expr
            | str_expr'''
    p[0] = p[1]


def p_expr_ident(p):
    '''expr : IDENT'''
    p[0] = ast.Ident(p[1])


# Num expressions

def p_num_expr_literal(p):
    '''num_expr : NUM'''
    p[0] = ast.Literal(p[1])


def p_num_expr_readint(p):
    '''num_expr : READINT'''
    p[0] = ast.ReadintExpr()


def p_num_expr_unary(p):
    '''num_expr : MINUS expr %prec UMINUS'''
    p[0] = ast.UnaryExpr(p[2])


def p_num_expr_binop(p):
    '''num_expr : expr PLUS expr
                | expr MINUS expr
                | expr TIMES expr
                | expr DIVIDE expr
                | expr MOD expr'''
    p[0] = ast.BinopExpr(p[1], p[2], p[3])


def p_num_expr_group(p):
    '''num_expr : LPAREN expr RPAREN'''
    p[0] = ast.GroupingExpr(p[2])


def p_num_expr_len(p):
    '''num_expr : LEN LPAREN expr RPAREN'''
    p[0] = ast.LenExpr(p[3])


def p_num_expr_pos(p):
    '''num_expr : POS LPAREN expr COMMA expr RPAREN'''
    p[0] = ast.PosExpr(p[3], p[5])


# String expressions

def p_str_expr_literal(p):
    '''str_expr : STRING'''
    p[0] = ast.Literal(p[1])


def p_str_expr_readstr(p):
    '''str_expr : READSTR'''
    p[0] = ast.ReadstrExpr()


def p_str_expr_concat(p):
    '''str_expr : CONCAT LPAREN expr COMMA expr RPAREN'''
    p[0] = ast.ConcatExpr(p[3], p[5])


def p_str_expr_substr(p):
    '''str_expr : SUBSTR LPAREN expr COMMA expr COMMA expr RPAREN'''
    p[0] = ast.SubstrExpr(p[3], p[5], p[7])


# Control flow statements

def p_if_stmt(p):
    '''if_stmt : IF bool_expr THEN simple_instr'''
    p[0] = ast.IfStmt(p[2], p[4])


def p_if_stmt_else(p):
    '''if_stmt : IF bool_expr THEN simple_instr ELSE simple_instr'''
    p[0] = ast.IfStmt(p[2], p[4], p[6])


def p_while_stmt(p):
    '''while_stmt : WHILE bool_expr DO simple_instr'''
    p[0] = ast.WhileStmt(p[2], p[4])


def p_while_stmt_do(p):
    '''while_stmt : DO simple_instr WHILE bool_expr'''
    p[0] = ast.WhileStmt(p[4], p[2], do_while=True)


# Boolean expressions

def p_bool_expr_literal(p):
    '''bool_expr : BOOL'''
    p[0] = ast.Literal(p[1])


def p_bool_expr_group(p):
    '''bool_expr : LPAREN bool_expr RPAREN'''
    p[0] = ast.GroupingExpr(p[2])


def p_bool_expr_not(p):
    '''bool_expr : NOT bool_expr'''
    p[0] = ast.NotExpr(p[2])


def p_bool_expr_boolop(p):
    '''bool_expr : bool_expr AND bool_expr
                 | bool_expr OR bool_expr'''
    p[0] = ast.BoolopExpr(p[1], p[2], p[3])


def p_bool_expr_num_relop(p):
    '''bool_expr : expr num_rel expr'''
    p[0] = ast.NumRelopExpr(p[1], p[2], p[3])


def p_bool_expr_str_relop(p):
    '''bool_expr : expr str_rel expr'''
    p[0] = ast.StrRelopExpr(p[1], p[2], p[3])


def p_num_rel(p):
    '''num_rel : EQUALS
               | LT
               | LE
               | GT
               | GE
               | NE'''
    p[0] = p[1]


def p_str_rel(p):
    '''str_rel : STREQ
               | STRNOTEQ'''
    p[0] = p[1]


# Output statement

def p_output_stmt(p):
    '''output_stmt : PRINT LPAREN expr RPAREN'''
    p[0] = ast.PrintStmt(p[3])


# Syntax error "handling"
def p_error(p):
    if p:
        error(p.lineno, f'Syntax error at token \'{p.value}\'')
    else:
        print('EOF - no more input')


def make_parser():
    parser = yacc.yacc()
    return parser

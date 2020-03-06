from abc import ABC, abstractmethod


class Node(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass

    def __repr__(self):
        attr = [(a, str(getattr(self, a))) for a in self.__dict__]
        return "<{}: {}>".format(self.__class__.__name__,
                                 "; ".join(["{}={}".format(a[0], a[1]) for a in attr]))


class Program(Node):
    def __init__(self, instr):
        self.instr = instr

    def accept(self, visitor):
        return visitor.visit_program(self)


# Instructions

class Instr(Node):
    def __init__(self, simple_instr_list):
        self.simple_instr_list = simple_instr_list

    def accept(self, visitor):
        return visitor.visit_instr(self)


class InstrBlock(Node):
    def __init__(self, instr):
        self.instr = instr

    def accept(self, visitor):
        return visitor.visit_instr_block(self)


class ExitStmt(Node):
    def __init__(self):
        pass

    def accept(self, visitor):
        return visitor.visit_exit_stmt(self)


# Assign statement

class AssignStmt(Node):
    def __init__(self, ident, expr):
        self.ident = ident
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_assign_stmt(self)


# Expressions

class Ident(Node):
    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        return visitor.visit_ident(self)


class Literal(Node):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal(self)


# Num expressions

class ReadintExpr(Node):
    def __init__(self):
        pass

    def accept(self, visitor):
        return visitor.visit_readint_expr(self)


class UnaryExpr(Node):
    def __init__(self, num_expr):
        self.num_expr = num_expr

    def accept(self, visitor):
        return visitor.visit_unary_expr(self)


class BinopExpr(Node):
    def __init__(self, num_expr0, op, num_expr1):
        self.num_expr0 = num_expr0
        self.op = op
        self.num_expr1 = num_expr1

    def accept(self, visitor):
        return visitor.visit_binop_expr(self)


class GroupingExpr(Node):
    def __init__(self, num_expr):
        self.num_expr = num_expr

    def accept(self, visitor):
        return visitor.visit_grouping_expr(self)


class LenExpr(Node):
    def __init__(self, str_expr):
        self.str_expr = str_expr

    def accept(self, visitor):
        return visitor.visit_len_expr(self)


class PosExpr(Node):
    def __init__(self, str_expr0, str_expr1):
        self.str_expr0 = str_expr0
        self.str_expr1 = str_expr1

    def accept(self, visitor):
        return visitor.visit_pos_expr(self)


# String expressions

class ReadstrExpr(Node):
    def __init__(self):
        pass

    def accept(self, visitor):
        return visitor.visit_readstr_expr(self)


class ConcatExpr(Node):
    def __init__(self, str_expr0, str_expr1):
        self.str_expr0 = str_expr0
        self.str_expr1 = str_expr1

    def accept(self, visitor):
        return visitor.visit_concat_expr(self)


class SubstrExpr(Node):
    def __init__(self, str_expr, num_expr0, num_expr1):
        self.str_expr = str_expr
        self.num_expr0 = num_expr0
        self.num_expr1 = num_expr1

    def accept(self, visitor):
        return visitor.visit_substr_expr(self)


# Control flow statements

class IfStmt(Node):
    def __init__(self, cond, true_simple_instr, else_simple_instr=None):
        self.cond = cond
        self.true_simple_instr = true_simple_instr
        self.else_simple_instr = else_simple_instr

    def accept(self, visitor):
        return visitor.visit_if_stmt(self)


class WhileStmt(Node):
    def __init__(self, cond, simple_instr, do_while=False):
        self.cond = cond
        self.simple_instr = simple_instr
        self.do_while = do_while

    def accept(self, visitor):
        return visitor.visit_while_stmt(self)


# Boolean expressions

class NotExpr(Node):
    def __init__(self, bool_expr):
        self.bool_expr = bool_expr

    def accept(self, visitor):
        return visitor.visit_not_expr(self)


class BoolopExpr(Node):
    def __init__(self, bool_expr0, bool_op, bool_expr1):
        self.bool_expr0 = bool_expr0
        self.bool_op = bool_op
        self.bool_expr1 = bool_expr1

    def accept(self, visitor):
        return visitor.visit_boolop_expr(self)


class NumRelopExpr(Node):
    def __init__(self, num_expr0, num_rel, num_expr1):
        self.num_expr0 = num_expr0
        self.num_rel = num_rel
        self.num_expr1 = num_expr1

    def accept(self, visitor):
        return visitor.visit_num_relop_expr(self)


class StrRelopExpr(Node):
    def __init__(self, str_expr0, str_rel, str_expr1):
        self.str_expr0 = str_expr0
        self.str_rel = str_rel
        self.str_expr1 = str_expr1

    def accept(self, visitor):
        return visitor.visit_str_relop_expr(self)


# Output statement

class PrintStmt(Node):
    def __init__(self, expr):
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_print_stmt(self)

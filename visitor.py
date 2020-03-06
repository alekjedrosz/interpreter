from abc import ABC, abstractmethod
import inspect


def decorate_all_methods(decorator_fn):
    def decorate(cls):
        for name, fn in inspect.getmembers(cls, predicate=inspect.isfunction):
            setattr(cls, name, decorator_fn(fn))
        return cls
    return decorate


@decorate_all_methods(abstractmethod)
class Visitor(ABC):
    def visit_program(self, program):
        pass

    def visit_instr(self, instr):
        pass

    def visit_instr_block(self, instr_block):
        pass

    def visit_exit_stmt(self, exit_stmt):
        pass

    def visit_assign_stmt(self, assign_stmt):
        pass

    def visit_ident(self, ident):
        pass

    def visit_literal(self, literal):
        pass

    def visit_readint_expr(self, readint_expr):
        pass

    def visit_unary_expr(self, unary_expr):
        pass

    def visit_binop_expr(self, binop_expr):
        pass

    def visit_grouping_expr(self, grouping_expr):
        pass

    def visit_len_expr(self, len_expr):
        pass

    def visit_pos_expr(self, pos_expr):
        pass

    def visit_readstr_expr(self, readstr_expr):
        pass

    def visit_concat_expr(self, concat_expr):
        pass

    def visit_substr_expr(self, substr_expr):
        pass

    def visit_if_stmt(self, if_stmt):
        pass

    def visit_while_stmt(self, while_stmt):
        pass

    def visit_not_expr(self, not_expr):
        pass

    def visit_boolop_expr(self, boolop_expr):
        pass

    def visit_num_relop_expr(self, num_relop_expr):
        pass

    def visit_str_relop_expr(self, str_relop_expr):
        pass

    def visit_print_stmt(self, print_stmt):
        pass

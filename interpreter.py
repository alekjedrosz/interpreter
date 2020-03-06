import sys

from visitor import Visitor
from parser_prim import make_parser
from errors import error
from environment import Environment


class Interpreter(Visitor):
    def __init__(self, input_str):
        """
        Initializes the interpreter and starts interpretation.
        :param input_str: Program to interpret.
        """
        parser = make_parser()
        ast = parser.parse(input_str)
        self.environment = Environment()
        ast.accept(self)

    def evaluate(self, expr):
        """
        Evaluates an expression.
        :param expr: Expression to evaluate.
        :return: Value of the expression.
        """
        return expr.accept(self)

    def execute(self, stmt):
        """
        Executes a statement.
        :param stmt: Statement to execute.
        """
        stmt.accept(self)

    def visit_program(self, program):
        """
        Executes a ''program'' statement.
        """
        self.execute(program.instr)

    def visit_instr(self, instr):
        """
        Executes all ''simple_instr'' statements in a ''instr'' statement.
        """
        for simple_instr in instr.simple_instr_list:
            self.execute(simple_instr)

    def visit_instr_block(self, instr_block):
        """
        Executes all ''instr'' statements in a ''instr_block'' statement.
        """
        self.execute(instr_block.instr)

    def visit_exit_stmt(self, exit_stmt):
        """
        Executes an ''exit_stmt''.
        """
        exit()

    def visit_assign_stmt(self, assign_stmt):
        """
        Evaluates an expression in ''assign_stmt'' and
        assigns it to its identifier.
        """
        value = self.evaluate(assign_stmt.expr)
        self.environment.assign(assign_stmt.ident, value)

    def visit_ident(self, ident):
        """
        Finds a value associated with the ''ident'' identifier and
        returns it.
        :return: Value assigned to ''ident''.
        """
        return self.environment.get(ident.name)

    def visit_literal(self, literal):
        """
        :return: Value associated with ''literal''.
        """
        return literal.value

    def visit_readint_expr(self, readint_expr):
        """
        Evaluates a ''readint_expr'' by reading a NUM
        from standard input.
        :return: Value of the ''readint_expr'' expression.
        """
        i = input()
        try:
            i = int(i)
        except ValueError:
            error('', 'Input to readint must be of type NUM.')
        return i

    def visit_unary_expr(self, unary_expr):
        """
        Evaluates a ''num_expr'' and negates it.
        :return: Negated value of the ''num_expr''.
        """
        value = self.evaluate(unary_expr.num_expr)
        return -value

    def visit_binop_expr(self, binop_expr):
        """
        Evaluates ''binop_expr'' on both sides of the binary
        operator and applies the operator to the resulting
        values.
        :return: Value of the expression.
        """
        left = self.evaluate(binop_expr.num_expr0)
        right = self.evaluate(binop_expr.num_expr1)
        op = binop_expr.op
        try:
            assert isinstance(left, int)
            assert isinstance(right, int)
        except AssertionError:
            error('', f'Binary operator {op} can only be applied to arguments of type NUM.')

        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            return left / right
        else:
            return left % right

    def visit_grouping_expr(self, grouping_expr):
        """
        Evaluates a ''num_expr'' inside a ''grouping_expr''.
        :return: Value of the ''num_expr''.
        """
        return self.evaluate(grouping_expr.num_expr)

    def visit_len_expr(self, len_expr):
        """
        Evaluates a ''str_expr'' passed into ''len_expr'' and
        computes its length.
        :return: Length of the ''str_expr''.
        """
        value = self.evaluate(len_expr.str_expr)
        try:
            assert isinstance(value, str)
        except AssertionError:
            error('', 'Argument passed to length() must be of type STRING.')
        return len(value)

    def visit_pos_expr(self, pos_expr):
        """
        Evaluates both ''str_expr'' expressions passed into
        ''pos_expr'' and computes the first occurrence of the
        first ''str_expr'' in the second ''str_expr''.
        :return: First occurrence of the first ''str_expr'' in the second
        ''str_expr'', or 0 if not found.
        """
        str_expr0 = self.evaluate(pos_expr.str_expr0)
        str_expr1 = self.evaluate(pos_expr.str_expr1)
        try:
            assert isinstance(str_expr0, str)
            assert isinstance(str_expr1, str)
        except AssertionError:
            error('', 'Arguments passed to position() must be of type STRING.')

        pos = str_expr0.find(str_expr1)
        return 0 if pos == -1 else pos

    def visit_readstr_expr(self, readstr_expr):
        """
        Evaluates a ''readstr_expr'' by reading a STRING from
        the standard input.
        :return: STRING read from the standard input.
        """
        i = input()
        return i

    def visit_concat_expr(self, concat_expr):
        """
        Evaluates both ''str_expr'' expressions passed into
        ''concat_expr'' and concatenates them.
        :return: Concatenated ''str_expr'' expressions.
        """
        str_expr0 = self.evaluate(concat_expr.str_expr0)
        str_expr1 = self.evaluate(concat_expr.str_expr1)
        try:
            assert isinstance(str_expr0, str)
            assert isinstance(str_expr1, str)
        except AssertionError:
            error('', 'Arguments passed to concatenate() must be of type STRING.')

        return ''.join([str_expr0, str_expr1])

    def visit_substr_expr(self, substr_expr):
        """
        Evaluates all three expressions passed into ''substr_expr''
        and returns a substring of the ''str_expr'' starting at
        the first ''num_expr'' of length at most equal to the
        second ''num_expr''.
        :return: The resulting substring, or an empty string if
        the first ''num_expr'' exceeds the length of the ''str_expr''.
        """
        string = self.evaluate(substr_expr.str_expr)
        start = self.evaluate(substr_expr.num_expr0)
        end = self.evaluate(substr_expr.num_expr1)
        try:
            assert isinstance(string, str)
            assert isinstance(start, int)
            assert isinstance(end, int)
        except AssertionError:
            error('', 'Arguments passed to substring() must be of appropriate types.')

        if start < 1 or end < 0:
            return ''
        return string[start-1:end]

    def visit_if_stmt(self, if_stmt):
        """
        Evaluates the ''if_stmt'' condition and executes
        one of the branching statements based on that
        evaluation.
        """
        condition = self.evaluate(if_stmt.cond)
        true_branch = if_stmt.true_simple_instr
        else_branch = if_stmt.else_simple_instr
        try:
            assert isinstance(condition, bool)
        except AssertionError:
            error('', 'If clause condition must be a boolean expression.')
        if condition:
            self.execute(true_branch)
        else:
            if else_branch is not None:
                self.execute(else_branch)

    def visit_while_stmt(self, while_stmt):
        """
        Evaluates the ''while_stmt'' condition in a while
        loop, executing the ''simple_instr'' statement as
        long as the condition is met.
        """
        condition = while_stmt.cond
        simple_instr = while_stmt.simple_instr
        try:
            assert isinstance(self.evaluate(condition), bool)
        except AssertionError:
            error('', 'While loop condition must be a boolean expression.')

        if while_stmt.do_while:
            while True:
                self.execute(simple_instr)
                if not self.evaluate(condition):
                    break
        else:
            while self.evaluate(condition):
                self.execute(simple_instr)

    def visit_not_expr(self, not_expr):
        """
        Evaluates a ''bool_expr'' and negates it.
        :return: Negated ''bool_expr''.
        """
        value = self.evaluate(not_expr.bool_expr)
        try:
            assert isinstance(value, bool)
        except AssertionError:
            error('', '\'not\' keyword can only be used with a boolean expression.')
        return not value

    def visit_boolop_expr(self, boolop_expr):
        """
        Evaluates both ''bool_expr'' and applies the
        boolean operator to them.
        :return: Value of the expression.
        """
        bool_expr0 = self.evaluate(boolop_expr.bool_expr0)
        bool_expr1 = self.evaluate(boolop_expr.bool_expr1)
        bool_op = boolop_expr.bool_op
        try:
            assert isinstance(bool_expr0, bool)
            assert isinstance(bool_expr1, bool)
        except AssertionError:
            error('', 'Boolean operators can only be used with boolean expressions.')

        if bool_op == 'and':
            return bool_expr0 and bool_expr1
        elif bool_op == 'or':
            return bool_expr0 or bool_expr1

    def visit_num_relop_expr(self, num_relop_expr):
        """
        Evaluates both ''num_expr'' and applies a
        relational operator to the resulting values.
        :return: Value of the expression.
        """
        num_expr0 = self.evaluate(num_relop_expr.num_expr0)
        num_expr1 = self.evaluate(num_relop_expr.num_expr1)
        num_rel = num_relop_expr.num_rel
        try:
            assert isinstance(num_expr0, int)
            assert isinstance(num_expr1, int)
        except AssertionError:
            error('', f'Relational operator \'{num_rel}\' can only be used with type NUM')
        if num_rel == '=':
            return num_expr0 == num_expr1
        elif num_rel == '<':
            return num_expr0 < num_expr1
        elif num_rel == '<=':
            return num_expr0 <= num_expr1
        elif num_rel == '>':
            return num_expr0 > num_expr1
        elif num_rel == '>=':
            return num_expr0 >= num_expr1
        elif num_rel == '<>':
            return num_expr0 != num_expr1
        else:
            error('', f'Relational operator \'{num_rel}\' not supported for type NUM.')

    def visit_str_relop_expr(self, str_relop_expr):
        """
        Evaluates both ''str_expr'' and applies a
        relational operator to the resulting values.
        :return: Value of the expression.
        """
        str_expr0 = self.evaluate(str_relop_expr.str_expr0)
        str_expr1 = self.evaluate(str_relop_expr.str_expr1)
        str_rel = str_relop_expr.str_rel
        try:
            assert isinstance(str_expr0, str)
            assert isinstance(str_expr1, str)
        except AssertionError:
            error('', f'Relational operator \'{str_rel}\' can only be used with type STRING.')
        if str_rel == '==':
            return str_expr0 == str_expr1
        elif str_rel == '!=':
            return str_expr0 != str_expr1

    def visit_print_stmt(self, print_stmt):
        """
        Evaluates the expression passed into ''print_stmt''
        and prints it to standard output.
        """
        value = self.evaluate(print_stmt.expr)
        print(value)


if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        Interpreter(f.read())

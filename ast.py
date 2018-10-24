from error import ParserErrorType, ParserError

class Expression:
    def semantic_check():
        pass

class SemanticError(Expression):

    left = None

    def __init__(self, parser_error):
        self.parser_error = parser_error

    def semantic_check(self):

        print(self.parser_error)

        if self.left is None:
            print("end of semantic errors")
        else:
            self.left.semantic_check()

class BinaryExpression(Expression):
    op = ""
    left = None
    right = None

    def __init__(self, op):
        self.op = op

    def semantic_check(self):
        if self.left is None:
            print("error: binary expression left is none")
        else:
            self.left.semantic_check()

        if self.right is None:
            print("error: binary expression right is none")
        else:
            self.right.semantic_check()

class UnitaryExpression(Expression):
    op = ""
    left = None

    def __init__(self, op, left = None):
        self.op = op
        self.left = left

    def semantic_check(self):
        if self.left is None:
            print("error: binary expression left is none")
        else:
            self.left.semantic_check()

class Term(Expression):
    value = False

    def __init__(self, value):
        self.value = value

    def semantic_check(self):
        pass

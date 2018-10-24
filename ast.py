from error import ParserErrorType, ParserError

class Expression:
    def visit(self):
        pass

    def resolve(self):
        pass

class BinaryExpression(Expression):

    def __init__(self, op):
        self.op = op

    def visit(self):
        if self.left is not None:
            self.left.visit()

        print("BinaryExpression: %s" % self.op)

        if self.right is not None:
            self.right.visit()

    def resolve(self):
        if self.left is None:
            raise Exception("l-value of operator is none")

        if self.right is None:
            raise Exception("r-value of operator is none")

        if self.op == "and":
            return self.left.resolve() and self.right.resolve()
        elif self.op == "or":
            return self.left.resolve() or self.right.resolve()
        else:
            raise Exception("binary operator is invalid")

class UnitaryExpression(Expression):

    def __init__(self, op):
        self.op = op

    def visit(self):
        if self.left is not None:
            self.left.visit()

        print("UnitaryExpression: %s" % self.op)

    def resolve(self):
        if self.left is None:
            raise Exception("l-value of operator is none")

        if self.op == "not":
            return not self.left.resolve()
        else:
            raise Exception("unitary operator is invalid")

class Term(Expression):

    def __init__(self, value):
        self.value = value

    def visit(self):
        print("Term: %s" % self.value)

    def resolve(self):
        return self.value

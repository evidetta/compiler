import ast
from error import ParserErrorType, ParserError
from tokens import Tokens

class ParserState:
    index = 0
    tokens = None
    parsed_string = ''

    state_stack = []
    errors = set([])

    def __init__(self, tokens, index = 0, parsed_string = '', errors = set([])):
        self.tokens = tokens
        self.index = index
        self.parsed_string = parsed_string
        self.errors = errors

    def currentToken(self):
        return self.tokens[self.index]['type']

    def currentString(self):
        return self.tokens[self.index]['string']

    def step(self):
        self.parsed_string += self.tokens[self.index]['string']
        self.index += 1

        while True:
            if self.tokens[self.index]['type'] == Tokens.ERROR:
                self.errors.add(ParserError("syntax error", len(self.parsed_string), ParserErrorType.LEXICAL_ERROR, 0))
                self.index += 1
                self.parsed_string += self.currentString()
            else:
                break

    def checkpoint(self):
        self.state_stack.append(ParserState(self.tokens, self.index, self.parsed_string, self.errors))

    def backtrack(self):
        parser_state = self.state_stack.pop()
        self.index = parser_state.index
        self.parsed_string = parser_state.parsed_string
        self.errors = parser_state.errors

def parse(tokens):
    parser_state = ParserState(tokens)
    output = match_statement(parser_state)
    output.semantic_check()


#    errors_by_type = [[e for e in parser_state.errors if e.error_type == v] for k, v in enumerate(ParserErrorType)]
#    for errors in errors_by_type:
#        for error in sorted(errors, key=lambda x: x.char_number):
#            print(error)


    return output

def match_statement(parser_state):
    expression = match_expression(parser_state)
    if expression is ast.SemanticError:
        semantic_error = ast.SemanticError(ParserError("statement not matchedd", len(parser_state.parsed_string)))
        semantic_error.left = expression
        return semantic_error
    if parser_state.currentToken() != Tokens.EOF:
        return ast.SemanticError(ParserError("statement not matched", len(parser_state.parsed_string)))
    return expression

def match_expression(parser_state):
    parser_state.checkpoint()
    and_expression = match_and_expression(parser_state)
    if and_expression is not ast.SemanticError:
        return and_expression
    parser_state.backtrack()

    parser_state.checkpoint()
    or_expression = match_or_expression(parser_state)
    if or_expression is not ast.SemanticError:
        return or_expression
    parser_state.backtrack()

    term = match_term(parser_state)
    if term is not ast.SemanticError:
        return term
    return ast.SemanticError(ParserError("expression not matched", len(parser_state.parsed_string)))

def match_and_expression(parser_state):
    and_expression = ast.BinaryExpression("and")
    term = match_term(parser_state)
    if term is ast.SemanticError:
        semantic_error = ast.SemanticError(ParserError("and_expression not matched", len(parser_state.parsed_string)))
        semantic_error.left = term
        return semantic_error
    and_expression.left = term
    if parser_state.currentToken() != Tokens.AND:
        return ast.SemanticError(ParserError("and_expression not matched", len(parser_state.parsed_string)))
    parser_state.step()
    expression = match_expression(parser_state)
    if expression is ast.SemanticError:
        semantic_error = ast.SemanticError(ParserError("and_expression not matched", len(parser_state.parsed_string)))
        semantic_error.left = term
        return semantic_error
    and_expression.right = expression
    return and_expression

def match_or_expression(parser_state):
    or_expression = ast.BinaryExpression("or")
    term = match_term(parser_state)
    if term is ast.SemanticError:
        semantic_error = ast.SemanticError(ParserError("or_expression not matched", len(parser_state.parsed_string)))
        semantic_error.left = term
        return semantic_error
    or_expression.left = term
    if parser_state.currentToken() != Tokens.OR:
        return ast.SemanticError(ParserError("or_expression not matched", len(parser_state.parsed_string)))
    parser_state.step()
    expression = match_expression(parser_state)
    if expression is ast.SemanticError:
        semantic_error = ast.SemanticError(ParserError("or_expression not matched", len(parser_state.parsed_string)))
        semantic_error.left = expression
        return semantic_error
    or_expression.right = expression
    return or_expression

def match_term(parser_state):
    value = match_value_term(parser_state)
    if value is not ast.SemanticError:
        return value
    value = match_negated_term(parser_state)
    if value is not ast.SemanticError:
        return value
    return ast.SemanticError(ParserError("term not matched", len(parser_state.parsed_string)))

def match_negated_term(parser_state):
    match_whitespace(parser_state)
    if parser_state.currentToken() != Tokens.NOT:
        ast.SemanticError(ParserError("negated term not matched", len(parser_state.parsed_string)))
    parser_state.step()
    term = match_term(parser_state)
    if term is ast.SemanticError:
        semantic_error = ast.SemanticError(ParserError("negated term not matched", len(parser_state.parsed_string)))
        semantic_error.left = term
    return ast.UnitaryExpression("not", term)

def match_value_term(parser_state):
    value = match_true_value(parser_state)
    if value is not ast.SemanticError:
        return value
    value = match_false_value(parser_state)
    if value is not ast.SemanticError:
        return value
    return ast.SemanticError(ParserError("value term not matched", len(parser_state.parsed_string)))

def match_true_value(parser_state):
    if parser_state.currentToken() == Tokens.TRUE:
        parser_state.step()
        match_whitespace(parser_state)
        return ast.Term(True)
    elif match_whitespace(parser_state):
        if parser_state.currentToken() == Tokens.TRUE:
            parser_state.step()
            match_whitespace(parser_state)
            return ast.Term(True)
    return ast.SemanticError(ParserError("true not matched", len(parser_state.parsed_string)))

def match_false_value(parser_state):
    if parser_state.currentToken() == Tokens.FALSE:
        parser_state.step()
        match_whitespace(parser_state)
        return ast.Term(False)
    elif match_whitespace(parser_state):
        if parser_state.currentToken() == Tokens.FALSE:
            parser_state.step()
            match_whitespace(parser_state)
            return ast.Term(False)
    return ast.SemanticError(ParserError("false not matched", len(parser_state.parsed_string)))

def match_whitespace(parser_state):
    if parser_state.currentToken() != Tokens.WHITESPACE:
        return False
    parser_state.step()
    while parser_state.currentToken() == Tokens.WHITESPACE:
        parser_state.step()
    return True

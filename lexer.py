from tokens import Tokens

def lex(input_str):
    tokens = []
    current_str = ''
    lexers = [lex_whitespace, lex_true, lex_false, lex_not, lex_and, lex_or]

    for char in input_str:
        current_str += char
        on_course = False

        for lexer in lexers:
            out = lexer(current_str, tokens)
            if out == True:
                current_str = ''
                on_course = True
                break
            elif out == False:
                on_course = True
                break

        if on_course == False:
            tokens.append({"type": Tokens.ERROR, "string": current_str})
            current_str = ''

    if current_str != '':
        tokens.append({"type": Tokens.ERROR, "string": current_str})
        current_str = ''

    tokens.append({"type": Tokens.EOF, "string": ''})
    return tokens

def lex_whitespace(current_str, tokens):
    if current_str == ' ':
        tokens.append({"type": Tokens.WHITESPACE, "string": current_str})
        return True
    return None

def lex_true(current_str, tokens):
    if current_str == 't':
        return False

    if current_str == 'tr':
        return False

    if current_str == 'tru':
        return False

    if current_str == 'true':
        tokens.append({"type": Tokens.TRUE, "string": current_str})
        return True
    return None

def lex_false(current_str, tokens):
    if current_str == 'f':
        return False

    if current_str == 'fa':
        return False

    if current_str == 'fal':
        return False

    if current_str == 'fals':
       return False

    if current_str == 'false':
        tokens.append({"type": Tokens.FALSE, "string": current_str})
        return True
    return None

def lex_and(current_str, tokens):
    if current_str == 'a':
        return False

    if current_str == 'an':
        return False

    if current_str == 'and':
        tokens.append({"type": Tokens.AND, "string": current_str})
        return True
    return None

def lex_or(current_str, tokens):
    if current_str == 'o':
        return False

    if current_str == 'or':
        tokens.append({"type": Tokens.OR, "string": current_str})
        return True
    return None

def lex_not(current_str, tokens):
    if current_str == 'n':
        return False

    if current_str == 'no':
        return False

    if current_str == 'not':
        tokens.append({"type": Tokens.NOT, "string": current_str})
        return True
    return None

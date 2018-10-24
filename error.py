from enum import Enum, unique

@unique
class ParserErrorType(Enum):
    LEXICAL_ERROR = 0
    SEMANTIC_ERROR = 1
    EOF_ERROR = 2


class ParserError:
    def __init__(self, msg, char_number, token, error_type = None, priority = 0):
        self.msg = msg
        self.char_number = char_number
        self.token = token
        self.error_type = error_type
        self.priority = priority

    def __str__(self):
        return "error: %s at char %d: got %s" % (self.msg, self.char_number, self.token)

    def __eq__(self, other):
        return self.msg == other.msg and self.char_number == other.char_number and self.error_type == other.error_type and self.priority == other.priority

    def __ne__(self, other):
        return self.msg != other.msg or self.char_number != other.char_number or self.error_type != other.error_type or self.priority != other.priority

    def __hash__(self):
        return hash("%sERROR%dERROR%sERROR%d" % (self.msg, self.char_number, self.error_type, self.priority))

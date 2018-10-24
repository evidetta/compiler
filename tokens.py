from enum import Enum, unique

@unique
class Tokens(Enum):
    FALSE = 0
    TRUE = 1
    AND = 2
    OR = 3
    NOT = 4
    WHITESPACE = 99
    EOF = 100
    ERROR = 999

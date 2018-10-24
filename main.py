import lexer
import parser

tokens = lexer.lex('true and false ')
output = parser.parse(tokens)
#output.visit()

import lexer
import parser

tokens = lexer.lex('not not true and not true or true and not not   not false')
tree, errors = parser.parse(tokens)
tree.visit()

print(tree.resolve())

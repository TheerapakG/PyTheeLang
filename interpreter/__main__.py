from .lexer import Lexer
from .token import Token, TokenType

while True:
    try:
        text = input('> ')
    except EOFError:
        break
    if not text:
        continue
    lexer = Lexer(text)
    while True:
        token = lexer.get_next_token()
        print(token)
        if(token.lexeme == TokenType.EOF):
            break

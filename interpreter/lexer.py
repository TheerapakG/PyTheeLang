from .token import Token, TokenType, RESERVED_KEYWORDS

import re
import codecs

ESCAPE_SEQUENCE_RE = re.compile(r'''
    ( \\U........      # 8-digit hex escapes
    | \\u....          # 4-digit hex escapes
    | \\x..            # 2-digit hex escapes
    | \\[0-7]{1,3}     # Octal escapes
    | \\N\{[^}]+\}     # Unicode characters by name
    | \\[\\'"abfnrtv]  # Single-character escapes
    )''', re.UNICODE | re.VERBOSE)

def decode_escapes(s):
    def decode_match(match):
        return codecs.decode(match.group(0), 'unicode-escape')

    return ESCAPE_SEQUENCE_RE.sub(decode_match, s)

class Lexer:

    def __init__(self, text):
        # input
        self.text = text
        self.pos = 0
        # current token instance
        self.current_token = None
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Error parsing input')

    def advance(self):
        """Advance the 'pos' pointer and set the 'current_char' variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]
            
    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char == ' ':
            self.advance()

    def identifier(self):
        """Handle identifiers and reserved keywords"""
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()

        token = RESERVED_KEYWORDS.get(result, Token('identifier', result))
        self.skip_whitespace()
        return token

    def space(self):
        result = 0
        while self.current_char is not None and self.current_char.isspace():
            result += 1
            self.advance()
        return Token(TokenType.INDENT, result)        
    
    def digit(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        if self.current_char == '.':
            result += self.current_char
            self.advance()

            while (
                self.current_char is not None and
                self.current_char.isdigit()
            ):
                result += self.current_char
                self.advance()

            token = Token(TokenType.FLT_LITERAL, float(result))
        else:
            token = Token(TokenType.INT_LITERAL, int(result))
        self.skip_whitespace()
        return token

    def cont(self):
        self.advance()
        self.skip_whitespace()
        return Token(TokenType.CONTINUE_PARSE, 'CONTINUE_PARSE')
        
    def cstr(self):
        result = ''
        self.advance()
        while self.current_char != '\'':
            if self.current_char == '\n' or self.current_char == None:
                self.error()
            if self.current_char == '\\':
                result += self.current_char
                self.advance()
                if self.current_char == '\n' or self.current_char == None:
                    self.error()
            result += self.current_char
            self.advance()
        self.advance()
        self.skip_whitespace()
        return Token(TokenType.STR_LITERAL, decode_escapes(result))
        
    def sstr(self):
        result = ''
        self.advance()
        while self.current_char != '\"':
            if self.current_char == '\n' or self.current_char == None:
                self.error()
            if self.current_char == '\\':
                result += self.current_char
                self.advance()
                if self.current_char == '\n' or self.current_char == None:
                    self.error()
            result += self.current_char
            self.advance()
        self.advance()
        self.skip_whitespace()
        return Token(TokenType.STR_LITERAL, decode_escapes(result))

    def sep(self):
        self.advance()
        self.skip_whitespace()
        return Token(TokenType.SEPARATOR, 'SEPARATOR')

    def paren_o(self):
        self.advance()
        self.skip_whitespace()
        return Token(TokenType.PAREN_O, 'PAREN_O')
    
    def paren_e(self):
        self.advance()
        self.skip_whitespace()
        return Token(TokenType.PAREN_E, 'PAREN_E')

    def square_o(self):
        self.advance()
        self.skip_whitespace()
        return Token(TokenType.SQUARE_O, 'SQUARE_O')
    
    def square_e(self):
        self.advance()
        self.skip_whitespace()
        return Token(TokenType.SQUARE_E, 'SQUARE_E')

    def curl_o(self):
        self.advance()
        self.skip_whitespace()
        return Token(TokenType.CURL_O, 'CURL_O')
    
    def curl_e(self):
        self.advance()
        self.skip_whitespace()
        return Token(TokenType.CURL_E, 'CURL_E')

    def comment(self):
        result = ''
        self.advance()
        self.advance()
        while self.current_char is not None and self.current_char != '\n':
            result += self.current_char
            self.advance()
        return Token(TokenType.COMMENT, result)

    def multi_comment(self):
        result = ''
        self.advance()
        self.advance()
        while self.current_char is not None and not(self.current_char == '*' and self.peek() == '/'):
            result += self.current_char
            self.advance()
        if self.current_char is None:
            self.error()
        self.advance()
        self.advance()
        return Token(TokenType.MULTI_COMMENT, result)

    def divide_assign(self):
        self.advance()
        self.advance()
        self.skip_whitespace()
        return Token(TokenType.DIVIDE_ASSIGN, 'DIVIDE_ASSIGN')

    def divide(self):
        self.advance()
        self.skip_whitespace()
        return Token(TokenType.DIVIDE, 'DIVIDE')

    def multiply_assign(self):
        self.advance()
        self.advance()
        self.skip_whitespace()
        return Token(TokenType.MULTIPLY_ASSIGN, 'MULTIPLY_ASSIGN')

    def multiply(self):
        self.advance()
        self.skip_whitespace()
        return Token(TokenType.MULTIPLY, 'MULTIPLY')

    def mod(self):
        self.advance()
        self.skip_whitespace()
        return Token(TokenType.MOD, 'MOD')

    def xor(self):
        self.advance()
        self.advance()
        self.skip_whitespace()
        return Token(TokenType.XOR, 'XOR')

    def exp_assign(self):
        self.advance()
        self.advance()
        self.skip_whitespace()
        return Token(TokenType.EXP, 'EXP_ASSIGN')
    
    def exp(self):
        self.advance()
        self.skip_whitespace()
        return Token(TokenType.EXP, 'EXP')

    def ternary(self):
        self.advance()
        self.skip_whitespace()
        return Token(TokenType.TERNARY, 'TERNARY')

    def incr(self):
        self.advance()
        self.advance()
        self.skip_whitespace()
        return Token(TokenType.INCREMENT, 'INCREMENT')
    
    def plus_assign(self):
        self.advance()
        self.advance()
        self.skip_whitespace()
        return Token(TokenType.PLUS_ASSIGN, 'PLUS_ASSIGN')

    def plus(self):
        self.advance()
        self.skip_whitespace()
        return Token(TokenType.PLUS, 'PLUS')

    def decr(self):
        self.advance()
        self.advance()
        self.skip_whitespace()
        return Token(TokenType.DECREMENT, 'DECREMENT')
    
    def minus_assign(self):
        self.advance()
        self.advance()
        self.skip_whitespace()
        return Token(TokenType.MINUS_ASSIGN, 'MINUS_ASSIGN')

    def minus(self):
        self.advance()
        self.skip_whitespace()
        return Token(TokenType.MINUS, 'MINUS')

    def shift_l(self):
        self.advance()
        self.advance()
        self.skip_whitespace()
        return Token(TokenType.SHIFT_L, 'SHIFT_L')

    def lesser_equal(self):
        self.advance()
        self.advance()
        self.skip_whitespace()
        return Token(TokenType.LESSER_EQUAL, 'LESSER_EQUAL')

    def lesser(self):
        self.advance()
        self.skip_whitespace()
        return Token(TokenType.LESSER, 'LESSER')

    def shift_r(self):
        self.advance()
        self.advance()
        self.skip_whitespace()
        return Token(TokenType.SHIFT_R, 'SHIFT_R')

    def greater_equal(self):
        self.advance()
        self.advance()
        self.skip_whitespace()
        return Token(TokenType.GREATER_EQUAL, 'GREATER_EQUAL')

    def greater(self):
        self.advance()
        self.skip_whitespace()
        return Token(TokenType.GREATER, 'GREATER')

    def op_and(self):
        self.advance()
        self.advance()
        self.skip_whitespace()
        return Token(TokenType.OP_AND, 'OP_AND')

    def bit_and_assign(self):
        self.advance()
        self.advance()
        self.skip_whitespace()
        return Token(TokenType.BIT_AND_ASSIGN, 'BIT_AND_ASSIGN')
    
    def bit_and(self):
        self.advance()
        self.skip_whitespace()
        return Token(TokenType.BIT_AND, 'BIT_AND')

    def op_or(self):
        self.advance()
        self.advance()
        self.skip_whitespace()
        return Token(TokenType.OP_OR, 'OP_OR')

    def bit_or_assign(self):
        self.advance()
        self.advance()
        self.skip_whitespace()
        return Token(TokenType.BIT_OR_ASSIGN, 'BIT_OR_ASSIGN')
    
    def bit_or(self):
        self.advance()
        self.skip_whitespace()
        return Token(TokenType.BIT_OR, 'BIT_OR')

    def not_equal(self):
        self.advance()
        self.advance()
        self.skip_whitespace()
        return Token(TokenType.NOT_EQUAL, 'NOT_EQUAL')
    
    def bit_not(self):
        self.advance()
        self.skip_whitespace()
        return Token(TokenType.BIT_NOT, 'BIT_NOT')

    def equal(self):
        self.advance()
        self.advance()
        self.skip_whitespace()
        return Token(TokenType.EQUAL, 'EQUAL')

    def assign(self):
        self.advance()
        self.skip_whitespace()
        return Token(TokenType.ASSIGN, 'ASSIGN')

    def get_next_token(self):
        """
        Lexer
        """

        while self.current_char is not None:
            if self.current_char.isalpha():
                return self.identifier()
        
            if self.current_char == '\n':
                return Token(TokenType.END_STATEMENT, None)

            if self.current_char.isspace():
                return self.space()

            if self.current_char.isdigit():
                return self.digit()

            if self.current_char == '\\':
                return self.cont()
                
            if self.current_char == '\'':
                return self.cstr()
                
            if self.current_char == '\"':
                return self.sstr()

            if self.current_char == ',':
                return self.sep()
            
            if self.current_char == '(':
                return self.paren_o()

            if self.current_char == ')':
                return self.paren_e()

            if self.current_char == '[':
                return self.square_o()

            if self.current_char == ']':
                return self.square_e()

            if self.current_char == '{':
                return self.curl_o()

            if self.current_char == '}':
                return self.curl_e()

            if self.current_char == '/' and self.peek() == '/':
                return self.comment()

            if self.current_char == '/' and self.peek() == '*':
                return self.multi_comment()

            if self.current_char == '/' and self.peek() == '=':
                return self.divide_assign()

            if self.current_char == '/':
                return self.divide()

            if self.current_char == '%':
                return self.mod()

            if self.current_char == '^' and self.peek() == '^':
                return self.xor()

            if self.current_char == '^' and self.peek() == '=':
                return self.exp_assign()
            
            if self.current_char == '^':
                return self.exp()

            if self.current_char == '?':
                return self.ternary()

            if self.current_char == '+' and self.peek() == '+':
                return self.incr()

            if self.current_char == '+' and self.peek() == '=':
                return self.plus_assign()

            if self.current_char == '+':
                return self.plus()

            if self.current_char == '-' and self.peek() == '-':
                return self.decr()

            if self.current_char == '-' and self.peek() == '=':
                return self.minus_assign()

            if self.current_char == '-':
                return self.minus()

            if self.current_char == '<' and self.peek() == '<':
                return self.shift_l()
            
            if self.current_char == '<' and self.peek() == '=':
                return self.lesser_equal()

            if self.current_char == '<':
                return self.lesser()

            if self.current_char == '>' and self.peek() == '>':
                return self.shift_r()
            
            if self.current_char == '>' and self.peek() == '=':
                return self.greater_equal()

            if self.current_char == '>':
                return self.greater()

            if self.current_char == '&' and self.peek() == '&':
                return self.op_and()
            
            if self.current_char == '&' and self.peek() == '=':
                return self.bit_and_assign()

            if self.current_char == '&':
                return self.bit_and()

            if self.current_char == '|' and self.peek() == '|':
                return self.op_or()
            
            if self.current_char == '|' and self.peek() == '=':
                return self.bit_or_assign()

            if self.current_char == '|':
                return self.bit_or()

            if self.current_char == '!' and self.peek() == '=':
                return self.not_equal()

            if self.current_char == '!':
                return self.bit_not()

            if self.current_char == '=' and self.peek() == '=':
                return self.equal()

            if self.current_char == '=':
                return self.assign()

            self.error()

        return Token(TokenType.EOF, None)

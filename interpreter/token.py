class Token:    
    def __init__(self, lexeme, value):
        # token type:
        self.lexeme = lexeme
        # token value:
        self.value = value

    def __str__(self):
        """
        String representation of the class instance.
        """
        return 'Token({lexeme}, {value})'.format(
            lexeme=self.lexeme,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

class TokenType:
    INDENT = 'INDENT'
    INT_LITERAL = 'INT_LITERAL'
    FLT_LITERAL = 'FLT_LITERAL'
    CONTINUE_PARSE = 'CONTINUE_PARSE'
    STR_LITERAL = 'STR_LITERAL'
    END_STATEMENT = 'END_STATEMENT'
    EOF = 'EOF'
    SEPARATOR = 'SEPARATOR'
    PAREN_O = 'PAREN_O'
    PAREN_E = 'PAREN_E'
    SQUARE_O = 'SQUARE_O'
    SQUARE_E = 'SQUARE_E'
    CURL_O = 'CURL_O'
    CURL_E = 'CURL_E'
    COMMENT = 'COMMENT'
    MULTI_COMMENT = 'MULTI_COMMENT'
    DIVIDE_ASSIGN = 'DIVIDE_ASSIGN'
    DIVIDE = 'DIVIDE'
    MULTIPLY_ASSIGN = 'MULTIPLY_ASSIGN'
    MULTIPLY = 'MULTIPLY'
    MOD = 'MOD'
    XOR = 'XOR'
    EXP_ASSIGN = 'EXP_ASSIGN'
    EXP = 'EXP'
    TERNARY = 'TERNARY'
    INCREMENT = 'INCREMENT'
    PLUS_ASSIGN = 'PLUS_ASSIGN'
    PLUS = 'PLUS'
    DECREMENT = 'DECREMENT'
    MINUS_ASSIGN = 'MINUS_ASSIGN'
    MINUS = 'MINUS'
    SHIFT_L = 'SHIFT_L'
    LESSER_EQUAL = 'LESSER_EQUAL'
    LESSER = 'LESSER'
    SHIFT_R = 'SHIFT_R'
    GREATER_EQUAL = 'GREATER_EQUAL'
    GREATER = 'GREATER'
    OP_AND = 'OP_AND'
    BIT_AND_ASSIGN = 'BIT_AND_ASSIGN'
    BIT_AND = 'BIT_AND'
    OP_OR = 'OP_OR'
    BIT_OR_ASSIGN = 'BIT_OR_ASSIGN'
    BIT_OR = 'BIT_OR'
    NOT_EQUAL = 'NOT_EQUAL'
    BIT_NOT = 'BIT_NOT'
    EQUAL = 'EQUAL'
    ASSIGN = 'ASSIGN'

    
RESERVED_KEYWORDS = {
    'enforce': Token('enforce', 'enforce'),
    'class': Token('class', 'class'),
    'function': Token('function', 'function'),
    'trait': Token('trait', 'trait'),
    'implement': Token('implement', 'implement'),
    'take': Token('take', 'take'),
    'as': Token('as', 'as'),
    'args': Token('args', 'args'),
    'capture': Token('capture', 'capture'),
    'raise': Token('raise', 'raise'),
    'catch': Token('catch', 'catch'),
    'ref': Token('ref', 'ref'),
    'operator': Token('operator', 'operator'),
    'if': Token('if', 'if'),
    'elif': Token('elif', 'elif'),
    'then': Token('then', 'then'),
    'else': Token('else', 'else'),
    'for': Token('for', 'for'),
    'while': Token('while', 'while'),
    'do': Token('do', 'do'),
    'continue': Token('continue', 'continue'),
    'break': Token('break', 'break'),
    'pass': Token('pass', 'pass'),
    'in': Token('in', 'in'),
}
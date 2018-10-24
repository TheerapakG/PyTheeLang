from .token import Token, TokenType, RESERVED_KEYWORDS
from .lexer import Lexer

class AST:
    pass

class UnaryOp(AST):
    def __init__(self, token, expr):
        self.token = token
        self.op = token.value
        self.expr = expr  # evalable expr

class BinaryOp(AST):
    def __init__(self, token, left, right):
        self.token = token
        self.op = token.value
        self.left = left  # evalable expr
        self.right = right  # evalable expr

class TernaryOp(AST):
    def __init__(self, token, val, true, false):
        self.token = token
        self.op = token.value
        self.val = val  # evalable expr
        self.true = true  # evalable expr
        self.false = false  # evalable expr

class Assign(AST):
    def __init__(self, token, left, right):
        self.token = token
        self.left = left  # evalable expr
        self.right = right  # evalable expr

class NoOp(AST):
    def __init__(self, token):
        self.token = token

class Literal(AST):
    def __init__(self, token):
        self.token = token
        self.type = token.lexeme
        self.value = token.value

class Var(AST):
    def __init__(self, token):
        self.token = token
        self.name = token.value

class Enforce(AST):
    def __init__(self, token, var, typename):
        self.token = token
        self.name = token.value
        self.var = var
        self.typename = typename

class Typename(AST):
    def __init__(self, token):
        self.token = token
        self.name = token.value

class Block(AST):
    def __init__(self, statements):
        self.statements = statements  # a list of nodes

class ClassDecl(AST):
    def __init__(self, token, traits, block):
        self.token = token
        self.name = token.value
        self.traits = traits # a list of Trait nodes
        self.block = block

class Trait(AST):
    def __init__(self, token):
        self.token = token
        self.name = token.value

class TraitDecl(AST):
    def __init__(self, token, traits, funcdecls):
        self.token = token
        self.name = token.value
        self.traits = traits # a list of Trait nodes
        self.funcdecls = funcdecls # a list of FuncDecl nodes

class Param(AST):
    def __init__(self, arg, traits):
        self.arg = arg
        self.traits = traits  # a list of Trait nodes

class FuncDecl(AST):
    def __init__(self, token, rettype, params, captures, block):
        self.params = params  # a list of Param nodes
        self.capturess = captures  # a list of Param nodes
        self.block = block

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()
        self.next_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def block(self, indent_not_less_than = 0):
        """
        block: mostly in form of <[INDENT]<statement>...> but also some whitspaces shit and comment shit before each line
        so it's more like <[[INDENT][MULTI_COMMENT][COMMENT]<END_STATEMENT>...][INDENT]<statement>...>[EOF]
        """
        indent = 0
        statements = list()
        while ((self.current_token == TokenType.INDENT or self.current_token == TokenType.END_STATEMENT) and (self.next_token == TokenType.INDENT or self.next_token == TokenType.END_STATEMENT)) or self.current_token == TokenType.COMMENT or self.current_token == TokenType.MULTI_COMMENT:
            self.eat(self.current_token.lexeme)
        if self.current_token.lexeme == TokenType.INDENT:
            indent = self.current_token.value
        if indent < indent_not_less_than:
            self.error()  # expected indent
        while (True):
            if indent != 0:
                if self.current_token.lexeme == TokenType.EOF:
                    return Block(statements)  # just end program
                if self.current_token.lexeme != TokenType.INDENT:
                    self.error()  # expected indent
                if self.current_token.value < indent:
                    return Block(statements)
                if self.current_token.value > indent:
                    self.error()  # unexpected indent
                self.eat(TokenType.INDENT)
            if self.current_token.lexeme == TokenType.EOF:
                return Block(statements)  # just end program
            statements.append(self.statement(indent))
            while ((self.current_token == TokenType.INDENT or self.current_token == TokenType.END_STATEMENT) and (self.next_token == TokenType.INDENT or self.next_token == TokenType.END_STATEMENT)) or self.current_token == TokenType.COMMENT or self.current_token == TokenType.MULTI_COMMENT:
                self.eat(self.current_token.lexeme)

    # if this isn't comment then this line will also considered "whitspaces shit" in the parser

    def statement(self, curr_indent_level):
        """
        block have already removed "whitspaces shit and comment shit" out

        statement: <ifblock><[EOF]|[END_STATEMENT]>
                   <forblock><[EOF]|[END_STATEMENT]>
                   <whileblock><[EOF]|[END_STATEMENT]>
                   <dowhileblock><[EOF]|[END_STATEMENT]>
                   <declaration><[EOF]|[END_STATEMENT]>
                   <raise><[EOF]|[END_STATEMENT]>
                   <funccall><[EOF]|[END_STATEMENT]>
                   <assign_expr><[EOF]|[END_STATEMENT]>
        """
        if self.current_token.lexeme == 'if':
            statement = self.ifblock(curr_indent_level)
        elif self.current_token.lexeme == 'for':
            statement = self.forblock(curr_indent_level)
        elif self.current_token.lexeme == 'while':
            statement = self.whileblock(curr_indent_level)
        elif self.current_token.lexeme == 'do':
            statement = self.dowhileblock(curr_indent_level)
        elif self.current_token.lexeme == 'enforce':
            statement = self.declaration(curr_indent_level)
        elif self.current_token.lexeme == 'raise':
            statement = self.raiseexcept(curr_indent_level)
        elif self.current_token.lexeme == 'identifier' and self.next_token.lexeme == TokenType.PAREN_O:
            statement = self.funccall(curr_indent_level)
        else:
            statement = self.assign_expr(curr_indent_level)

        if self.current_token.lexeme == TokenType.EOF:
            self.eat(TokenType.EOF)
        elif self.current_token.lexeme == TokenType.END_STATEMENT:
            self.eat(TokenType.END_STATEMENT)
        else:
            self.error()
        return statement

    def expression(self):
        """
        expression: <Var>[<operation><expression>]
        """
        
    
    def ifblock(self, curr_indent_level):
        """
        ifblock: <if><non-assign expression bool><<END_STATEMENT><block>|<statement>>
        """
        return 0

    def forblock(self, curr_indent_level):
        """
        forblock: <for><expression><SEPARATOR><non-assign expression bool><SEPARATOR><expression><<END_STATEMENT><block>|<statement>>
                  <for><Var><in><expression><<END_STATEMENT><block>|<statement>>
        """
        return 0

    def whileblock(self, curr_indent_level):
        """
        whileblock: <while><non-assign expression bool><<END_STATEMENT><block>|<statement>>
        """
        return 0

    def dowhileblock(self, curr_indent_level):
        """
        expression: <do><<END_STATEMENT><block>|<statement>><while><non-assign expression bool>
        """
        return 0

    def declaration(self, curr_indent_level):
        """
        declaration: <enforce><identifier><as><non-assign non-instace expr>

        make later lookup for identifier an instance
        """
        return 0

    def raiseexcept(self, curr_indent_level):
        """
        raiseexcept: <raise><non-assign instance expr>
        """
        return 0

    def funccall(self, curr_indent_level):
        """
        funccall: <identifier><PAREN_O>[<non-assign instance expr>...]<PAREN_E>[<in><non-assign expr>]
        """
        return 0


    def parse(self):
        node = self.block()
        if self.current_token.type != TokenType.EOF:
            self.error()

        return node

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.lexeme == token_type:
            self.current_token = self.next_token
            self.next_token = self.lexer.get_next_token()
            if self.current_token.lexeme == TokenType.CONTINUE_PARSE:
                self.eat(TokenType.CONTINUE_PARSE)
                if self.current_token.lexeme == TokenType.END_STATEMENT:
                    self.eat(TokenType.END_STATEMENT)
                if self.current_token.lexeme == TokenType.INDENT:
                    self.eat(TokenType.INDENT)
        else:
            self.error()
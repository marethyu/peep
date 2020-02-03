import enum

class TokenTag(enum.Enum):
    # Builtin types
    INT = 0
    FLOAT = 1
    BOOL = 2
    STRING = 3
    
    # Instruction words
    IF = 4
    ELSE = 5
    WHILE = 6
    FOR = 7
    DO = 8
    BREAK = 9
    CONTINUE = 10
    
    # Builtin functions
    PRINT = 11
    SCAN = 12
    
    # Single character tokens
    LPAREN = 13
    RPAREN = 14
    LBRACK = 15
    RBRACK = 16
    SEMICOLON = 17
    ASSIGN = 18
    
    OR = 19
    AND = 20
    EQ_OP = 21
    REL_OP = 22
    ADD_OP = 23
    MUL_OP = 24
    UNARY_OP = 25
    
    # Other tokens
    IDENT = 26
    INT_CONST = 27
    RL_CONST = 28
    PLUS_EQ = 29
    MINUS_EQ = 30
    TRUE = 31
    FALSE = 32
    STR_LITERAL = 33
    EOF = 34

class Token(object):
    def __init__(self, tag, lexeme, lineno):
        self.tag = tag
        self.lexeme = lexeme
        self.lineno = lineno
    
    def __str__(self):
        return "Token(tag={}, lexeme=\"{}\", lineno={})".format(self.tag, self.lexeme, self.lineno)
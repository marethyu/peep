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
    REL_OP = 19 # ==, !=, <, >, <=, >=
    ADD_OP = 20 # +, -, ||
    OP = 21 # *, /, %, &&
    UNARY_OP = 22 # +, -, !
    
    # Other tokens
    IDENT = 23
    INT_CONST = 24
    RL_CONST = 25
    PLUS_EQ = 26 # +=
    MINUS_EQ = 27 # -=
    TRUE = 28
    FALSE = 29
    STR_LITERAL = 30
    EOF = 31

class Token(object):
    def __init__(self, tag, lexeme, lineno):
        self.tag = tag
        self.lexeme
        self.lineno = lineno
    
    def __str__(self):
        return "Token(tag={}, lexeme=\"{}\", lineno={})".format(self.tag, self.lexeme, self.lineno)
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
    
    # Single character tokens
    LPAREN = 12
    RPAREN = 13
    LBRACK = 14
    RBRACK = 15
    SEMICOLON = 16
    ASSIGN = 17
    REL_OP = 18 # ==, !=, <, >, <=, >=
    ADD_OP = 19 # +, -, ||
    OP = 20 # *, /, %, &&
    UNARY_OP = 21 # +, -, !
    
    # Other tokens
    IDENT = 22
    INT_CONST = 23
    RL_CONST = 24
    PLUS_EQ = 25 # +=
    MINUS_EQ = 26 # -=
    TRUE = 27
    FALSE = 28
    STR_LITERAL = 29
    UNK = 30
    EOF = 31

class Token(object):
    def __init__(self, tag, lexeme, lineno):
        self.tag = tag
        self.lexeme
        self.lineno = lineno
    
    def __str__(self):
        return "Token(tag={}, lexeme=\"{}\", lineno={})".format(self.tag, self.lexeme, self.lineno)
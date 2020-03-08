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
    BREAK = 8
    CONTINUE = 9
    
    # Builtin functions
    PRINT = 10
    SCAN = 11
    
    # Single character tokens
    LPAREN = 12
    RPAREN = 13
    LBRACK = 14
    RBRACK = 15
    SEMICOLON = 16
    ASSIGN = 17
    
    OR = 18
    AND = 19
    EQ_OP = 20
    REL_OP = 21
    ADD_OP = 22
    MUL_OP = 23
    UNARY_OP = 24
    
    # Other tokens
    IDENT = 25
    INT_CONST = 26
    RL_CONST = 27
    PLUS_EQ = 28
    MINUS_EQ = 29
    MUL_EQ = 30
    DIV_EQ = 31
    MOD_EQ = 32
    TRUE = 33
    FALSE = 34
    STR_LITERAL = 35
    EOF = 36

class Token:
    def __init__(self, tag, lexeme, lineno):
        self.tag = tag
        self.lexeme = lexeme
        self.lineno = lineno
    
    def __str__(self):
        return "Token(tag={}, lexeme=\"{}\", lineno={})".format(self.tag, self.lexeme, self.lineno)

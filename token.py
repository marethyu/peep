import enum

class TokenType(enum.Enum):
    # Build-in types
    INT = 0
    FLOAT = 1
    BOOL = 2
    STRING = 3
    VOID = 4
    
    # Instruction words
    IF = 5
    ELSE = 6
    WHILE = 7
    FOR = 8
    DO = 9
    BREAK = 10
    CONTINUE = 11
    RETURN = 12
    USE = 13 # It's like C's #include
    OBJECT = 14 # Same idea as C's struct
    
    # Build-in functions
    SCAN = 15
    PRINT = 16
    ASSERT = 17
    EXEC = 18 # This function executes an external command from shell
    
    # Single character tokens
    LPAREN = 19
    RPAREN = 20
    LSQ_BRCKT = 21
    RSQ_BRCKT = 22
    LCURLY_BRACE = 23
    RCURLY_BRACE = 24
    SEMICOLON = 25
    COMMA = 26
    DOT = 27
    ASSIGN = 28
    BIN_OP = 29
    UNARY_OP = 30
    
    # Logical
    EQUAL = 31
    NOT_EQU = 32
    AND = 33
    OR = 34
    NOT = 35
    LESS = 36
    GREATER = 37
    LESS_EQ = 38
    GREATER_EQ = 39
    
    # Other tokens
    IDENT = 40
    INT_CONST = 41
    FLT_CONST = 42
    PLUS_EQ = 43 # +=
    MINUS_EQ = 44 # -=
    TRUE = 45
    FALSE = 46
    STRING_CONST = 47
    UNK = 48
    EOF = 49

class Token(object):
    def __init__(self, type, value, lineno):
        self.type = type
        self.value = value
        self.lineno = lineno
    
    def __str__(self):
        return "Token(type={}, value=\"{}\", lineno={})".format(self.type, self.value, self.lineno)
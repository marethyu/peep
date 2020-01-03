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
    ASSIGN = 27
    BIN_OP = 28
    UNARY_OP = 29
    
    # Logical
    EQUAL = 30
    NOT_EQU = 31
    AND = 32
    OR = 33
    NOT = 34
    LESS = 35
    GREATER = 36
    LESS_EQ = 37
    GREATER_EQ = 38
    
    # Other tokens
    IDENT = 39
    INT_CONST = 40
    FLT_CONST = 41
    PLUS_EQ = 42 # +=
    MINUS_EQ = 43 # -=
    TRUE = 44
    FALSE = 45
    STRING_CONST = 46
    UNK = 47
    EOF = 48

class Token(object):
    def __init__(self, type, value, lineno):
        self.type = type
        self.value = value
        self.lineno = lineno
    
    def __str__(self):
        return "Token(type={}, value={}, lineno={})".format(self.type, self.value, self.lineno)
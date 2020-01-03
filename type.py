import enum

class Type(enum.Enum):
    """Type is used to describe identifier's type"""
    
    # Built-in types
    INT = 0
    FLOAT = 1
    BOOL = 2
    STRING = 3
    VOID = 4
    
    # Other types
    ARRAY = 5
    FUNCTION = 6
    OBJECT_DEC = 7 # Object declaration
    OBJECT = 8
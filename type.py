import enum

class Type(enum.Enum):
    """Type is used to describe identifier's type"""
    
    # Built-in types
    INT = 0
    FLOAT = 1
    BOOL = 2
    STRING = 3
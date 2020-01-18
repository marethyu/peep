import enum

class Type(enum.Enum):
    """Type is used to describe identifier's type, it contains some miscellaneous functions"""
    
    # Built-in types
    INT = 0
    FLOAT = 1
    BOOL = 2
    STRING = 3
    
    @staticmethod
    def check_match(type1, type2):
        return type1 == type2
    
    @staticmethod
    def is_type_ok(op_type, op, is_unary=False):
        """Precondition (for binary expressions): Type.check_match is called beforehand"""
        
        if op == '==':
            return op_type in [Type.INT, Type.FLOAT, Type.BOOL, Type.STRING]
        elif op == '!=':
            return op_type in [Type.INT, Type.FLOAT, Type.BOOL, Type.STRING]
        elif op == '<':
            return op_type in [Type.INT, Type.FLOAT, Type.STRING]
        elif op == '>':
            return op_type in [Type.INT, Type.FLOAT, Type.STRING]
        elif op == '<=':
            return op_type in [Type.INT, Type.FLOAT, Type.STRING]
        elif op == '>=':
            return op_type in [Type.INT, Type.FLOAT, Type.STRING]
        elif op == '+':
            if is_unary:
                return op_type in [Type.INT, Type.FLOAT]
            return op_type in [Type.INT, Type.FLOAT, Type.STRING]
        elif op == '-':
            if is_unary:
                return op_type in [Type.INT, Type.FLOAT]
            return op_type in [Type.INT, Type.FLOAT]
        elif op == '||':
            return op_type in [Type.BOOL]
        elif op == '*':
            return op_type in [Type.INT, Type.FLOAT]
        elif op == '/':
            return op_type in [Type.INT, Type.FLOAT]
        elif op == '%':
            return op_type in [Type.INT, Type.FLOAT]
        elif op == '&&':
            return op_type in [Type.BOOL]
        elif op == '!' and is_unary:
            return op_type in [Type.BOOL]
        
        return False
    
    @staticmethod
    def combine(op_type, op):
        """Precondition: Type.is_type_ok is called beforehand"""
        
        if op == '==':
            return Type.BOOL
        elif op == '!=':
            return Type.BOOL
        elif op == '<':
            return Type.BOOL
        elif op == '>':
            return Type.BOOL
        elif op == '<=':
            return Type.BOOL
        elif op == '>=':
            return Type.BOOL
        elif op == '+':
            return op_type
        elif op == '-':
            return op_type
        elif op == '||':
            return Type.BOOL
        elif op == '*':
            return op_type
        elif op == '/':
            return op_type
        elif op == '%':
            return op_type
        elif op == '&&':
            return Type.BOOL
        elif op == '!':
            return Type.BOOL
        
        return None
    
    @staticmethod
    def is_bool(type):
        return type == Type.BOOL
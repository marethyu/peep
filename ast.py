import enum

from abc import ABC, abstractmethod
from err import TypeError
from type import Type

class Kind(enum.Enum):
    # Expressions
    IDENT = 0
    CONST = 1
    REL_OP = 2
    ADD_OP = 3
    OP = 4
    U_OP = 5
    
    # Statements
    DECLARE = 6
    ASSIGN = 7
    INC = 8
    DEC = 9
    IF = 10
    WHILE = 11
    FOR = 12
    DO_WHILE = 13
    BREAK = 14
    CONT = 15
    EXPR = 16 # this is actually a statement
    PRINT = 17
    BLOCK = 18 # a collection of statements
    PRGM = 19 # an entire program

class ASTNode(ABC):
    def __init__(self, kind, value):
        self.kind = kind
        self.value = value
        
        import lexer
        self.lineno = lexer.lineno
    
    @abstractmethod
    def accept(self, tree_walker):
        pass

class Identifier(ASTNode):
    def __init__(self, type, name):
        super().__init__(Kind.IDENT, name)
        self.type = type
    
    def accept(self, tree_walker):
        tree_walker.visit_ident(self)

class Constant(ASTNode):
    def __init__(self, type, value):
        super().__init__(Kind.CONST, value)
        self.type = type
    
    def accept(self, tree_walker):
        tree_walker.visit_const(self)

# abstract
class BinaryOp(ASTNode):
    def __init__(self, kind, left, right, op):
        super().__init__(kind, None)
        self.left = left
        self.right = right
        self.op = op
        
        if not Type.check_match(left.type, right.type):
            raise TypeError(self.lineno, "Types does not match!")
        if not Type.is_type_ok(left.type, op):
            raise TypeError("Incompatible types for an operator")
        self.type = Type.combine(left.type, op)
    
    def accept(self, tree_walker):
        pass

class RelationalOp(BinaryOp):
    def __init__(self, left, right, op):
        super().__init__(Kind.REL_OP, left, right, op)
    
    def accept(self, tree_walker):
        tree_walker.visit_relop(self)

class AddictiveOp(BinaryOp):
    def __init__(self, left, right, op):
        super().__init__(Kind.ADD_OP, left, right, op)
    
    def accept(self, tree_walker):
        tree_walker.visit_addop(self)

class Operator(BinaryOp):
    def __init__(self, left, right, op):
        super().__init__(Kind.OP, left, right, op)
    
    def accept(self, tree_walker):
        tree_walker.visit_op(self)

class UnaryOp(ASTNode):
    def __init__(self, op, operand):
        super().__init__(Kind.U_OP, None)
        self.op = op
        self.operand = operand
        
        if not Type.is_type_ok(operand.type, op, is_unary=True):
            raise TypeError("Incompatible types for an operator")
        self.type = Type.combine(operand.type, op)
    
    def accept(self, tree_walker):
        tree_walker.visit_uop(self)

class Declaration(ASTNode):
    def __init__(self, ident):
        super().__init__(Kind.DECLARE, None)
        self.ident = ident
        self.type = self.ident.type
    
    def accept(self, tree_walker):
        tree_walker.visit_decl(self)

class Assign(ASTNode):
    def __init__(self, ident, expr):
        super().__init__(Kind.ASSIGN, None)
        self.ident = ident
        self.expr = expr
        
        if not Type.check_match(ident.type, expr.type):
            raise TypeError(self.lineno, "Types does not match!")
    
    def accept(self, tree_walker):
        tree_walker.visit_assign(self)

class Increment(ASTNode):
    def __init__(self, ident, expr):
        super().__init__(Kind.INC, None)
        self.ident = ident
        self.expr = expr
        
        if not Type.check_match(ident.type, expr.type):
            raise TypeError(self.lineno, "Types does not match!")
    
    def accept(self, tree_walker):
        tree_walker.visit_inc(self)

class Decrement(ASTNode):
    def __init__(self, ident, expr):
        super().__init__(Kind.DEC, None)
        self.ident = ident
        self.expr = expr
        
        if not Type.check_match(ident.type, expr.type):
            raise TypeError(self.lineno, "Types does not match!")
    
    def accept(self, tree_walker):
        tree_walker.visit_dec(self)

class If(ASTNode):
    def __init__(self, test, block, elif_br=None, else_br=None):
        super().__init__(Kind.IF, None)
        self.test = test
        self.block = block
        self.elif_br = elif_br
        self.else_br = else_br
        
        if not Type.is_bool(test.type):
            raise TypeError(self.lineno, "Expression inside (...) must return bool!")
    
    def accept(self, tree_walker):
        tree_walker.visit_if(self)

class While(ASTNode):
    def __init__(self, test, block):
        super().__init__(Kind.WHILE, None)
        self.test = test
        self.block = block
        
        if not Type.is_bool(test.type):
            raise TypeError(self.lineno, "Expression inside (...) must return bool!")
    
    def accept(self, tree_walker):
        tree_walker.visit_while(self)

class For(ASTNode):
    def __init__(self, init, test, stmt, block):
        super().__init__(Kind.FOR, None)
        self.init = init
        self.test = test
        self.stmt = stmt
        self.block = block
        
        if not Type.is_bool(test.type):
            raise TypeError(self.lineno, "Expression inside (...) must return bool!")
    
    def accept(self, tree_walker):
        tree_walker.visit_for(self)

class DoWhile(ASTNode):
    def __init__(self, block, test):
        super().__init__(Kind.DO_WHILE, None)
        self.block = block
        self.test = test
        
        if not Type.is_bool(test.type):
            raise TypeError(self.lineno, "Expression inside (...) must return bool!")
    
    def accept(self, tree_walker):
        tree_walker.visit_dowhile(self)

class Break(ASTNode):
    def __init__(self):
        super().__init__(Kind.BREAK, None)
    
    def accept(self, tree_walker):
        tree_walker.visit_break(self)

class Continue(ASTNode):
    def __init__(self):
        super().__init__(Kind.CONT, None)
    
    def accept(self, tree_walker):
        tree_walker.visit_cont(self)

class Expression(ASTNode):
    def __init__(self, expr):
        super().__init__(Kind.EXPR, None)
        self.expr = expr
    
    def accept(self, tree_walker):
        tree_walker.visit_expr(self)

class Print(ASTNode):
    def __init__(self, arg):
        super().__init__(Kind.PRINT, None)
        self.arg = arg
    
    def accept(self, tree_walker):
        tree_walker.visit_print(self)

class Block(ASTNode):
    def __init__(self, prev_blk, stmt):
        super().__init__(Kind.BLOCK, None)
        self.prev_blk = prev_blk
        self.stmt = stmt
    
    def accept(self, tree_walker):
        tree_walker.visit_blk(self)

class Program(ASTNode):
    def __init__(self, block):
        super().__init__(Kind.PRGM, None)
        self.block = block
    
    def accept(self, tree_walker):
        tree_walker.visit_prgm(self)
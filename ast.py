import enum

from abc import ABC, abstractmethod

class Kind(enum.Enum):
    # Expressions
    IDENT = 0
    CONST = 1
    ASSIGN = 2
    REL_OP = 3
    ADD_OP = 4
    OP = 5
    U_MINUS = 6
    NOT = 7
    
    # Statements
    IF = 8
    FOR = 9
    WHILE = 10
    DO_WHILE = 11
    EXPR = 12 # this is actually a statement
    BLOCK = 13 # a collection of statements
    PRGM = 14 # an entire program

class ASTNode(ABC):
    def __init__(self, kind, value):
        self.kind = kind
        self.value = value
    
    @abstractmethod
    def accept(self, tree_walker):
        pass

class Ident(ASTNode):
    def __init__(self, type, name):
        super.__init__(Kind.IDENT, name)
        self.type = type
    
    def accept(self, tree_walker):
        tree_walker.visit_ident(self)

class Const(ASTNode):
    def __init__(self, type, value):
        super.__init__(Kind.CONST, value)
        self.type = type
    
    def accept(self, tree_walker):
        tree_walker.visit_const(self)

class Assign(ASTNode):
    def __init__(self, ident, const):
        super.__init__(Kind.ASSIGN, None)
        self.ident = ident
        self.const = const
    
    def accept(self, tree_walker):
        tree_walker.visit_assign(self)

# abstract
class BinaryOp(ASTNode):
    def __init__(self, kind, left, right, op):
        super.__init__(kind, None)
        self.left = left
        self.right = right
        self.op = op
    
    def accept(self, tree_walker):
        pass

class RelationalOp(BinaryOp):
    def __init__(self, left, right, op):
        super.__init__(Kind.REL_OP, left, right, op)
    
    def accept(self, tree_walker):
        tree_walker.visit_relop(self)

class AddictiveOp(BinaryOp):
    def __init__(self, left, right, op):
        super.__init__(Kind.ADD_OP, left, right, op)
    
    def accept(self, tree_walker):
        tree_walker.visit_addop(self)

class Operator(BinaryOp):
    def __init__(self, left, right, op):
        super.__init__(Kind.OP, left, right, op)
    
    def accept(self, tree_walker):
        tree_walker.visit_op(self)

# abstract
class UnaryOp(ASTNode):
    def __init__(self, kind, operand):
        super.__init__(kind, None)
        self.operand = operand
    
    def accept(self, tree_walker):
        pass

class UnaryMinus(UnaryOp):
    def __init__(self, operand):
        super.__init__(Kind.U_MINUS, operand)
    
    def accept(self, tree_walker):
        tree_walker.visit_uminus(self)

class Not(UnaryOp):
    def __init__(self, operand):
        super.__init__(Kind.NOT, operand)
    
    def accept(self, tree_walker):
        tree_walker.visit_not(self)

class If(ASTNode):
    def __init__(self, test, block, elif_blk=None, else_blk=None):
        super.__init__(Kind.IF, None)
        self.block = block
        self.elif_blk = elif_blk
        self.else_blk = else_blk
    
    def accept(self, tree_walker):
        tree_walker.visit_if(self)

class For(ASTNode):
    def __init__(self, init, test, stmt):
        super.__init__(Kind.FOR, None)
        self.init = init
        self.test = test
        self.stmt = stmt
    
    def accept(self, tree_walker):
        tree_walker.visit_for(self)

class While(ASTNode):
    def __init__(self, test, block):
        super.__init__(Kind.WHILE, None)
        self.test = test
        self.block = block
    
    def accept(self, tree_walker):
        tree_walker.visit_while(self)

class DoWhile(ASTNode):
    def __init__(self, block, test):
        super.__init__(Kind.DO_WHILE, None)
        self.block = block
        self.test = test
    
    def accept(self, tree_walker):
        tree_walker.visit_dowhile(self)

class Expression(ASTNode):
    def __init__(self, expr):
        super.__init__(Kind.EXPR, None)
        self.expr = expr
    
    def accept(self, tree_walker):
        tree_walker.visit_expr(self)

class Block(ASTNode):
    def __init__(self, prev_blk, stmt):
        super.__init__(Kind.BLOCK, None)
        self.prev_blk = prev_blk
        self.stmt = stmt
    
    def accept(self, tree_walker):
        tree_walker.visit_blk(self)

class Program(ASTNode):
    def __init__(self, block):
        super.__init__(Kind.PRGM, None)
        self.block = block
    
    def accept(self, tree_walker):
        tree_walker.visit_prgm(self)
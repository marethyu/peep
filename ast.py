import enum
import lexer

from abc import ABC, abstractmethod

class Kind(enum.Enum):
    # Expressions
    IDENT = 0
    CONST = 1
    DECLARE = 2
    ASSIGN = 3
    REL_OP = 4
    ADD_OP = 5
    OP = 6
    U_MINUS = 7
    NOT = 8
    
    # Statements
    IF = 9
    WHILE = 10
    FOR = 11
    DO_WHILE = 12
    BREAK = 13
    CONT = 14
    EXPR = 15 # this is actually a statement
    BLOCK = 16 # a collection of statements
    PRGM = 17 # an entire program

class ASTNode(ABC):
    def __init__(self, kind, value):
        self.kind = kind
        self.value = value
        self.lineno = lexer.lineno
    
    @abstractmethod
    def accept(self, tree_walker):
        pass

class Identifier(ASTNode):
    def __init__(self, type, name):
        super.__init__(Kind.IDENT, name)
        self.type = type
    
    def accept(self, tree_walker):
        tree_walker.visit_ident(self)

class Constant(ASTNode):
    def __init__(self, type, value):
        super.__init__(Kind.CONST, value)
        self.type = type
    
    def accept(self, tree_walker):
        tree_walker.visit_const(self)

class Declaration(ASTNode):
    def __init__(self, ident):
        super.__init__(Kind.DECLARE, None)
        self.ident = ident
    
    def accept(self, tree_walker):
        tree_walker.visit_decl(self)

class Assign(ASTNode):
    def __init__(self, ident, expr):
        super.__init__(Kind.ASSIGN, None)
        self.ident = ident
        self.expr = expr
    
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
    def __init__(self, test, block, elif_br=None, else_br=None):
        super.__init__(Kind.IF, None)
        self.block = block
        self.elif_br = elif_br
        self.else_br = else_br
    
    def accept(self, tree_walker):
        tree_walker.visit_if(self)

class While(ASTNode):
    def __init__(self, test, block):
        super.__init__(Kind.WHILE, None)
        self.test = test
        self.block = block
    
    def accept(self, tree_walker):
        tree_walker.visit_while(self)

class For(ASTNode):
    def __init__(self, init, test, stmt, block):
        super.__init__(Kind.FOR, None)
        self.init = init
        self.test = test
        self.stmt = stmt
        self.block = block
    
    def accept(self, tree_walker):
        tree_walker.visit_for(self)

class DoWhile(ASTNode):
    def __init__(self, block, test):
        super.__init__(Kind.DO_WHILE, None)
        self.block = block
        self.test = test
    
    def accept(self, tree_walker):
        tree_walker.visit_dowhile(self)

class Break(ASTNode):
    def __init__(self):
        super.__init__(Kind.BREAK, None)
    
    def accept(self, tree_walker):
        tree_walker.visit_break(self)

class Continue(ASTNode):
    def __init__(self):
        super.__init__(Kind.CONT, None)
    
    def accept(self, tree_walker):
        tree_walker.visit_cont(self)

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
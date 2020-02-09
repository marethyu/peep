import enum

from abc import ABC, abstractmethod
from err import TypeError, raise_error
from type import Type

class Kind(enum.Enum):
    # Expressions
    IDENT = 0
    CONST = 1
    OR_OP = 2
    AND_OP = 3
    EQ_OP = 4
    REL_OP = 5
    ADD_OP = 6
    MUL_OP = 7
    U_OP = 8
    
    # Statements
    DECLARE = 9
    ASSIGN = 10
    INC = 11
    DEC = 12
    IF = 13
    WHILE = 14
    FOR = 15
    DO_WHILE = 16
    BREAK = 17
    CONT = 18
    EXPR = 19 # this is actually a statement
    PRINT = 20
    SCAN = 21
    BLOCK = 22 # a collection of statements
    PRGM = 23 # an entire program

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
        return tree_walker.visit_ident(self)

class Constant(ASTNode):
    def __init__(self, type, value):
        super().__init__(Kind.CONST, value)
        self.type = type
    
    def accept(self, tree_walker):
        return tree_walker.visit_const(self)

# abstract
class BinaryOp(ASTNode):
    def __init__(self, kind, left, right, op):
        super().__init__(kind, None)
        self.left = left
        self.right = right
        self.op = op
        
        if not Type.check_match(left.type, right.type):
            raise_error(TypeError(self.lineno, "Types does not match! (left operand type:{}, right operand type:{})".format(left.type, right.type)))
        if not Type.is_type_ok(left.type, op):
            raise_error(TypeError(self.lineno, "Incompatible types for an operator (operand type:{}, operator:{})".format(left.type, op)))
        self.type = Type.combine(left.type, op)
    
    def accept(self, tree_walker):
        pass

class OrOperator(BinaryOp):
    def __init__(self, left, right):
        super().__init__(Kind.OR_OP, left, right, '||')
    
    def accept(self, tree_walker):
        return tree_walker.visit_orop(self)

class AndOperator(BinaryOp):
    def __init__(self, left, right):
        super().__init__(Kind.AND_OP, left, right, '&&')
    
    def accept(self, tree_walker):
        return tree_walker.visit_andop(self)

class EqualityOp(BinaryOp):
    def __init__(self, left, right, op):
        super().__init__(Kind.EQ_OP, left, right, op)
    
    def accept(self, tree_walker):
        return tree_walker.visit_eqop(self)

class RelationalOp(BinaryOp):
    def __init__(self, left, right, op):
        super().__init__(Kind.REL_OP, left, right, op)
    
    def accept(self, tree_walker):
        return tree_walker.visit_relop(self)

class AddictiveOp(BinaryOp):
    def __init__(self, left, right, op):
        super().__init__(Kind.ADD_OP, left, right, op)
    
    def accept(self, tree_walker):
        return tree_walker.visit_addop(self)

class MultiplicativeOp(BinaryOp):
    def __init__(self, left, right, op):
        super().__init__(Kind.MUL_OP, left, right, op)
    
    def accept(self, tree_walker):
        return tree_walker.visit_mulop(self)

class UnaryOp(ASTNode):
    def __init__(self, op, operand):
        super().__init__(Kind.U_OP, None)
        self.op = op
        self.operand = operand
        
        if not Type.is_type_ok(operand.type, op, is_unary=True):
            raise_error(TypeError("Incompatible types for an operator! (operand type:{}, operator:{})".format(operand.type, op)))
        self.type = Type.combine(operand.type, op)
    
    def accept(self, tree_walker):
        return tree_walker.visit_uop(self)

class Declaration(ASTNode):
    def __init__(self, ident):
        super().__init__(Kind.DECLARE, None)
        self.ident = ident
        self.type = self.ident.type
    
    def accept(self, tree_walker):
        return tree_walker.visit_decl(self)

class Assign(ASTNode):
    def __init__(self, ident, expr):
        super().__init__(Kind.ASSIGN, None)
        self.ident = ident
        self.expr = expr
        
        if not Type.check_match(ident.type, expr.type):
            raise_error(TypeError(self.lineno, "Types does not match! (ident type:{}, expr type:{})".format(ident.type, expr.type)))
    
    def accept(self, tree_walker):
        return tree_walker.visit_assign(self)

class Increment(ASTNode):
    def __init__(self, ident, expr):
        super().__init__(Kind.INC, None)
        self.ident = ident
        self.expr = expr
        
        if not Type.check_match(ident.type, expr.type):
            raise_error(TypeError(self.lineno, "Types does not match! (ident type:{}, expr type:{})".format(ident.type, expr.type)))
        if not Type.is_type_ok(ident.type, '+='):
            raise_error(TypeError(self.lineno, "Incompatible types for an operator (type:{}, operator:{})".format(ident.type, '+=')))
    
    def accept(self, tree_walker):
        return tree_walker.visit_inc(self)

class Decrement(ASTNode):
    def __init__(self, ident, expr):
        super().__init__(Kind.DEC, None)
        self.ident = ident
        self.expr = expr
        
        if not Type.check_match(ident.type, expr.type):
            raise_error(TypeError(self.lineno, "Types does not match! (ident type:{}, expr type:{})".format(ident.type, expr.type)))
        if not Type.is_type_ok(ident.type, '-='):
            raise_error(TypeError(self.lineno, "Incompatible types for an operator (type:{}, operator:{})".format(ident.type, '-=')))
    
    def accept(self, tree_walker):
        return tree_walker.visit_dec(self)

class If(ASTNode):
    def __init__(self, test, block, brs):
        super().__init__(Kind.IF, None)
        self.test = test
        self.block = block
        # empty for simple if stmt, contains a element (else branch) for if-else stmt,
        # >1 elements means elif branch (s) preceding the else branch
        self.brs = brs
        
        if not Type.is_bool(test.type):
            raise_error(TypeError(self.lineno, "Expression inside (...) must return bool! (It returns {} instead)".format(test.type)))
    
    def accept(self, tree_walker):
        return tree_walker.visit_if(self)

class While(ASTNode):
    def __init__(self, test, block):
        super().__init__(Kind.WHILE, None)
        self.test = test
        self.block = block
        
        if not Type.is_bool(test.type):
            raise_error(TypeError(self.lineno, "Expression inside (...) must return bool! (It returns {} instead)".format(test.type)))
    
    def accept(self, tree_walker):
        return tree_walker.visit_while(self)

class For(ASTNode):
    def __init__(self, init, test, stmt, block):
        super().__init__(Kind.FOR, None)
        self.init = init
        self.test = test
        self.stmt = stmt
        self.block = block
        
        if not Type.is_bool(test.type):
            raise_error(TypeError(self.lineno, "Expression inside (...) must return bool! (It returns {} instead)".format(test.type)))
    
    def accept(self, tree_walker):
        return tree_walker.visit_for(self)

class DoWhile(ASTNode):
    def __init__(self, block, test):
        super().__init__(Kind.DO_WHILE, None)
        self.block = block
        self.test = test
        
        if not Type.is_bool(test.type):
            raise_error(TypeError(self.lineno, "Expression inside (...) must return bool! (It returns {} instead)".format(test.type)))
    
    def accept(self, tree_walker):
        return tree_walker.visit_dowhile(self)

class Break(ASTNode):
    def __init__(self):
        super().__init__(Kind.BREAK, None)
    
    def accept(self, tree_walker):
        return tree_walker.visit_break(self)

class Continue(ASTNode):
    def __init__(self):
        super().__init__(Kind.CONT, None)
    
    def accept(self, tree_walker):
        return tree_walker.visit_cont(self)

class Expression(ASTNode):
    def __init__(self, expr):
        super().__init__(Kind.EXPR, None)
        self.expr = expr
    
    def accept(self, tree_walker):
        return tree_walker.visit_expr(self)

class Print(ASTNode):
    def __init__(self, arg):
        super().__init__(Kind.PRINT, None)
        self.arg = arg
    
    def accept(self, tree_walker):
        return tree_walker.visit_print(self)

class Scan(ASTNode):
    def __init__(self, ident):
        super().__init__(Kind.SCAN, None)
        self.ident = ident
    
    def accept(self, tree_walker):
        return tree_walker.visit_scan(self)

class Block(ASTNode):
    def __init__(self, prev_blk, stmt):
        super().__init__(Kind.BLOCK, None)
        self.prev_blk = prev_blk
        self.stmt = stmt
    
    def accept(self, tree_walker):
        return tree_walker.visit_blk(self)

class Program(ASTNode):
    def __init__(self, block):
        super().__init__(Kind.PRGM, None)
        self.block = block
    
    def accept(self, tree_walker):
        return tree_walker.visit_prgm(self)

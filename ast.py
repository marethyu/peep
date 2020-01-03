from abc import ABC, abstractmethod
from type import Type

class ASTNode(ABC):
    def __init__(self, lineno):
        self.lineno = lineno
    
    # See http://sourcemaking.com/design_patterns/visitor
    @abstractmethod
    def accept(self, tree_visitor):
        pass

# abstract
class Expression(ASTNode):
    def __init__(self, type, lineno):
        super().__init__(lineno)
        self.type = type
    
    def accept(self, tree_visitor):
        pass

# abstract
class Constant(ASTNode):
    def __init__(self, type, lineno):
        super().__init__(lineno)
        self.type = type
    
    def accept(self, tree_visitor):
        pass

class IntegerConst(Constant):
    def __init__(self, value, lineno):
        super().__init__(Type.INT, lineno)
        self.value = int(value)
    
    def accept(self, tree_visitor):
        tree_visitor.visit_int_const(self)
    
    def __str__(self):
        return "IntegerConst(value={}, lineno={})".format(self.value, self.lineno)

class FloatConstant(Constant):
    def __init__(self, value, lineno):
        super().__init__(Type.FLOAT, lineno)
        self.value = float(value)
    
    def accept(self, tree_visitor):
        tree_visitor.visit_flt_const(self)
    
    def __str__(self):
        return "FloatConstant(value={}, lineno={})".format(self.value, self.lineno)

class BooleanConst(Constant):
    def __init__(self, value, lineno):
        super().__init__(Type.BOOL, lineno)
        self.value = bool(value is "true")
    
    def accept(self, tree_visitor):
        tree_visitor.visit_bool_const(self)
    
    def __str__(self):
        return "BooleanConst(value={}, lineno={})".format(self.value, self.lineno)

class StringLiteral(Constant):
    def __init__(self, value, lineno):
        super().__init__(Type.STRING, lineno)
        self.value = value
    
    def accept(self, tree_visitor):
        tree_visitor.visit_str_literal(self)
    
    def __str__(self):
        return "StringLiteral(value=\"{}\", lineno={})".format(self.value, self.lineno)

class BinaryOp(Expression):
    def __init__(self, left, right, op, lineno):
        # ...

class UnaryOp(Expression):
    pass

class LHSExpression(Expression):
    pass

class ArrayAccess(LHSExpression):
    pass

class FieldAccess(LHSExpression):
    pass

class Identifier(LHSExpression):
    pass

class Variable(Identifier):
    pass

class Array(Identifier):
    pass

class Function(Identifier):
    pass

class Statement(ASTNode):
    pass

class Block(Statement):
    pass

class VarDeclarationStmt(Statement):
    pass

class AssignmentStmt(Statement):
    pass

class IfStatement(Statement):
    pass

class WhileStmt(Statement):
    pass

class ForStatement(Statement):
    pass

class DoWhileStmt(Statement):
    pass

class BreakStatement(Statement):
    pass

class ContinueStmt(Statement):
    pass

class ReturnStmt(Statement):
    pass

class UseStatement(Statement):
    pass

class FunctionCall(Expression, Statement):
    pass

class Scan(FunctionCall):
    pass

class Print(FunctionCall):
    pass

class Assert(FunctionCall):
    pass

class Exit(FunctionCall):
    pass
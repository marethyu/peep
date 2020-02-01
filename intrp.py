from ast import Block, Declaration
from treewalker import TreeWalker
from type import Type

class CallStack(object):
    def __init__(self):
        self.records = []
    
    def push(self, ar):
        self.records.append(ar)
    
    def pop(self):
        self.records.pop()
    
    def top(self):
        return self.records[-1]

class Interpreter(TreeWalker):
    def __init__(self, tree):
        self.stk = CallStack()
        self.tree = tree
    
    def interpret(self):
        if self.tree is not None:
            self.tree.accept(self)
    
    def visit_ident(self, ident):
        ar = self.stk.top()
        return ar[ident.value]
    
    def visit_const(self, const):
        type = const.type
        
        if type == Type.INT:
            return int(const.value)
        elif type == Type.FLOAT:
            return float(const.value)
        elif type == Type.BOOL:
            return const.value == "true"
        else: # type == Type.STRING
            return const.value
    
    def visit_relop(self, relop):
        op = relop.op
        
        if op == "==":
            return relop.left.accept(self, True) == relop.right.accept(self, True)
        elif op == "!=":
            return relop.left.accept(self, True) != relop.right.accept(self, True)
        elif op == "<":
            return relop.left.accept(self, True) < relop.right.accept(self, True)
        elif op == ">":
            return relop.left.accept(self, True) > relop.right.accept(self, True)
        elif op == "<=":
            return relop.left.accept(self, True) <= relop.right.accept(self, True)
        else: # op == ">="
            return relop.left.accept(self, True) >= relop.right.accept(self, True)
    
    def visit_addop(self, addop):
        op = addop.op
        
        if op == "+":
            return addop.left.accept(self, True) + addop.right.accept(self, True)
        elif op == "-":
            return addop.left.accept(self, True) - addop.right.accept(self, True)
        else: # op == "||"
            return addop.left.accept(self, True) or addop.right.accept(self, True)
    
    def visit_op(self, op):
        o = op.op
        
        if o == "*":
            return op.left.accept(self, True) * op.right.accept(self, True)
        elif o == "/":
            type = op.left.type
            
            if type == Type.INT:
                return op.left.accept(self, True) // op.right.accept(self, True)
            
            return op.left.accept(self, True) / op.right.accept(self, True)
        elif o == "%":
            return op.left.accept(self, True) % op.right.accept(self, True)
        else: # o == "&&"
            return op.left.accept(self, True) and op.right.accept(self, True)
    
    def visit_uop(self, uop):
        op = uop.op
        
        if op == "+":
            return uop.operand.accept(self, True)
        elif op == "-":
            return -uop.operand.accept(self, True)
        else: # op == "!"
            return not uop.operand.accept(self, True)
    
    def visit_decl(self, decl):
        ar = self.stk.top()
        self.stk.pop()
        from defaultvals import Default
        ar[decl.ident.value] = Default.default_value(decl.ident.type)
        self.stk.push(ar)
        return decl.ident
    
    def visit_assign(self, assign): # todo: object references (no need to call stack push or pop)
        ident = assign.ident
        if isinstance(ident, Declaration):
            ident = ident.accept(self, True)
        ar = self.stk.top()
        self.stk.pop()
        ar[ident.value] = assign.expr.accept(self, True)
        self.stk.push(ar)
    
    def visit_inc(self, inc):
        ident = inc.ident
        ar = self.stk.top()
        self.stk.pop()
        ar[ident.value] += inc.expr.accept(self, True)
        self.stk.push(ar)
    
    def visit_dec(self, dec):
        ident = dec.ident
        ar = self.stk.top()
        self.stk.pop()
        ar[ident.value] -= dec.expr.accept(self, True)
        self.stk.push(ar)
    
    def visit_if(self, if_):
        if if_.test.accept(self, True):
            if_.block.accept(self)
        elif len(if_.brs) > 0:
            if len(if_.brs) == 1:
                if_.brs[-1].accept(self)
            else:
                for i in range(0, len(if_.brs) - 1):
                    if if_.brs[i].test.accept(self, True):
                        if_.brs[i].block.accept(self)
                        break
                else:
                    if_.brs[-1].accept(self)
    
    def visit_while(self, while_):
        while while_.test.accept(self, True):
            while_.block.accept(self)
    
    def visit_for(self, for_):
        for_.init.accept(self)
        
        while for_.test.accept(self, True):
            for_.block.accept(self)
            for_.stmt.accept(self)
    
    def visit_dowhile(self, dowhile):
        while True:
            dowhile.block.accept(self)
            
            if not dowhile.test.accept(self, True):
                break
    
    def visit_break(self, break_): # todo
        pass
    
    def visit_cont(self, cont): # todo
        pass
    
    def visit_expr(self, expr):
        expr.expr.accept(self)
    
    def visit_print(self, print_): # todo: make print function more specialized for Peep, don't exploit Python's print (ie. instead of printing True by default, print true instead)
        print(print_.arg.accept(self, True))
    
    def visit_blk(self, blk):
        if blk.prev_blk is not None:
            blk.prev_blk.accept(self)
        # oh, there's another block...
        if isinstance(blk.stmt, Block):
            self.stk.push({}) # push a new activation record
            blk.stmt.accept(self)
            self.stk.pop()
        else:
            blk.stmt.accept(self)
    
    def visit_prgm(self, prgm):
        self.stk.push({}) # push the topmost activation record
        prgm.block.accept(self)
        self.stk.pop()
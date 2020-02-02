# TODO: Runtime errors, what to do when there's nothing inside block?

from ast import Block, Declaration
from scope import Scope
from treewalker import TreeWalker
from type import Type

class ActivationRecord(object):
    def __init__(self):
        self.mmap = Scope(None) # memory map
    
    def new_scope(self):
        self.mmap = Scope(self.mmap)
    
    def old_scope(self):
        for key in self.mmap.dct.keys():
            if not self.mmap.lookup_local(key):
                self.mmap.parent[key] = self.mmap[key]
        
        self.mmap = self.mmap.parent
    
    def __getitem__(self, key):
        return self.mmap[key]
    
    def __setitem__(self, key, value):
        self.mmap[key] = value

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
        self.encountered_break = False
        self.encountered_cont = False
    
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
    
    def visit_orop(self, orop):
        return orop.left.accept(self) or orop.right.accept(self)
    
    def visit_andop(self, andop):
        return andop.left.accept(self) and andop.right.accept(self)
    
    def visit_eqop(self, eqop):
        op = eqop.op
        
        if op == "==":
            return eqop.left.accept(self) == eqop.right.accept(self)
        else: # op == "!="
            return eqop.left.accept(self) != eqop.right.accept(self)
    
    def visit_relop(self, relop):
        op = relop.op
        
        if op == "<":
            return relop.left.accept(self) < relop.right.accept(self)
        elif op == ">":
            return relop.left.accept(self) > relop.right.accept(self)
        elif op == "<=":
            return relop.left.accept(self) <= relop.right.accept(self)
        else: # op == ">="
            return relop.left.accept(self) >= relop.right.accept(self)
    
    def visit_addop(self, addop):
        op = addop.op
        
        if op == "+":
            return addop.left.accept(self) + addop.right.accept(self)
        else: # op == "-"
            return addop.left.accept(self) - addop.right.accept(self)
    
    def visit_mulop(self, mulop):
        op = mulop.op
        
        if op == "*":
            return mulop.left.accept(self) * mulop.right.accept(self)
        elif op == "/":
            type = mulop.left.type
            
            if type == Type.INT:
                return mulop.left.accept(self) // mulop.right.accept(self)
            
            return mulop.left.accept(self) / mulop.right.accept(self)
        else: # op == "%"
            return mulop.left.accept(self) % mulop.right.accept(self)
    
    def visit_uop(self, uop):
        op = uop.op
        
        if op == "+":
            return uop.operand.accept(self)
        elif op == "-":
            return -uop.operand.accept(self)
        else: # op == "!"
            return not uop.operand.accept(self)
    
    def visit_decl(self, decl):
        ar = self.stk.top()
        from defaultvals import Default
        ar[decl.ident.value] = Default.default_value(decl.ident.type)
        return decl.ident
    
    def visit_assign(self, assign):
        ident = assign.ident
        if isinstance(ident, Declaration):
            ident = ident.accept(self)
        ar = self.stk.top()
        ar[ident.value] = assign.expr.accept(self)
    
    def visit_inc(self, inc):
        ident = inc.ident
        ar = self.stk.top()
        ar[ident.value] += inc.expr.accept(self)
    
    def visit_dec(self, dec):
        ident = dec.ident
        ar = self.stk.top()
        ar[ident.value] -= dec.expr.accept(self)
    
    def visit_if(self, if_):
        if if_.test.accept(self):
            self.stk.top().new_scope()
            if_.block.accept(self)
            self.stk.top().old_scope()
        elif len(if_.brs) > 0:
            if len(if_.brs) == 1:
                self.stk.top().new_scope()
                if_.brs[-1].accept(self)
                self.stk.top().old_scope()
            else:
                for i in range(0, len(if_.brs) - 1):
                    if if_.brs[i].test.accept(self):
                        self.stk.top().new_scope()
                        if_.brs[i].block.accept(self)
                        self.stk.top().old_scope()
                        break
                else:
                    self.stk.top().new_scope()
                    if_.brs[-1].accept(self)
                    self.stk.top().old_scope()
    
    def visit_while(self, while_):
        self.stk.top().new_scope()
        while while_.test.accept(self):
            while_.block.accept(self)
            
            if self.encountered_break:
                break
            
            if self.encountered_cont:
                self.encountered_cont = False
        
        self.encountered_break = False
        self.stk.top().old_scope()
    
    def visit_for(self, for_):
        self.stk.top().new_scope()
        for_.init.accept(self)
        
        while for_.test.accept(self):
            for_.block.accept(self)
            
            if self.encountered_break:
                break
            
            if self.encountered_cont:
                self.encountered_cont = False
            
            for_.stmt.accept(self)
        
        self.encountered_break = False
        self.stk.top().old_scope()
    
    def visit_dowhile(self, dowhile):
        self.stk.top().new_scope()
        while True:
            dowhile.block.accept(self)
            
            if self.encountered_break:
                break
            
            if self.encountered_cont:
                self.encountered_cont = False
            
            if not dowhile.test.accept(self):
                break
        
        self.encountered_break = False
        self.stk.top().old_scope()
    
    def visit_break(self, break_):
        self.encountered_break = True
    
    def visit_cont(self, cont):
        self.encountered_cont = True
    
    def visit_expr(self, expr):
        expr.expr.accept(self)
    
    def visit_print(self, print_): # todo: make print function more specialized for Peep, don't exploit Python's print (ie. instead of printing True by default, print true instead)
        print(print_.arg.accept(self))
    
    def visit_scan(self, scan):
        ident = scan.ident
        ar = self.stk.top()
        ar[ident.value] = input()
    
    def visit_blk(self, blk):
        if blk.prev_blk is not None:
            blk.prev_blk.accept(self)
        if self.encountered_break or self.encountered_cont:
            return
        if isinstance(blk.stmt, Block):
            self.stk.top().new_scope()
            blk.stmt.accept(self)
            self.stk.top().old_scope()
        else:
            blk.stmt.accept(self)
    
    def visit_prgm(self, prgm):
        self.stk.push(ActivationRecord()) # push the topmost activation record
        prgm.block.accept(self)
        self.stk.pop()
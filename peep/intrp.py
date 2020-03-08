from ast import Block, Declaration
from err import DivisionByZeroError, InputCastingError, raise_runtime_error
from scope import Scope
from treewalker import TreeWalker
from type import Type

class ChainedList:
    def __init__(self, prev):
        self.prev = prev
        self.data = []
    
    def append(self, elm):
        self.data.append(elm)
    
    def elm_exists(self, elm):
        return elm in self.data

class ActivationRecord:
    def __init__(self, filename, current_function, last_lineno):
        self.filename = filename
        self.current_function = current_function
        self.last_lineno = last_lineno
        self.mmap = None # memory map
        self.cl = None
    
    def new_scope(self):
        self.mmap = Scope(self.mmap)
        self.cl = ChainedList(self.cl)
    
    def old_scope(self):
        for key in self.mmap.dct.keys():
            if not self.cl.elm_exists(key):
                self.mmap.parent[key] = self.mmap[key]
        
        self.mmap = self.mmap.parent
        self.cl = self.cl.prev
    
    def __getitem__(self, key):
        return self.mmap[key]
    
    def put(self, key, value, new=False):
        if new:
            self.cl.append(key)
        self.mmap[key] = value

class CallStack:
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
            try:
                self.tree.accept(self)
            except KeyboardInterrupt:
                pass
    
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
        type = eqop.left.type
        
        if type == Type.FLOAT: # built-in float comparison
            left = eqop.left.accept(self)
            right = eqop.right.accept(self)
            
            import math, sys
            if op == "==":
                return math.fabs(left - right) < sys.float_info.epsilon # check left and right are equal
            return math.fabs(left - right) > sys.float_info.epsilon
        
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
                right = mulop.right.accept(self)
                if right == 0:
                    self.stk.top().last_lineno = mulop.right.lineno
                    raise_runtime_error(DivisionByZeroError(mulop.right.lineno), self.stk)
                return mulop.left.accept(self) // right
            
            right = mulop.right.accept(self)
            import math, sys
            if math.fabs(right - 0.0) < sys.float_info.epsilon: # right == 0.0
                self.stk.top().last_lineno = mulop.right.lineno
                raise_runtime_error(DivisionByZeroError(mulop.right.lineno), self.stk)
            return mulop.left.accept(self) / right
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
        ar.put(decl.ident.value, Default.default_value(decl.ident.type), True)
        return decl.ident
    
    def visit_assign(self, assign):
        ident = assign.ident
        if isinstance(ident, Declaration):
            ident = ident.accept(self)
        ar = self.stk.top()
        ar.put(ident.value, assign.expr.accept(self))
    
    def visit_inc(self, inc):
        ident = inc.ident
        ar = self.stk.top()
        val = ar[ident.value]
        ar.put(ident.value, val + inc.expr.accept(self))
    
    def visit_dec(self, dec):
        ident = dec.ident
        ar = self.stk.top()
        val = ar[ident.value]
        ar.put(ident.value, val - dec.expr.accept(self))
    
    def visit_mul_assign(self, mul_assign):
        ident = mul_assign.ident
        ar = self.stk.top()
        val = ar[ident.value]
        ar.put(ident.value, val * mul_assign.expr.accept(self))
    
    def visit_div_assign(self, div_assign):
        ident = div_assign.ident
        ar = self.stk.top()
        val = ar[ident.value]
        
        if ident.type == Type.INT:
            ar.put(ident.value, val // div_assign.expr.accept(self))
        else: # Type.FLOAT
            ar.put(ident.value, val / div_assign.expr.accept(self))
    
    def visit_mod_assign(self, mod_assign):
        ident = mod_assign.ident
        ar = self.stk.top()
        val = ar[ident.value]
        ar.put(ident.value, val % mod_assign.expr.accept(self))
    
    def visit_if(self, if_):
        if if_.test.accept(self):
            self.stk.top().new_scope()
            if if_.block is not None:
                if_.block.accept(self)
            self.stk.top().old_scope()
        elif len(if_.brs) > 0:
            if len(if_.brs) == 1:
                self.stk.top().new_scope()
                if if_.brs[-1] is not None:
                    if_.brs[-1].accept(self)
                self.stk.top().old_scope()
            else:
                for i in range(0, len(if_.brs) - 1):
                    if if_.brs[i].test.accept(self):
                        self.stk.top().new_scope()
                        if if_.brs[i].block is not None:
                            if_.brs[i].block.accept(self)
                        self.stk.top().old_scope()
                        break
                else:
                    self.stk.top().new_scope()
                    if if_.brs[-1] is not None:
                        if_.brs[-1].accept(self)
                    self.stk.top().old_scope()
    
    def visit_while(self, while_):
        self.stk.top().new_scope()
        
        while while_.test.accept(self):
            if while_.block is not None:
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
            if for_.block is not None:
                for_.block.accept(self)
            
            if self.encountered_break:
                break
            
            if self.encountered_cont:
                self.encountered_cont = False
            
            for_.stmt.accept(self)
        
        self.encountered_break = False
        self.stk.top().old_scope()
    
    def visit_break(self, break_):
        self.encountered_break = True
    
    def visit_cont(self, cont):
        self.encountered_cont = True
    
    def visit_expr(self, expr):
        expr.expr.accept(self)
    
    def visit_print(self, print_):
        out = print_.arg.accept(self)
        
        # we don't want to exploit Python's built-in print
        # function too much so a little modification is made
        if isinstance(out, bool):
            print("true" if out else "false")
        else:
            print(out)
    
    def visit_scan(self, scan):
        ident = scan.ident
        inp = input()
        ar = self.stk.top()
        
        if ident.type == Type.INT:
            try:
                ar.put(ident.value, int(inp))
            except ValueError:
                self.stk.top().last_lineno = ident.lineno
                raise_runtime_error(InputCastingError("Cannot cast input to int", ident.lineno), self.stk)
        elif ident.type == Type.FLOAT:
            try:
                ar.put(ident.value, float(inp))
            except ValueError:
                self.stk.top().last_lineno = ident.lineno
                raise_runtime_error(InputCastingError("Cannot cast input to float", ident.lineno), self.stk)
        elif ident.type == Type.BOOL:
            if inp not in ['true', 'false']:
                self.stk.top().last_lineno = ident.lineno
                raise_runtime_error(InputCastingError("Cannot cast input to bool", ident.lineno), self.stk)
            ar.put(ident.value, inp == "true")
        else: # ident.type == Type.STRING
            ar.put(ident.value, inp)
    
    def visit_blk(self, blk):
        if blk.prev_blk is not None:
            blk.prev_blk.accept(self)
        if self.encountered_break or self.encountered_cont:
            return
        if blk.stmt is None:
            return
        if isinstance(blk.stmt, Block):
            self.stk.top().new_scope()
            blk.stmt.accept(self)
            self.stk.top().old_scope()
        else:
            blk.stmt.accept(self)
    
    def visit_prgm(self, prgm):
        import util
        filename = util.filename
        if filename.find('/') != -1:
            filename = filename[filename.rfind('/') + 1:] # remove directory prefix
        self.stk.push(ActivationRecord(filename, "__MAIN", 0)) # push the topmost activation record
        if prgm.block is not None:
            self.stk.top().new_scope()
            prgm.block.accept(self)
            self.stk.top().old_scope()
        self.stk.pop()

from treewalker import TreeWalker

class ActivationRecord(object):
    def __init__(self):
        pass

class RuntimeStack(object):
    def __init__(self):
        pass

class Interpreter(TreeWalker):
    def __init__(self):
        pass
    
    def visit_ident(self, ident):
        pass
    
    def visit_const(self, const):
        pass
    
    def visit_relop(self, relop):
        pass
    
    def visit_addop(self, addop):
        pass
    
    def visit_op(self, op):
        pass
    
    def visit_uop(self, uop):
        pass
    
    def visit_decl(self, decl):
        pass
    
    def visit_assign(self, assign):
        pass
    
    def visit_inc(self, inc):
        pass
    
    def visit_dec(self, dec):
        pass
    
    def visit_if(self, if_):
        pass
    
    def visit_while(self, while_):
        pass
    
    def visit_for(self, for_):
        pass
    
    def visit_dowhile(self, dowhile):
        pass
    
    def visit_break(self, break_):
        pass
    
    def visit_cont(self, cont):
        pass
    
    def visit_expr(self, expr):
        pass
    
    def visit_print(self, print_):
        pass
    
    def visit_blk(self, blk):
        pass
    
    def visit_prgm(self, prgm):
        pass
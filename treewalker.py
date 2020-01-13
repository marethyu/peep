from abc import ABC, abstractmethod

class TreeWalker(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def visit_ident(self, ident):
        pass
    
    @abstractmethod
    def visit_const(self, const):
        pass
    
    @abstractmethod
    def visit_relop(self, relop):
        pass
    
    @abstractmethod
    def visit_addop(self, addop):
        pass
    
    @abstractmethod
    def visit_op(self, op):
        pass
    
    @abstractmethod
    def visit_uop(self, uop):
        pass
    
    @abstractmethod
    def visit_decl(self, decl):
        pass
    
    @abstractmethod
    def visit_assign(self, assign):
        pass
    
    @abstractmethod
    def visit_inc(self, inc):
        pass
    
    @abstractmethod
    def visit_dec(self, dec):
        pass
    
    @abstractmethod
    def visit_if(self, if_):
        pass
    
    @abstractmethod
    def visit_while(self, while_):
        pass
    
    @abstractmethod
    def visit_for(self, for_):
        pass
    
    @abstractmethod
    def visit_dowhile(self, dowhile):
        pass
    
    @abstractmethod
    def visit_break(self, break_):
        pass
    
    @abstractmethod
    def visit_cont(self, cont):
        pass
    
    @abstractmethod
    def visit_expr(self, expr):
        pass
    
    @abstractmethod
    def visit_print(self, print_):
        pass
    
    @abstractmethod
    def visit_blk(self, blk):
        pass
    
    @abstractmethod
    def visit_prgm(self, prgm):
        pass
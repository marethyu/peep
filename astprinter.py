from treewalker import TreeWalker

class ASTPrinter(TreeWalker):
    def __init__(self):
        super().__init__()
        self.indent = 0
    
    def visit_ident(self, ident):
        print(' ' * self.indent + ident.value + " (type={})".format(ident.type)) # value is a name of the identifier
    
    def visit_const(self, const):
        print(' ' * self.indent + const.value + " (type={})".format(const.type))
    
    def visit_relop(self, relop):
        self._emit(relop.op, lambda: [relop.left.accept(self),
                                      relop.right.accept(self)][-1])
    
    def visit_addop(self, addop):
        self._emit(addop.op, lambda: [addop.left.accept(self),
                                      addop.right.accept(self)][-1])
    
    def visit_op(self, op):
        self._emit(op.op, lambda: [op.left.accept(self),
                                   op.right.accept(self)][-1])
    
    def visit_uop(self, uop):
        self._emit(uop.op, lambda: [uop.operand.accept(self)][-1])
    
    def visit_decl(self, decl):
        self._emit('declaration', lambda: [print(' ' * self.indent + str(decl.ident.type)),
                                           decl.ident.accept(self)][-1])
    
    def visit_assign(self, assign):
        self._emit('=', lambda: [assign.ident.accept(self),
                                 assign.expr.accept(self)][-1])
    
    def visit_inc(self, inc):
        self._emit('+=', lambda: [inc.ident.accept(self),
                                  inc.expr.accept(self)][-1])
    
    def visit_dec(self, dec):
        self._emit('-=', lambda: [dec.ident.accept(self),
                                  dec.expr.accept(self)][-1])
    
    def visit_if(self, if_):
        self._emit('if', lambda: [if_.test.accept(self),
                                  if_.block.accept(self),
                                  if_.elif_br.accept(self) if if_.elif_br is not None else None,
                                  if_.else_br.accept(self) if if_.else_br is not None else None][-1])
    
    def visit_while(self, while_):
        self._emit('while', lambda: [while_.test.accept(self),
                                     while_.block.accept(self)][-1])
    
    def visit_for(self, for_):
        self._emit('for', lambda: [for_.init.accept(self),
                                   for_.test.accept(self),
                                   for_.stmt.accept(self),
                                   for_.block.accept(self)][-1])
    
    def visit_dowhile(self, dowhile):
        self._emit('do_while', lambda: [dowhile.block.accept(self),
                                        dowhile.test.accept(self)][-1])
    
    def visit_break(self, break_):
        self._emit('break', lambda: [None])
    
    def visit_cont(self, cont):
        self._emit('continue', lambda: [None])
    
    def visit_expr(self, expr):
        self._emit('expression', lambda: [expr.accept(self)][-1])
    
    def visit_print(self, print_):
        self._emit('print', lambda: [print_.arg.accept(self)][-1])
    
    def visit_blk(self, blk):
        self._emit('block', lambda: [blk.prev_blk.accept(self) if blk.prev_blk is not None else None,
                                     blk.stmt.accept(self)][-1])
    
    def visit_prgm(self, prgm):
        self._emit('program', lambda: [prgm.block.accept(self)][-1])
    
    def _emit(self, node_name, action):
        print(' ' * self.indent + node_name)
        self.indent += 2
        action()
        self.indent -= 2
from treewalker import TreeWalker

class ASTPrinter(TreeWalker):
    def __init__(self, tree):
        super().__init__()
        self.tree = tree
        self.indent = 0
    
    def print_ast(self):
        if self.tree is None:
            return
        print("BEGIN AST")
        self.tree.accept(self)
        print("END AST")
    
    def visit_ident(self, ident):
        print(' ' * self.indent + ident.value + " (type={})".format(ident.type)) # value is a name of the identifier
    
    def visit_const(self, const):
        print(' ' * self.indent + const.value + " (type={})".format(const.type))
    
    def visit_orop(self, orop):
        self._print(orop.op, lambda: [orop.left.accept(self),
                                      orop.right.accept(self)][-1])
    
    def visit_andop(self, andop):
        self._print(andop.op, lambda: [andop.left.accept(self),
                                       andop.right.accept(self)][-1])
    
    def visit_eqop(self, eqop):
        self._print(eqop.op, lambda: [eqop.left.accept(self),
                                      eqop.right.accept(self)][-1])
    
    def visit_relop(self, relop):
        self._print(relop.op, lambda: [relop.left.accept(self),
                                       relop.right.accept(self)][-1])
    
    def visit_addop(self, addop):
        self._print(addop.op, lambda: [addop.left.accept(self),
                                       addop.right.accept(self)][-1])
    
    def visit_mulop(self, mulop):
        self._print(mulop.op, lambda: [mulop.left.accept(self),
                                       mulop.right.accept(self)][-1])
    
    def visit_uop(self, uop):
        self._print(uop.op, lambda: [uop.operand.accept(self)][-1])
    
    def visit_decl(self, decl):
        self._print('declaration', lambda: [print(' ' * self.indent + str(decl.ident.type)),
                                            decl.ident.accept(self)][-1])
    
    def visit_assign(self, assign):
        self._print('=', lambda: [assign.ident.accept(self),
                                  assign.expr.accept(self)][-1])
    
    def visit_inc(self, inc):
        self._print('+=', lambda: [inc.ident.accept(self),
                                   inc.expr.accept(self)][-1])
    
    def visit_dec(self, dec):
        self._print('-=', lambda: [dec.ident.accept(self),
                                   dec.expr.accept(self)][-1])
    
    def visit_if(self, if_):
        print(' ' * self.indent + 'begin_if')
        self.indent += 2
        if_.test.accept(self)
        if_.block.accept(self)
        for branch in if_.brs:
            branch.accept(self)
        self.indent -= 2
        print(' ' * self.indent + 'end_if')
    
    def visit_while(self, while_):
        self._print('while', lambda: [while_.test.accept(self),
                                      while_.block.accept(self)][-1])
    
    def visit_for(self, for_):
        self._print('for', lambda: [for_.init.accept(self),
                                    for_.test.accept(self),
                                    for_.stmt.accept(self),
                                    for_.block.accept(self)][-1])
    
    def visit_dowhile(self, dowhile):
        self._print('do_while', lambda: [dowhile.block.accept(self),
                                         dowhile.test.accept(self)][-1])
    
    def visit_break(self, break_):
        self._print('break', lambda: [None])
    
    def visit_cont(self, cont):
        self._print('continue', lambda: [None])
    
    def visit_expr(self, expr):
        self._print('expression', lambda: [expr.expr.accept(self)][-1])
    
    def visit_print(self, print_):
        self._print('print', lambda: [print_.arg.accept(self)][-1])
    
    def visit_scan(self, scan):
        self._print('scan', lambda: [scan.ident.accept(self)][-1])
    
    def visit_blk(self, blk):
        self._print('block', lambda: [blk.prev_blk.accept(self) if blk.prev_blk is not None else None,
                                      blk.stmt.accept(self)][-1])
    
    def visit_prgm(self, prgm):
        self._print('program', lambda: [prgm.block.accept(self)][-1])
    
    def _print(self, node_name, action):
        print(' ' * self.indent + 'begin_' + node_name)
        self.indent += 2
        action()
        self.indent -= 2
        print(' ' * self.indent + 'end_' + node_name)
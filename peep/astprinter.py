from peep import TreeWalker


class FileBuffer:
    def __init__(self):
        self.lines = []

    def write(self, line):
        self.lines.append(line)


class ASTPrinter(TreeWalker):
    def __init__(self, tree):
        super().__init__()
        self.tree = tree
        self.indent = 0
        self.ind_inc = 2
        self.file = FileBuffer()

    def print_ast(self):
        if self.tree is None:
            return

        self.file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        self.tree.accept(self)

    def visit_ident(self, ident):
        self._file_writeline('<Identifier type=\"{}\" name=\"{}\"></Identifier>'.format(ident.type, ident.value))

    def visit_const(self, const):
        const_val = str(const.value)
        if "&" in const_val:
            possible_lone_amps = const_val.split("&")
            for index, sub_str in enumerate(possible_lone_amps):
                if sub_str.startswith("quot;") or sub_str.startswith("lt;") or \
                        sub_str.startswith("amp;") or sub_str.startswith("gt;"):
                    possible_lone_amps[index] = "amp;" + sub_str

                if index == 0:
                    if possible_lone_amps[0] == "":
                        possible_lone_amps[index] = "amp;" + sub_str
                else:
                    possible_lone_amps[index] = "amp;" + sub_str

            const_val = "&".join(possible_lone_amps)

        const_val = const_val.replace('<', "&lt;")
        const_val = const_val.replace('>', "&gt;")
        const_val = const_val.replace('"', "&quot;")
        const_val = const_val.replace('\'', "&apos;")

        self._file_writeline('<Constant type=\"{}\" value=\"{}\"></Constant>'.format(const.type, const_val))

    def visit_orop(self, orop):
        self._file_writeline('<OrOperator>')
        self.indent += self.ind_inc
        orop.left.accept(self)
        orop.right.accept(self)
        self.indent -= self.ind_inc
        self._file_writeline('</OrOperator>')

    def visit_andop(self, andop):
        self._file_writeline('<AndOperator>')
        self.indent += self.ind_inc
        andop.left.accept(self)
        andop.right.accept(self)
        self.indent -= self.ind_inc
        self._file_writeline('</AndOperator>')

    def visit_eqop(self, eqop):
        self._file_writeline('<EqualityOperator op=\"{}\">'.format(eqop.op))
        self.indent += self.ind_inc
        eqop.left.accept(self)
        eqop.right.accept(self)
        self.indent -= self.ind_inc
        self._file_writeline('</EqualityOperator>')

    def visit_relop(self, relop):
        self._file_writeline('<RelationalOp op=\"{}\">'.format(relop.op))
        self.indent += self.ind_inc
        relop.left.accept(self)
        relop.right.accept(self)
        self.indent -= self.ind_inc
        self._file_writeline('</RelationalOp>')

    def visit_addop(self, addop):
        self._file_writeline('<AddictiveOp op=\"{}\">'.format(addop.op))
        self.indent += self.ind_inc
        addop.left.accept(self)
        addop.right.accept(self)
        self.indent -= self.ind_inc
        self._file_writeline('</AddictiveOp>')

    def visit_mulop(self, mulop):
        self._file_writeline('<MultiplicativeOp op=\"{}\">'.format(mulop.op))
        self.indent += self.ind_inc
        mulop.left.accept(self)
        mulop.right.accept(self)
        self.indent -= self.ind_inc
        self._file_writeline('</MultiplicativeOp>')

    def visit_uop(self, uop):
        self._file_writeline('<UnaryOp op=\"{}\">'.format(uop.op))
        self.indent += self.ind_inc
        uop.operand.accept(self)
        self.indent -= self.ind_inc
        self._file_writeline('</UnaryOp>')

    def visit_decl(self, decl):
        self._file_writeline('<Declaration>')
        self.indent += self.ind_inc
        decl.ident.accept(self)
        self.indent -= self.ind_inc
        self._file_writeline('</Declaration>')

    def visit_assign(self, assign):
        self._file_writeline('<Assign>')
        self.indent += self.ind_inc
        assign.ident.accept(self)
        assign.expr.accept(self)
        self.indent -= self.ind_inc
        self._file_writeline('</Assign>')

    def visit_inc(self, inc):
        self._file_writeline('<Increment>')
        self.indent += self.ind_inc
        inc.ident.accept(self)
        inc.expr.accept(self)
        self.indent -= self.ind_inc
        self._file_writeline('</Increment>')

    def visit_dec(self, dec):
        self._file_writeline('<Decrement>')
        self.indent += self.ind_inc
        dec.ident.accept(self)
        dec.expr.accept(self)
        self.indent -= self.ind_inc
        self._file_writeline('</Decrement>')

    def visit_mul_assign(self, mul_assign):
        self._file_writeline('<MultiplicativeAssign>')
        self.indent += self.ind_inc
        mul_assign.ident.accept(self)
        mul_assign.expr.accept(self)
        self.indent -= self.ind_inc
        self._file_writeline('</MultiplicativeAssign>')

    def visit_div_assign(self, div_assign):
        self._file_writeline('<DivisionAssign>')
        self.indent += self.ind_inc
        div_assign.ident.accept(self)
        div_assign.expr.accept(self)
        self.indent -= self.ind_inc
        self._file_writeline('</DivisionAssign>')

    def visit_mod_assign(self, mod_assign):
        self._file_writeline('<ModulusAssign>')
        self.indent += self.ind_inc
        mod_assign.ident.accept(self)
        mod_assign.expr.accept(self)
        self.indent -= self.ind_inc
        self._file_writeline('</ModulusAssign>')

    def visit_if(self, if_):
        self._file_writeline('<If>')
        self.indent += self.ind_inc

        if_.test.accept(self)
        if if_.block is None:
            self._file_writeline('<Block>')
            self._file_writeline('</Block>')
        else:
            if_.block.accept(self)
        for branch in if_.brs:
            if branch is None:
                self._file_writeline('<Block>')
                self._file_writeline('</Block>')
            else:
                branch.accept(self)

        self.indent -= self.ind_inc
        self._file_writeline('</If>')

    def visit_while(self, while_):
        self._file_writeline('<While>')
        self.indent += self.ind_inc

        while_.test.accept(self)
        if while_.block is None:
            self._file_writeline('<Block>')
            self._file_writeline('</Block>')
        else:
            while_.block.accept(self)

        self.indent -= self.ind_inc
        self._file_writeline('</While>')

    def visit_for(self, for_):
        self._file_writeline('<For>')
        self.indent += self.ind_inc

        for_.init.accept(self)
        for_.test.accept(self)
        for_.stmt.accept(self)
        if for_.block is None:
            self._file_writeline('<Block>')
            self._file_writeline('</Block>')
        else:
            for_.block.accept(self)

        self.indent -= self.ind_inc
        self._file_writeline('</For>')

    def visit_break(self, break_):
        self._file_writeline('<Break></Break>')

    def visit_cont(self, cont):
        self._file_writeline('<Continue></Continue>')

    def visit_expr(self, expr):
        self._file_writeline('<Expression>')
        self.indent += self.ind_inc
        expr.expr.accept(self)
        self.indent -= self.ind_inc
        self._file_writeline('</Expression>')

    def visit_print(self, print_):
        self._file_writeline('<Print>')
        self.indent += self.ind_inc
        print_.arg.accept(self)
        self.indent -= self.ind_inc
        self._file_writeline('</Print>')

    def visit_scan(self, scan):
        self._file_writeline('<Scan>')
        self.indent += self.ind_inc
        scan.ident.accept(self)
        self.indent -= self.ind_inc
        self._file_writeline('</Scan>')

    def visit_blk(self, blk):
        self._file_writeline('<Block>')
        self.indent += self.ind_inc

        if blk.prev_blk is None:
            self._file_writeline('<Block>')
            self._file_writeline('</Block>')
        else:
            blk.prev_blk.accept(self)
        if blk.stmt is None:
            self._file_writeline('<EmptyStatement>')
            self._file_writeline('</EmptyStatement>')
        else:
            blk.stmt.accept(self)

        self.indent -= self.ind_inc
        self._file_writeline('</Block>')

    def visit_prgm(self, prgm):
        self._file_writeline('<Program>')
        self.indent += self.ind_inc

        if prgm.block is None:
            self._file_writeline('<Block>')
            self._file_writeline('</Block>')
        else:
            prgm.block.accept(self)

        self.indent -= self.ind_inc
        self._file_writeline('</Program>')

    def _file_writeline(self, line):
        self.file.write(' ' * self.indent + line + '\n')

    def write(self, file_name):
        with open(file_name + ".ast.xml", "w") as ast:
            ast.writelines(self.file.lines)

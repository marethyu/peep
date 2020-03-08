from ast import *
from err import DuplicateIdentError, UndeclaredIdentError, SyntaxError, raise_error
from scope import Scope
from token import TokenTag as Tag
from type import Type

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.symtab = None
        self.look = None
        self.in_loop = False
        self._move()
    
    def parse(self):
        """
        Returns a root of AST
        
        <program> ::= <block>
        """
        node = Program(self._block())
        self._match(Tag.EOF)
        return node
    
    def _block(self):
        """<block> ::= "{" { <statement> } "}"""
        node = None
        
        self.symtab = Scope(self.symtab)
        self._match(Tag.LBRACK)
        
        while self.look.tag is not Tag.RBRACK:
            prev_blk = node
            node = Block(prev_blk, self._statement())
        
        self._match(Tag.RBRACK)
        self.symtab = self.symtab.parent
        
        return node
    
    def _statement(self):
        """
        <statement> ::= "if" <paren_expression> <block> [ [ "else" "if" <paren_expression> <block> ] "else" <block> ] |
                        "while" <paren_expression> <block> |
                        "for" "(" <declare_assign> ";" <expression> ";" <assignment> | <increment> | <decrement> | <mul_assign> | <div_assign> | <mod_assign> ")" <block> |
                        "break" |
                        "continue" |
                        <block> |
                        <declaration> ";" |
                        <declare_assign> ";" |
                        <assignment> ";" |
                        <expression> ";" |
                        <increment> ";" |
                        <decrement> ";" |
                        <mul_assign> ";" |
                        <div_assign> ";" |
                        <mod_assign> ";" |
                        "print" <paren_expression> ";" |
                        "scan" "(" <identifier> ")"|
                        ";"
        """
        node = None
        
        if self.look.tag is Tag.IF:
            self._match(Tag.IF)
            node = If(self._paren_expr(), self._block(), [])
            
            while self.look.tag is Tag.ELSE:
                self._match(Tag.ELSE)
                
                if self.look.tag is Tag.IF:
                    self._match(Tag.IF)
                    node.brs.append(If(self._paren_expr(), self._block(), [])) # consume else-if branch
                else: # self.look.tag is Tag.LBRACK
                    node.brs.append(self._block()) # consume else branch
                    break
        elif self.look.tag is Tag.WHILE:
            self._match(Tag.WHILE)
            self.in_loop = True
            node = While(self._paren_expr(), self._block())
            self.in_loop = False
        elif self.look.tag is Tag.FOR:
            # we're doing this early because we want the initialization statement to
            # be inside a for-loop scope not the scope outside the loop
            self.symtab = Scope(self.symtab)
            
            init = None
            test = None
            stmt = None
            block = None
            
            self._match(Tag.FOR)
            self._match(Tag.LPAREN)
            
            init = self._declaration(True)
            test = self._expr()
            self._match(Tag.SEMICOLON)
            
            ident = self._check_ident()
            
            if self.look.tag is Tag.ASSIGN:
                stmt = self._assign(ident)
            elif self.look.tag is Tag.PLUS_EQ:
                stmt = self._inc(ident)
            elif self.look.tag is Tag.MINUS_EQ:
                stmt = self._dec(ident)
            elif self.look.tag is Tag.MUL_EQ:
                stmt = self._mul_eq(ident)
            elif self.look.tag is Tag.DIV_EQ:
                stmt = self._div_eq(ident)
            elif self.look.tag is Tag.MOD_EQ:
                stmt = self._mod_eq(ident)
            else:
                raise_error(SyntaxError("Expected '=', '+=', '-=', '*=', '/=', '%=' but got {} instead!".format(self.look.tag), self.look.lineno))
            
            self._match(Tag.RPAREN)
            self.in_loop = True
            self._match(Tag.LBRACK)
            
            block_node = None
            
            while self.look.tag is not Tag.RBRACK:
                prev_blk = block_node
                block_node = Block(prev_blk, self._statement())
            
            self._match(Tag.RBRACK)
            node = For(init, test, stmt, block_node)
            self.in_loop = False
            self.symtab = self.symtab.parent
        elif self.look.tag is Tag.BREAK:
            if not self.in_loop:
                raise_error(SyntaxError("break is used outside of a loop!", self.look.lineno))
            self._match(Tag.BREAK)
            node = Break()
            self._match(Tag.SEMICOLON)
        elif self.look.tag is Tag.CONTINUE:
            if not self.in_loop:
                raise_error(SyntaxError("continue is used outside of a loop!", self.look.lineno))
            self._match(Tag.CONTINUE)
            node = Continue()
            self._match(Tag.SEMICOLON)
        elif self.look.tag is Tag.LBRACK:
            node = self._block()
        elif self.look.tag in [Tag.INT, Tag.FLOAT, Tag.BOOL, Tag.STRING]:
            node = self._declaration(False)
        elif self.look.tag is Tag.IDENT:
            ident = self._check_ident()
            
            if self.look.tag is Tag.ASSIGN:
                node = self._assign(ident)
            elif self.look.tag is Tag.PLUS_EQ:
                node = self._inc(ident)
            elif self.look.tag is Tag.MINUS_EQ:
                node = self._dec(ident)
            elif self.look.tag is Tag.MUL_EQ:
                node = self._mul_eq(ident)
            elif self.look.tag is Tag.DIV_EQ:
                node = self._div_eq(ident)
            elif self.look.tag is Tag.MOD_EQ:
                node = self._mod_eq(ident)
            else:
                raise_error(SyntaxError("Expected '=', '+=', '-=', '*=', '/=', '%=' but got {} instead!".format(self.look.tag), self.look.lineno))
            
            self._match(Tag.SEMICOLON)
        elif self.look.tag is Tag.PRINT:
            self._match(Tag.PRINT)
            node = Print(self._paren_expr())
            self._match(Tag.SEMICOLON)
        elif self.look.tag is Tag.SCAN:
            self._match(Tag.SCAN)
            self._match(Tag.LPAREN)
            node = Scan(self._check_ident())
            self._match(Tag.RPAREN)
            self._match(Tag.SEMICOLON)
        elif self.look.tag is Tag.SEMICOLON: # empty statement
            self._match(Tag.SEMICOLON)
        else: # expression
            node = Expression(self._expr())
            self._match(Tag.SEMICOLON)
        
        return node
    
    def _assign(self, ident):
        """<assignment> ::= <identifier> "=" <expression>"""
        self._match(Tag.ASSIGN)
        return Assign(ident, self._expr())
    
    def _declaration(self, force_assign):
        """
        <declare_assign> ::= <declaration> "=" <expression>
        <declaration> ::= <builtin_type> <identifier>
        """
        type = None
        
        if self.look.tag is Tag.INT:
            type = Type.INT
            self._match(Tag.INT)
        elif self.look.tag is Tag.FLOAT:
            type = Type.FLOAT
            self._match(Tag.FLOAT)
        elif self.look.tag is Tag.BOOL:
            type = Type.BOOL
            self._match(Tag.BOOL)
        else:
            type = Type.STRING
            self._match(Tag.STRING)
        
        ident = Identifier(type, self.look.lexeme)
        
        # the new identifier must not exist in local scope
        if self.symtab.lookup_local(self.look.lexeme) is not None:
            raise_error(DuplicateIdentError(self.look.lexeme, self.look.lineno))
        self.symtab[self.look.lexeme] = ident
        
        self._match(Tag.IDENT)
        
        if not force_assign and self.look.tag is Tag.SEMICOLON:
            self._match(Tag.SEMICOLON)
            return Declaration(ident)
        else:
            self._match(Tag.ASSIGN)
            node = Assign(Declaration(ident), self._expr())
            self._match(Tag.SEMICOLON)
            return node
    
    def _inc(self, ident):
        """<increment> ::= <identifier> "+=" <expression>"""
        self._match(Tag.PLUS_EQ)
        return Increment(ident, self._expr())
    
    def _dec(self, ident):
        """<decrement> ::= <identifier> "-=" <expression>"""
        self._match(Tag.MINUS_EQ)
        return Decrement(ident, self._expr())
    
    def _mul_eq(self, ident):
        """<mul_assign> ::= <identifier> "*=" <expression>"""
        self._match(Tag.MUL_EQ)
        return MultiplicativeAssign(ident, self._expr())
    
    def _div_eq(self, ident):
        """<div_assign> ::= <identifier> "/=" <expression>"""
        self._match(Tag.DIV_EQ)
        return DivisionAssign(ident, self._expr())
    
    def _mod_eq(self, ident):
        """<mod_assign> ::= <identifier> "%=" <expression>"""
        self._match(Tag.MOD_EQ)
        return ModulusAssign(ident, self._expr())
    
    def _paren_expr(self):
        """<paren_expression> ::= "(" <expression> ")"""
        node = None
        
        self._match(Tag.LPAREN)
        node = self._expr()
        self._match(Tag.RPAREN)
        
        return node
    
    def _expr(self):
        """<expression> ::= <or_operand> [ "||" <or_operand> ]"""
        expr = self._or_operand()
        
        while self.look.tag is Tag.OR:
            self._match(Tag.OR)
            expr = OrOperator(expr, self._or_operand())
        
        return expr
    
    def _or_operand(self):
        """<or_operand> ::= <and_operand> [ "&&" <and_operand> ]"""
        or_operand = self._and_operand()
        
        while self.look.tag is Tag.AND:
            self._match(Tag.AND)
            or_operand = AndOperator(or_operand, self._and_operand())
        
        return or_operand
    
    def _and_operand(self):
        """<and_operand> ::= <equality_operand> [ <equality_op> <equality_operand> ]"""
        and_operand = self._eq_operand()
        
        while self.look.tag is Tag.EQ_OP:
            op = self.look.lexeme
            self._match(Tag.EQ_OP)
            and_operand = EqualityOp(and_operand, self._eq_operand(), op)
        
        return and_operand
    
    def _eq_operand(self):
        """<equality_operand> ::= <simple_expression> [ <relational_op> <simple_expression> ]"""
        eq_operand = self._simple_expr()
        
        while self.look.tag is Tag.REL_OP:
            op = self.look.lexeme
            self._match(Tag.REL_OP)
            eq_operand = RelationalOp(eq_operand, self._simple_expr(), op)
        
        return eq_operand
    
    def _simple_expr(self):
        """<simple_expression> ::= <term> [ <addictive_op> <term> ]"""
        simpl_expr = self._term()
        
        while self.look.tag is Tag.ADD_OP:
            op = self.look.lexeme
            self._match(Tag.ADD_OP)
            simpl_expr = AddictiveOp(simpl_expr, self._term(), op)
        
        return simpl_expr
    
    def _term(self):
        """<term> ::= <factor> [ <multiplicative_op> <factor> ]"""
        term = self._factor()
        
        while self.look.tag is Tag.MUL_OP:
            op = self.look.lexeme
            self._match(Tag.MUL_OP)
            term = MultiplicativeOp(term, self._factor(), op)
        
        return term
    
    def _factor(self):
        """
        <factor> ::= [ <unary_op> ] <int_constant> |
                     [ <unary_op> ] <real_constant> |
                     [ <unary_op> ] <bool_const> |
                     [ <unary_op> ] <paren_expression> |
                     [ <unary_op> ] <identifier> |
                     <string_literal>
        """
        if self.look.tag is Tag.INT_CONST:
            node = Constant(Type.INT, self.look.lexeme)
            self._match(Tag.INT_CONST)
            return node
        elif self.look.tag is Tag.RL_CONST:
            node = Constant(Type.FLOAT, self.look.lexeme)
            self._match(Tag.RL_CONST)
            return node
        elif self.look.tag in [Tag.TRUE, Tag.FALSE]:
            node = Constant(Type.BOOL, self.look.lexeme)
            self._match(self.look.tag)
            return node
        elif self.look.tag is Tag.LPAREN:
            return self._paren_expr()
        elif self.look.tag is Tag.IDENT:
            ident = self._check_ident()
            return ident
        elif self.look.tag is Tag.UNARY_OP:
            op = self.look.lexeme
            self._match(Tag.UNARY_OP)
            return UnaryOp(op, self._factor())
        elif self.look.tag is Tag.STR_LITERAL:
            node = Constant(Type.STRING, self.look.lexeme)
            self._match(Tag.STR_LITERAL)
            return node
        else:
            raise_error(SyntaxError("Unexpected token in expression! ({})".format(self.look.tag), self.look.lineno))
    
    def _check_ident(self):
        symb = self.look.lexeme
        
        self._match(Tag.IDENT)
        ident = self.symtab[symb]
        
        if ident is None:
            raise_error(UndeclaredIdentError(symb, self.look.lineno))
        
        return ident
    
    def _match(self, tag):
        if self.look.tag is not tag:
            raise_error(SyntaxError("Expected {} but got {}!".format(tag, self.look.tag), self.look.lineno))
        self._move()
    
    def _move(self):
        self.look = self.lexer.next_token()

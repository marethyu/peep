from ast import *
from err import DuplicateIdentError, UndeclaredIdentError, SyntaxError
from token import TokenTag as Tag
from type import Type

class Scope(object):
    def __init__(self, parent):
        self.parent = parent
        self.symtab = {}
    
    # parameter symb is identifier's name
    def put(self, symb, ident):
        self.symtab[symb] = ident
    
    def lookup_local(self, symb):
        return self.symtab.get(symb)
    
    def lookup(self, symb):
        scope = self
        
        while scope is not None:
            entry = scope.symtab.get(symb)
            
            if entry is not None:
                return entry
            
            scope = scope.parent
        
        return None

class Parser(object):
    """EBNF for Peep programming language
    
    <program> ::= <block>
    <block> ::= "{" { <statement> } "}"
    <statement> ::= "if" <paren_expression> <block> [ [ "else" "if" <paren_expression> <block> ] "else" <block> ] |
                    "while" <paren_expression> <block> |
                    "for" "(" <declare_assign> ";" <expression> ";" <assignment> | <increment> | <decrement> ")" <block> |
                    "do" <block> "while" <paren_expression> ";" |
                    "break" |
                    "continue" |
                    <block> |
                    <declaration> ";" |
                    <declare_assign> ";" |
                    <assignment> ";" |
                    <expression> ";" |
                    <increment> ";" |
                    <decrement> ";" |
                    "print" <paren_expression> ";" |
                    ";"
    <assignment> ::= <identifier> "=" <expression>
    <declare_assign> ::= <declaration> "=" <expression>
    <declaration> ::= <builtin_type> <identifier>
    <increment> ::= <identifier> "+=" <expression>
    <decrement> ::= <identifier> "-=" <expression>
    <paren_expression> ::= "(" <expression> ")"
    <expression> ::= <simple_expression> [ <relational_op> <simple_expression> ]
    <simple_expression> ::= <term> [ <addictive_op> <term> ]
    <term> ::= <factor> [ <op> <factor> ]
    <factor> ::= [ <unary_op> ] <int_constant> |
                 [ <unary_op> ] <real_constant> |
                 [ <unary_op> ] <bool_const> |
                 [ <unary_op> ] <paren_expression> |
                 [ <unary_op> ] <identifier> |
                 <string_literal>
    <identifier> ::= <alpha> [ <alpha_num> ]
    <builtin_type> ::= "int" | "float" | "bool" | "string"
    <relational_op> ::= "==" | "!=" | "<" | ">" | "<=" | ">="
    <addictive_op> ::= "+" | "-" | "||"
    <op> ::= "*" | "/" | "%" | "&&"
    <unary_op> ::= "+" | "-" | "!"
    <int_constant> ::= <digit> [ <digit> ]
    <real_constant> ::= <int_constant> "." <digit> [ <digit> ]
    <bool_const> ::= "true" | "false"
    <string_literal> ::= "\"" <character> [ <character> ] "\""
    <digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
    <alpha> ::= "a" | "b" | "c" | "d" | "e" | ... | "z"
    <alpha_num> ::= <digit> | <alpha>
    <character> ::= <alpha_num> | "\" <escape_seq>
    <escape_seq> ::= "n" | "t" | "\"" | "'" | "\" | "a" | "b" | "f" | "r" | "v"
    
    ********************************************************************************
    
    IMPORTANT: PLEASE START SMALL!
    
    Next steps (not necessary in order):
    - Global variables
    - Command line arguments
    - Generalize for statement
    - Functions
    - Builtin functions
    - Variable references
    - Casting
    - Arrays
    - Modules
    - Classes
    """
    
    def __init__(self, lexer):
        self.lexer = lexer
        self.env = None
        self.look = None
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
        
        self.env = Scope(self.env)
        self._match(Tag.LBRACK)
        
        while self.look.tag is not Tag.RBRACK:
            prev_blk = node
            node = Block(prev_blk, self._statement())
        
        self._match(Tag.RBRACK)
        self.env = self.env.parent
        
        return node
    
    def _statement(self):
        """
        <statement> ::= "if" <paren_expression> <block> [ [ "else" "if" <paren_expression> <block> ] "else" <block> ] |
                        "while" <paren_expression> <block> |
                        "for" "(" <declare_assign> ";" <expression> ";" <assignment> | <increment> | <decrement> ")" <block> |
                        "do" <block> "while" <paren_expression> ";" |
                        "break" |
                        "continue" |
                        <block> |
                        <declaration> ";" |
                        <declare_assign> ";" |
                        <assignment> ";" |
                        <expression> ";" |
                        <increment> ";" |
                        <decrement> ";" |
                        "print" <paren_expression> ";" |
                        ";"
        """
        node = None
        
        if self.look.tag is Tag.IF:
            self._match(Tag.IF)
            node = If(self._paren_expr(), self._block())
            
            if self.look.tag is Tag.ELSE:
                self._match(Tag.ELSE)
                
                elif_br = None
                else_br = None
                
                if self.look.tag is Tag.IF:
                    elif_br = self._statement() # consume another if statement recursively
                else: # self.look.tag is Tag.LBRACK
                    else_br = self._block() # consume else branch
                
                node.elif_br = elif_br
                node.else_br = else_br
        elif self.look.tag is Tag.WHILE:
            self._match(Tag.WHILE)
            node = While(self._paren_expr(), self._block())
        elif self.look.tag is Tag.FOR:
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
            else:
                raise SyntaxError(self.look.tag, self.look.lineno)
            
            self._match(Tag.RPAREN)
            
            node = For(init, test, stmt, self._block())
        elif self.look.tag is Tag.DO:
            self._match(Tag.DO)
            block = self._block()
            self._match(Tag.WHILE)
            node = DoWhile(block, self._paren_expr())
            self._match(Tag.SEMICOLON)
        elif self.look.tag is Tag.BREAK:
            self._match(Tag.BREAK)
            node = Break()
            self._match(Tag.SEMICOLON)
        elif self.look.tag is Tag.CONTINUE:
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
            else:
                raise SyntaxError(self.look.tag, self.look.lineno)
            
            self._match(Tag.SEMICOLON)
        elif self.look.tag is Tag.PRINT:
            self._match(Tag.PRINT)
            node = Print(self._paren_expr())
            self._match(Tag.SEMICOLON)
        else: # expression
            node = self._expr()
        
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
        if self.env.lookup_local(self.look.lexeme) is not None:
            raise DuplicateIdentError(self.look.lexeme, self.look.lineno)
        self.env.put(self.look.lexeme, ident)
        
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
    
    def _paren_expr(self):
        """<paren_expression> ::= "(" <expression> ")"""
        node = None
        
        self._match(Tag.LPAREN)
        node = self._expr()
        self._match(Tag.RPAREN)
        
        return node
    
    def _expr(self):
        """<expression> ::= <simple_expression> [ <relational_op> <simple_expression> ]"""
        expr = self._simple_expr()
        
        while self.look.tag is Tag.REL_OP:
            op = self.look.lexeme
            self._match(Tag.REL_OP)
            expr = RelationalOp(expr, self._simple_expr(), op)
        
        return expr
    
    def _simple_expr(self):
        """<simple_expression> ::= <term> [ <addictive_op> <term> ]"""
        sim_expr = self._term()
        
        while self.look.tag is Tag.ADD_OP:
            op = self.look.lexeme
            self._match(Tag.ADD_OP)
            sim_expr = AddictiveOp(sim_expr, self._term(), op)
        
        return sim_expr
    
    def _term(self):
        """<term> ::= <factor> [ <op> <factor> ]"""
        term = self._factor()
        
        while self.look.tag is Tag.OP:
            op = self.look.lexeme
            self._match(Tag.OP)
            term = Operator(term, self._factor(), op)
        
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
            raise SyntaxError(self.look.tag, self.look.lineno)
    
    def _check_ident(self):
        symb = self.look.lexeme
        
        self._match(Tag.IDENT)
        ident = self.env.lookup(symb)
        
        if ident is None:
            raise UndeclaredIdentError(symb, self.look.lineno)
        
        return ident
    
    def _match(self, tag):
        if self.look.tag is not tag:
            raise SyntaxError(self.look.tag, self.look.lineno)
        self._move()
    
    def _move(self):
        self.look = self.lexer.next_token()
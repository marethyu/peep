from ast import *
from err import UndeclaredIdentError, SyntaxError
from token import TokenTag
from type import Type

class Scope(object):
    def __init__(self, parent):
        self.parent = parent
        self.symtab = {}
    
    # parameter symb is identifier's name
    def put(self, symb, ident):
        self.symtab[symb] = ident
    
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
    <declare_assign> ::= <builtin_type> <identifier> "=" <expression>
    <declaration> ::= <builtin_type> <identifier>
    <increment> ::= <identifier> "+=" <expression>
    <decrement> ::= <identifier> "-=" <expression>
    <paren_expression> ::= "(" <expression> ")"
    <expression> ::= <simple_expression> [ <relational_op> <simple_expression> ]
    <simple_expression> ::= <term> [ <addictive_op> <term> ]
    <term> ::= <factor> [ <op> <factor> ]
    <factor> ::= [ <unary_op> ] <int_constant> |
                 [ <unary_op> ] <real_constant> |
                 [ <unary_op> ] <paren_expression> |
                 <bool_const> |
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
        return Program(self._block())
    
    def _block(self):
        """<block> ::= "{" { <statement> } "}""""
        node = None
        
        self._match(TokenTag.LBRACK)
        
        while self.look.tag is not TokenTag.RBRACK:
            prev_blk = node
            node = Block(prev_blk, self._statement())
        
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
        
        if self.look.tag is TokenTag.IF:
            self._match(TokenTag.IF)
            node = If(self._paren_expr(), self._block())
            
            if self.look.tag is TokenTag.ELSE:
                self._match(TokenTag.ELSE)
                
                elif_br = None
                else_br = None
                
                if self.look.tag is TokenTag.IF:
                    elif_br = self._statement() # consume another if statement recursively
                else: # self.look.tag is TokenTag.LBRACK
                    else_br = self._block() # consume else branch
                
                node.elif_br = elif_br
                node.else_br = else_br
        elif self.look.tag is TokenTag.WHILE:
            self._match(TokenTag.WHILE)
            node = While(self._paren_expr(), self._block())
        elif self.look.tag is TokenTag.FOR:
            init = None
            test = None
            stmt = None
            block = None
            
            self._match(TokenTag.FOR)
            self._match(TokenTag.LPAREN)
            
            init = self._declaration(True)
            test = self._expr()
            self._match(TokenTag.SEMICOLON)
            
            ident = self._check_ident()
            
            if self.look.tag is TokenTag.ASSIGN:
                stmt = self._assign(ident)
            elif self.look.tag is TokenTag.PLUS_EQ:
                stmt = self._inc(ident)
            elif self.look.tag is TokenTag.MINUS_EQ:
                stmt = self._dec(ident)
            else:
                raise SyntaxError(self.look.tag, self.look.lineno)
            
            self._match(TokenTag.RPAREN)
            
            node = For(init, test, stmt, self._block())
        elif self.look.tag is TokenTag.DO:
            self._match(TokenTag.DO)
            node = DoWhile(self._block(), self._paren_expr())
            self._match(TokenTag.SEMICOLON)
        elif self.look.tag is TokenTag.BREAK:
            self._match(TokenTag.BREAK)
            node = Break()
            self._match(TokenTag.SEMICOLON)
        elif self.look.tag is TokenTag.CONTINUE:
            self._match(TokenTag.CONTINUE)
            node = Continue()
            self._match(TokenTag.SEMICOLON)
        elif self.look.tag is TokenTag.LBRACK:
            node = self._block()
        elif self.look.tag in [TokenTag.INT, TokenTag.FLOAT, TokenTag.BOOL, TokenTag.STRING]:
            node = self._declaration(False)
        elif self.look.tag is TokenTag.IDENT:
            ident = self._check_ident()
            
            if self.look.tag is TokenTag.ASSIGN:
                node = self._assign(ident)
            elif self.look.tag is TokenTag.PLUS_EQ:
                node = self._inc(ident)
            elif self.look.tag is TokenTag.MINUS_EQ:
                node = self._dec(ident)
            else:
                raise SyntaxError(self.look.tag, self.look.lineno)
            
            self._match(TokenTag.SEMICOLON)
        elif self.look.tag is TokenTag.PRINT:
            self._match(TokenTag.PRINT)
            node = Print(self._paren_expr())
        else: # expression
            node = self._expr()
        
        return node
    
    def _assign(self, ident):
        self._match(TokenTag.ASSIGN)
        return Assign(ident, self._expr())
    
    def _declaration(self, force_assign):
        type = None
        
        if self.look.tag is TokenTag.INT:
            type = Type.INT
            self._match(TokenTag.INT)
        elif self.look.tag is TokenTag.FLOAT:
            type = Type.FLOAT
            self._match(TokenTag.FLOAT)
        elif self.look.tag is TokenTag.BOOL:
            type = Type.BOOL
            self._match(TokenTag.BOOL)
        else:
            type = Type.STRING
            self._match(TokenTag.STRING)
        
        ident = Identifier(type, self.look.lexeme)
        env.put(self.look.lexeme, ident)
        self._match(TokenTag.IDENT)
        
        if not force_assign and self.look.tag is TokenTag.SEMICOLON:
            self._match(TokenTag.SEMICOLON)
            return Declaration(ident)
        else:
            self._match(TokenTag.ASSIGN)
            node = Assign(ident, self._expr())
            self._match(TokenTag.SEMICOLON)
            return node
    
    def _inc(self, ident):
        pass
    
    def _check_ident(self):
        symb = self.look.lexeme
        
        self._match(TokenTag.IDENT)
        ident = self.env.lookup(symb)
        
        if ident is None:
            raise UndeclaredIdentError(symb, self.look.lineno)
        
        return ident
    
    def _match(self, tag):
        if self.look.tag is not tag:
            raise SyntaxError(self.look.tag, self.look.lineno)
        self._move()
    
    def _move(self):
        self.look = lexer.next_token()
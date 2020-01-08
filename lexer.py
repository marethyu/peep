from err import LexError
from token import TokenTag, Token

# global variable
lineno = 1

class Lexer(object):
    def __init__(self, file):
        self.prgm = file.read()
        self.prgm_len = len(self.prgm)
        self.idx = 0
        self.current = prgm[self.idx]
        self.prev_tag = None # for detection of unary operators
        self.dct = {}
        self._init_dict()
    
    def next_token(self):
        if self.current is None:
            return Token(TokenTag.EOF, None, lineno)
        
        if self.current.isspace():
            self._eat_whitespace()
            return self.next_token()
        
        if self.current == '/':
            peek = self._peek()
            
            if peek is not None and peek == '/':
                self._eat_comment()
                return self.next_token()
        
        if self.current.isdigit():
            return self._make_num_tok()
        
        if self.current.isalpha():
            return self._make_word_tok()
        
        if self.current == '(':
            return self._make_token(TokenTag.LPAREN, '(')
        
        if self.current == ')':
            return self._make_token(TokenTag.RPAREN, ')')
        
        if self.current == '{':
            return self._make_token(TokenTag.LBRACK, '{')
        
        if self.current == '}':
            return self._make_token(TokenTag.RBRACK, '}')
        
        if self.current == ';':
            return self._make_token(TokenTag.SEMICOLON, ';')
        
        if self.current == '=':
            self._next_ch()
            
            if self.current is not None and self.current == '=':
                return self._make_token(TokenTag.REL_OP, '==')
            
            self.prev_tag = TokenTag.ASSIGN
            return Token(TokenTag.ASSIGN, '=', lineno)
        
        if self.current in ['+', '-', '*', '/', '%']:
            op = self.current
            peek = self._peek()
            
            if (peek is not None and
                op in ['+', '-'] and
                (peek == '(' or peek.isalnum()) and
                self.prev_tag in [None, TokenTag.ASSIGN, TokenTag.LPAREN, TokenTag.COMMA, TokenTag.REL_OP, TokenTag.ADD_OP, TokenTag.OP]):
                return self._make_token(TokenTag.UNARY_OP, op)
            
            if (peek is not None and
                op in ['+', '-'] and
                peek == '='):
                return self._make_token(TokenTag.PLUS_EQ if op is '+' else TokenTag.MINUS_EQ, op + '=')
            
            if op in ['+', '-']:
                return self._make_token(TokenTag.ADD_OP, op)
            
            return self._make_token(TokenTag.OP, op)
        
        if self.current == '!':
            self._next_ch()
            
            if self.current is not None and self.current == '=':
                return self._make_token(TokenTag.REL_OP, '!=')
            
            self.prev_tag = TokenTag.UNARY_OP
            return Token(TokenTag.UNARY_OP, '!', lineno)
        
        if self.current == '&':
            peek = self._peek()
            
            if peek is not None and peek == '&':
                self._next_ch() # eat '&'
                return self._make_token(TokenTag.OP, '&&')
        
        if self.current == '|':
            peek = self._peek()
            
            if peek is not None and peek == '|':
                self._next_ch() # eat '|'
                return self._make_token(TokenTag.ADD_OP, '||')
        
        if self.current == '<':
            self._next_ch()
            
            if self.current is not None and self.current == '=':
                return self._make_token(TokenTag.REL_OP, '<=')
            
            self.prev_tag = TokenTag.REL_OP
            return Token(TokenTag.REL_OP, '<', lineno)
        
        if self.current == '>':
            self._next_ch()
            
            if self.current is not None and self.current == '=':
                return self._make_token(TokenTag.REL_OP, '>=')
            
            self.prev_tag = TokenTag.REL_OP
            return Token(TokenTag.REL_OP, '>', lineno)
        
        if self.current == '"':
            str = ""
            
            # consume '"'
            self._next_ch()
            
            while self.current is not None and self.current is not '"':
                str += self.current
                self._next_ch()
            
            return self._make_token(TokenTag.STR_LITERAL, str)
        
        raise LexError("Unknown token {}".format(self.current), lineno)
    
    def _make_token(self, tag, lexeme):
        self._next_ch()
        self.prev_tag = tag
        return Token(tag, lexeme, lineno)
    
    def _make_word_tok(self):
        word = ""
        
        while self.current is not None and self.current.isalnum():
            word += self.current
            self._next_ch()
        
        tag = self.dct.get(word)
        
        if tag is not None:
            self.prev_tag = tag
            return Token(tag, word, lineno)
        
        self.prev_tag = TokenTag.IDENT
        return Token(TokenTag.IDENT, word, lineno)
    
    def _make_num_tok(self):
        num = ""
        
        while self.current is not None and self.current.isdigit():
            num += self.current
            self._next_ch()
        
        if self.current is not None and self.current == '.':
            num += self.current
            self._next_ch()
            
            while self.current is not None and self.current.isdigit():
                num += self.current
                self._next_ch()
            
            self.prev_tag = TokenTag.RL_CONST
            return Token(TokenTag.RL_CONST, num, lineno)
        
        self.prev_tag = TokenTag.INT_CONST
        return Token(TokenTag.INT_CONST, num, lineno)
    
    def _eat_comment(self):
        # consume "//"
        self._next_ch()
        self._next_ch()
        
        while self.current is not '\n':
            self._next_ch()
        # consume '\n'
        self._next_ch()
    
    def _eat_whitespace(self):
        while self.current is not None and self.current.isspace():
            self._next_ch()
    
    def _peek(self):
        next_idx = self.idx + 1
        return None if next_idx >= self.prgm_len else self.prgm[next_idx]
    
    def _next_ch(self):
        if self.current == '\n':
            lineno += 1
        self.idx += 1
        self.current = None if self.idx >= self.prgm_len else self.prgm[self.idx]
    
    def _init_dict(self):
        self.dct['int'] = TokenTag.INT
        self.dct['float'] = TokenTag.FLOAT
        self.dct['bool'] = TokenTag.BOOL
        self.dct['string'] = TokenTag.STRING
        self.dct['if'] = TokenTag.IF
        self.dct['else'] = TokenTag.ELSE
        self.dct['while'] = TokenTag.WHILE
        self.dct['for'] = TokenTag.FOR
        self.dct['do'] = TokenTag.DO
        self.dct['break'] = TokenTag.BREAK
        self.dct['continue'] = TokenTag.CONTINUE
        self.dct['print'] = TokenTag.PRINT
        self.dct["scan"] = TokenTag.SCAN
        self.dct['true'] = TokenTag.TRUE
        self.dct['false'] = TokenTag.FALSE
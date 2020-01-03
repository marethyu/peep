from token import TokenTag, Token

class Lexer(object):
    def __init__(self, prgm):
        self.prgm = prgm
        self.prgm_len = len(self.prgm)
        self.lineno = 1
        self.idx = 0
        self.current = prgm[self.idx]
        self.prev_tag = None # for detection of unary operators
        self.dct = {}
        self._init_dict()
    
    def next_token(self):
        if self.current is None:
            return Token(TokenTag.EOF, None, self.lineno)
        
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
        
        if self.current == '[':
            return self._make_token(TokenTag.LSQ_BRCKT, '[')
        
        if self.current == ']':
            return self._make_token(TokenTag.RSQ_BRCKT, ']')
        
        if self.current == '{':
            return self._make_token(TokenTag.LCURLY_BRACE, '{')
        
        if self.current == '}':
            return self._make_token(TokenTag.RCURLY_BRACE, '}')
        
        if self.current == ';':
            return self._make_token(TokenTag.SEMICOLON, ';')
        
        if self.current == ',':
            return self._make_token(TokenTag.COMMA, ',')
        
        if self.current == '.':
            return self._make_token(TokenTag.DOT, '.')
        
        if self.current == '=':
            self._next_ch()
            
            if self.current is not None and self.current == '=':
                return self._make_token(TokenTag.EQUAL, '==')
            
            self.prev_tag = TokenTag.ASSIGN
            return Token(TokenTag.ASSIGN, '=', self.lineno)
        
        if self.current in ['+', '-', '*', '/', '%']:
            op = self.current
            peek = self._peek()
            
            if (peek is not None and
                op in ['+', '-'] and
                (peek == '(' or peek.isalnum()) and
                self.prev_tag in [None, TokenTag.ASSIGN, TokenTag.BIN_OP, TokenTag.LPAREN, TokenTag.COMMA, TokenTag.EQUAL, TokenTag.NOT_EQU, TokenTag.LESS, TokenTag.GREATER, TokenTag.LESS_EQ, TokenTag.GREATER_EQ]):
                return self._make_token(TokenTag.UNARY_OP, op)
            
            if (peek is not None and
                op in ['+', '-'] and
                peek == '='):
                return self._make_token(TokenTag.PLUS_EQ if op is '+' else TokenTag.MINUS_EQ, op + '=')
            
            return self._make_token(TokenTag.BIN_OP, op)
        
        if self.current == '!':
            self._next_ch()
            
            if self.current is not None and self.current == '=':
                return self._make_token(TokenTag.NOT_EQU, '!=')
            
            self.prev_tag = TokenTag.NOT
            return Token(TokenTag.NOT, '!', self.lineno)
        
        if self.current == '&':
            peek = self._peek()
            
            if peek is not None and peek == '&':
                self._next_ch() # eat '&'
                return self._make_token(TokenTag.AND, '&&')
        
        if self.current == '|':
            peek = self._peek()
            
            if peek is not None and peek == '|':
                self._next_ch() # eat '|'
                return self._make_token(TokenTag.OR, '||')
        
        if self.current == '<':
            self._next_ch()
            
            if self.current is not None and self.current == '=':
                return self._make_token(TokenTag.LESS_EQ, '<=')
            
            self.prev_tag = TokenTag.LESS
            return Token(TokenTag.LESS, '<', self.lineno)
        
        if self.current == '>':
            self._next_ch()
            
            if self.current is not None and self.current == '=':
                return self._make_token(TokenTag.GREATER_EQ, '>=')
            
            self.prev_tag = TokenTag.GREATER
            return Token(TokenTag.GREATER, '>', self.lineno)
        
        if self.current == '"':
            str = ""
            
            # consume '"'
            self._next_ch()
            
            while self.current is not None and self.current is not '"':
                str += self.current
                self._next_ch()
            
            return self._make_token(TokenTag.STR_LITERAL, str)
        
        return self._make_token(TokenTag.UNK, self.current)
    
    def _make_token(self, tag, value):
        self._next_ch()
        self.prev_tag = tag
        return Token(tag, value, self.lineno)
    
    def _make_word_tok(self):
        word = ""
        
        while self.current is not None and self.current.isalnum():
            word += self.current
            self._next_ch()
        
        tag = self.dct.get(word)
        
        if tag is not None:
            self.prev_tag = tag
            return Token(tag, word, self.lineno)
        
        self.prev_tag = TokenTag.IDENT
        return Token(TokenTag.IDENT, word, self.lineno)
    
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
            
            self.prev_tag = TokenTag.FLT_CONST
            return Token(TokenTag.FLT_CONST, num, self.lineno)
        
        self.prev_tag = TokenTag.INT_CONST
        return Token(TokenTag.INT_CONST, num, self.lineno)
    
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
            self.lineno += 1
        self.idx += 1
        self.current = None if self.idx >= self.prgm_len else self.prgm[self.idx]
    
    def _init_dict(self):
        self.dct['int'] = TokenTag.INT
        self.dct['float'] = TokenTag.FLOAT
        self.dct['bool'] = TokenTag.BOOL
        self.dct['string'] = TokenTag.STRING
        self.dct['void'] = TokenTag.VOID
        self.dct['if'] = TokenTag.IF
        self.dct['else'] = TokenTag.ELSE
        self.dct['while'] = TokenTag.WHILE
        self.dct['for'] = TokenTag.FOR
        self.dct['do'] = TokenTag.DO
        self.dct['break'] = TokenTag.BREAK
        self.dct['continue'] = TokenTag.CONTINUE
        self.dct['return'] = TokenTag.RETURN
        self.dct['use'] = TokenTag.USE
        self.dct['object'] = TokenTag.OBJECT
        self.dct['scan'] = TokenTag.SCAN
        self.dct['print'] = TokenTag.PRINT
        self.dct['assert'] = TokenTag.ASSERT
        self.dct['exit'] = TokenTag.EXIT
        self.dct['true'] = TokenTag.TRUE
        self.dct['false'] = TokenTag.FALSE
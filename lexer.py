from token import TokenType, Token

class Lexer(object):
    def __init__(self, prgm):
        self.prgm = prgm
        self.prgm_len = len(self.prgm)
        self.lineno = 1
        self.idx = 0
        self.current = prgm[self.idx]
        self.prev_type = None # for detection of unary operators
        self.dct = {}
        self._init_dict()
    
    def next_token(self):
        if self.current is None:
            return Token(TokenType.EOF, None, self.lineno)
        
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
            return self._make_token(TokenType.LPAREN, '(')
        
        if self.current == ')':
            return self._make_token(TokenType.RPAREN, ')')
        
        if self.current == '[':
            return self._make_token(TokenType.LSQ_BRCKT, '[')
        
        if self.current == ']':
            return self._make_token(TokenType.RSQ_BRCKT, ']')
        
        if self.current == '{':
            return self._make_token(TokenType.LCURLY_BRACE, '{')
        
        if self.current == '}':
            return self._make_token(TokenType.RCURLY_BRACE, '}')
        
        if self.current == ';':
            return self._make_token(TokenType.SEMICOLON, ';')
        
        if self.current == ',':
            return self._make_token(TokenType.COMMA, ',')
        
        if self.current == '=':
            self._next_ch()
            
            if self.current is not None and self.current == '=':
                return self._make_token(TokenType.EQUAL, '==')
            
            self.prev_type = TokenType.ASSIGN
            return Token(TokenType.ASSIGN, '=', self.lineno)
        
        if self.current in ['+', '-', '*', '/', '%']:
            op = self.current
            peek = self._peek()
            
            if (peek is not None and
                op in ['+', '-'] and
                (peek == '(' or peek.isalnum()) and
                self.prev_type in [None, TokenType.BIN_OP, TokenType.LPAREN, TokenType.COMMA, TokenType.EQUAL, TokenType.NOT_EQU, TokenType.LESS, TokenType.GREATER, TokenType.LESS_EQ, TokenType.GREATER_EQ]):
                return self._make_token(TokenType.UNARY_OP, op)
            
            if (peek is not None and
                op in ['+', '-'] and
                peek == '='):
                return self._make_token(TokenType.PLUS_EQ if op is '+' else TokenType.MINUS_EQ, op + '=')
            
            return self._make_token(TokenType.BIN_OP, op)
        
        if self.current == '!':
            self._next_ch()
            
            if self.current is not None and self.current == '=':
                return self._make_token(TokenType.NOT_EQU, '!=')
            
            self.prev_type = TokenType.NOT
            return Token(TokenType.NOT, '!', self.lineno)
        
        if self.current == '&':
            peek = self._peek()
            
            if peek is not None and peek == '&':
                self._next_ch() # eat '&'
                return self._make_token(TokenType.AND, '&&')
        
        if self.current == '|':
            peek = self._peek()
            
            if peek is not None and peek == '|':
                self._next_ch() # eat '|'
                return self._make_token(TokenType.OR, '||')
        
        if self.current == '<':
            self._next_ch()
            
            if self.current is not None and self.current == '=':
                return self._make_token(TokenType.LESS_EQ, '<=')
            
            self.prev_type = TokenType.LESS
            return Token(TokenType.LESS, '<', self.lineno)
        
        if self.current == '>':
            self._next_ch()
            
            if self.current is not None and self.current == '=':
                return self._make_token(TokenType.GREATER_EQ, '>=')
            
            self.prev_type = TokenType.GREATER
            return Token(TokenType.GREATER, '>', self.lineno)
        
        # TODO: Handle escape characters
        if self.current == '"':
            str = ""
            
            # consume '"'
            self._next_ch()
            
            while self.current is not None and self.current is not '"':
                str += self.current
                self._next_ch()
            
            return self._make_token(TokenType.STRING_CONST, str)
        
        return Token(TokenType.UNK, self.current, self.lineno)
    
    def _make_token(type, value):
        self._next_ch()
        self.prev_type = type
        return Token(type, value, self.lineno)
    
    def _make_word_tok(self):
        word = ""
        
        while self.current is not None and self.current.isalnum():
            word += self.current
            self._next_ch()
        
        type = self.dct.get(word)
        
        if type is not None:
            self.prev_type = type
            return Token(type, word, self.lineno)
        
        self.prev_type = TokenType.IDENT
        return Token(TokenType.IDENT, word, self.lineno)
    
    def _make_num_tok(self):
        num = ""
        
        while self.current is not None and self.current.isdigit():
            num += self.current
            self._next_ch()
        
        if self.current is not None and self.current == '.':
            # consume a decimal point
            self._next_ch()
            
            while self.current is not None and self.current.isdigit():
                num += self.current
                self._next_ch()
            
            self.prev_type = TokenType.FLT_CONST
            return Token(TokenType.FLT_CONST, num, self.lineno)
        
        self.prev_type = INT_CONST
        return Token(TokenType.INT_CONST, num, self.lineno)
    
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
    
    def _init_dct(self):
        self.dct['int'] = TokenType.INT
        self.dct['float'] = TokenType.FLOAT
        self.dct['bool'] = TokenType.BOOL
        self.dct['string'] = TokenType.STRING
        self.dct['void'] = TokenType.VOID
        self.dct['if'] = TokenType.IF
        self.dct['else'] = TokenType.ELSE
        self.dct['while'] = TokenType.WHILE
        self.dct['for'] = TokenType.FOR
        self.dct['do'] = TokenType.DO
        self.dct['break'] = TokenType.BREAK
        self.dct['continue'] = TokenType.CONTINUE
        self.dct['return'] = TokenType.RETURN
        self.dct['use'] = TokenType.USE
        self.dct['object'] = TokenType.OBJECT
        self.dct['scan'] = TokenType.SCAN
        self.dct['print'] = TokenType.PRINT
        self.dct['assert'] = TokenType.ASSERT
        self.dct['exec'] = TokenType.EXEC
        self.dct['true'] = TokenType.TRUE
        self.dct['false'] = TokenType.FALSE
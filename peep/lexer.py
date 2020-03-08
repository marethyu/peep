from err import LexError, raise_error
from token import TokenTag, Token

# global variable
lineno = 1


class Lexer:
    def __init__(self, file):
        self.prgm = file.read()
        self.prgm_len = len(self.prgm)

        if self.prgm_len == 0:
            raise_error(LexError("The program is empty!", 0))

        self.idx = 0
        self.current = self.prgm[self.idx]
        self.prev_tag = None  # for detection of unary operators
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

            if peek == '/':
                self._eat_comment()
                return self.next_token()
            elif peek == '*':
                self._eat_multiline_comment()
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

            if self.current == '=':
                return self._make_token(TokenTag.EQ_OP, '==')

            self.prev_tag = TokenTag.ASSIGN
            return Token(TokenTag.ASSIGN, '=', lineno)

        if self.current in ('+', '-', '*', '/', '%'):
            op = self.current
            peek = self._peek()

            if op in ("+", "-"):
                if ((peek == '(' or peek.isalnum()) and
                        self.prev_tag in [None, TokenTag.ASSIGN, TokenTag.LPAREN, TokenTag.REL_OP, TokenTag.ADD_OP,
                                          TokenTag.MUL_OP]):
                    return self._make_token(TokenTag.UNARY_OP, op)

                if peek == "=":
                    return self._make_token(TokenTag.PLUS_EQ if op == '+' else TokenTag.MINUS_EQ, op + '=', True)

                return self._make_token(TokenTag.ADD_OP, op)

            if peek == "=":
                if op == '*':
                    return self._make_token(TokenTag.MUL_EQ, '*=', True)
                elif op == '/':
                    return self._make_token(TokenTag.DIV_EQ, '/=', True)
                else:
                    return self._make_token(TokenTag.MOD_EQ, '%=', True)

            return self._make_token(TokenTag.MUL_OP, op)

        if self.current == '!':
            self._next_ch()

            if self.current == '=':
                return self._make_token(TokenTag.EQ_OP, '!=')

            self.prev_tag = TokenTag.UNARY_OP
            return Token(TokenTag.UNARY_OP, '!', lineno)

        if self.current == '&':
            peek = self._peek()

            if peek == '&':
                self._next_ch()  # eat '&'
                return self._make_token(TokenTag.AND, '&&')

        if self.current == '|':
            peek = self._peek()

            if peek == '|':
                self._next_ch()  # eat '|'
                return self._make_token(TokenTag.OR, '||')

        if self.current == '<':
            self._next_ch()

            if self.current == '=':
                return self._make_token(TokenTag.REL_OP, '<=')

            self.prev_tag = TokenTag.REL_OP
            return Token(TokenTag.REL_OP, '<', lineno)

        if self.current == '>':
            self._next_ch()

            if self.current == '=':
                return self._make_token(TokenTag.REL_OP, '>=')

            self.prev_tag = TokenTag.REL_OP
            return Token(TokenTag.REL_OP, '>', lineno)

        if self.current == '"':
            escape_characters = {'n': '\n', 't': '\t', 'v': '\v', 'b': '\b', 'f': '\f', 'a': '\a', 'r': '\r', '\\': '\\',
                                 '"': '\"', '\'': '\''}

            string_literal = ""
            # consume '"'
            self._next_ch()
            prev = self.current
            is_escaped = prev == '\\'

            while self.current is not None and (self.current != '"' or is_escaped):
                self._next_ch()
                # handle escape sequences
                if is_escaped:
                    string_literal += escape_characters.get(self.current, '\\' + self.current)
                    # current is the escaped character, advance by one
                    self._next_ch()
                else:
                    string_literal += prev
                    
                is_escaped = self.current == "\\"
                prev = self.current

            return self._make_token(TokenTag.STR_LITERAL, string_literal)

        raise_error(LexError("Unknown token {}".format(self.current), lineno))

    def _make_token(self, tag, lexeme, skip_twice=False):
        self._next_ch()
        if skip_twice:
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

        if self.current == '.':
            num += self.current
            self._next_ch()

            while self.current is not None and self.current.isdigit():
                num += self.current
                self._next_ch()

            self.prev_tag = TokenTag.RL_CONST
            return Token(TokenTag.RL_CONST, num, lineno)

        self.prev_tag = TokenTag.INT_CONST
        return Token(TokenTag.INT_CONST, num, lineno)

    def _eat_multiline_comment(self):
        # consume "/*"
        self._next_ch()
        self._next_ch()

        while True:
            while self.current is not None and self.current != '*':
                self._next_ch()

            if self.current is None:
                raise_error(LexError("A multi-line comment doesn't end with '*/'!", lineno))
            elif self._peek() == '/':
                # consume closing "*/"
                self._next_ch()
                self._next_ch()
                break
            else:  # self._peek() != '/' (oops...)
                self._next_ch()
                # then continue the loop...

    def _eat_comment(self):
        # consume "//"
        self._next_ch()
        self._next_ch()

        while self.current != '\n':
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
            global lineno
            lineno += 1
        self.idx += 1
        self.current = None if self.idx >= self.prgm_len else self.prgm[self.idx]

    def _init_dict(self):
        self.dct.update({
            'int': TokenTag.INT,
            'float': TokenTag.FLOAT,
            'bool': TokenTag.BOOL,
            'string': TokenTag.STRING,
            'if': TokenTag.IF,
            'else': TokenTag.ELSE,
            'while': TokenTag.WHILE,
            'for': TokenTag.FOR,
            'break': TokenTag.BREAK,
            'continue': TokenTag.CONTINUE,
            'print': TokenTag.PRINT,
            "scan": TokenTag.SCAN,
            'true': TokenTag.TRUE,
            'false': TokenTag.FALSE,
        })

# global variable
errlist = []

class PeepError(Exception):
    pass

class ParseError(PeepError):
    def __init__(self, message):
        self.message = message

class UndeclaredIdentError(ParseError):
    def __init__(self, token, lineno):
        super.__init__("ERROR: @line {}: Identifier {} is undeclared in this scope!".format(lineno, token.value))

class SyntaxError(ParseError):
    def __init__(self, unexpected_tag, lineno):
        super.__init__("ERROR: @line {}: {} unexpected!".format(lineno, unexpected_tag))
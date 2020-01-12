class PeepError(Exception):
    def __init__(self, lineno, message):
        self.message = "ERROR @line {}".format(lineno) + ": " + message

class LexError(PeepError):
    def __init__(self, message, lineno):
        super().__init__(lineno, message)

class ParseError(PeepError):
    def __init__(self, message, lineno):
        super().__init__(lineno, message)

class UndeclaredIdentError(ParseError):
    def __init__(self, id_name, lineno):
        super().__init__("Identifier {} is undeclared in this scope!".format(id_name), lineno)

class SyntaxError(ParseError):
    def __init__(self, unexpected_tag, lineno):
        super().__init__("{} unexpected!".format(unexpected_tag), lineno)
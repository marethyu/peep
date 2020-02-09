from sys import exit

class PeepError:
    def __init__(self, base_error_name, lineno, message):
        self.message = base_error_name + " @line {}".format(lineno) + ": " + message
    
    def __str__(self):
        return self.message

class LexError(PeepError):
    def __init__(self, message, lineno):
        super().__init__(self.__class__.__name__, lineno, message)

class SemanticError(PeepError):
    def __init__(self, message, lineno, base_error_name):
        super().__init__(base_error_name, lineno, message)

class DuplicateIdentError(SemanticError):
    def __init__(self, id_name, lineno):
        super().__init__("Identifier {} is already declared in this scope!".format(id_name), lineno, self.__class__.__name__)

class UndeclaredIdentError(SemanticError):
    def __init__(self, id_name, lineno):
        super().__init__("Identifier {} is undeclared in this scope!".format(id_name), lineno, self.__class__.__name__)

class SyntaxError(PeepError):
    def __init__(self, message, lineno):
        super().__init__(self.__class__.__name__, lineno, message)

class TypeError(PeepError):
    def __init__(self, lineno, msg):
        super().__init__(self.__class__.__name__, lineno, msg)

class RuntimeError(PeepError):
    def __init__(self, msg, lineno, base_error_name):
        super().__init__(base_error_name, lineno, msg)

class DivisionByZeroError(RuntimeError):
    def __init__(self, lineno):
        super().__init__("Division by zero will produce an undefined result!", lineno, self.__class__.__name__)

class InputCastingError(RuntimeError):
    def __init__(self, msg, lineno):
        super().__init__(msg, lineno, self.__class__.__name__)

def raise_error(error):
    print(error)
    exit(0)

def raise_runtime_error(error, call_stk):
    print(error)
    
    for i in range(len(call_stk.records) - 1, -1, -1):
        ar = call_stk.records[i]
        print('\tat ' + ar.filename + '.' + ar.current_function + '.' + str(ar.last_lineno))
    
    exit(0)

class Scope(object):
    def __init__(self, level=0, parent=None):
        self.level = level
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
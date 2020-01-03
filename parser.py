class Scope(object):
    def __init__(self, level=0, parent=None):
        self.level = level
        self.parent = parent
        self.symtab = {}
    
    def put(self, ident_name, ident):
        self.symtab[ident_name] = ident
    
    def lookup(self, ident_name):
        scope = self
        
        while scope is not None:
            entry = scope.symtab.get(ident_name)
            
            if entry is not None:
                return entry
            
            scope = scope.parent
        
        return None
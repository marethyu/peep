class Scope:
    def __init__(self, parent):
        self.parent = parent
        self.dct = {}
    
    def lookup_local(self, name):
        return self.dct.get(name)
    
    def __getitem__(self, name):
        scope = self
        
        while scope is not None:
            entry = scope.dct.get(name)
            
            if entry is not None:
                return entry
            
            scope = scope.parent
        
        return None
    
    def __setitem__(self, name, ident):
        self.dct[name] = ident

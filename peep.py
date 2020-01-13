from lexer import Lexer
from parse import Parser
from astprinter import ASTPrinter

def help():
    help_msg = ("Usage: peep [filename].peep")
    
    print(help_msg)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 1:
        help()
    else:
        try:
            file = open(sys.argv[1])
        except FileNotFoundError:
            print("That file does not exist!")
            sys.exit(1)
        
        """
        lex = Lexer(file)
        
        while True:
            token = lex.next_token()
            
            from token import TokenTag
            if token.tag is TokenTag.EOF:
                break
            
            print(token)
        """
        
        ast_root = Parser(Lexer(file)).parse()
        printer = ASTPrinter()
        ast_root.accept(printer)
        
        file.close()
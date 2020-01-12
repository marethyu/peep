from lexer import Lexer
from parse import Parser

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
            sys.exit(0)
        
        """
        lex = Lexer(file)
        
        while True:
            token = lex.next_token()
            
            from token import TokenTag
            if token.tag is TokenTag.EOF:
                break
            
            print(token)
        """
        
        parse = Parser(Lexer(file))
        parse.parse()
        
        file.close()
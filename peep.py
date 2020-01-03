from token import TokenTag
from lexer import Lexer

if __name__ == "__main__":
    with open("finaltest.peep") as file:
        lex = Lexer(file.read())
        
        while True:
            token = lex.next_token()
            
            if token.tag == TokenTag.EOF:
                break;
            
            print(token)
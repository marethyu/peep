import argparse
import sys

from peep import Lexer
from peep import Parser
from peep import ASTPrinter
from peep import Interpreter

peep_ver = "1.1.2"

def p_ast(lexer):
    root = Parser(lexer).parse()
    astprinter = ASTPrinter(root)
    astprinter.print_ast()
    from peep.util import filename
    assert filename is not None
    astprinter.write(filename)

def i(lexer):
    root = Parser(lexer).parse()
    interpreter = Interpreter(root)
    interpreter.interpret()

def version():
    print('v' + peep_ver)

def main():
    parser = argparse.ArgumentParser()
    
    group = parser.add_mutually_exclusive_group(required=True)
    
    # only one of the arguments below can be used
    group.add_argument("-p", "--print_ast", help="Print AST (Abstract Syntax Tree) for the program in a seperate .xml file", action="store_true")
    group.add_argument("-i", help="Execute the program from the source file", action="store_true")
    
    parser.add_argument("file", type=str, help="file with a .peep extension")
    parser.add_argument("--version", help="Show current version of Peep", action="store_true")
    
    args = parser.parse_args()
    
    if args.version:
        version()
    
    try:
        lexer = Lexer(args.file)
    except LexError as le:
        return
    
    if args.print_ast:
        p_ast(lexer)
    elif args.i:
        i(lexer)

if __name__ == '__main__':
    main()

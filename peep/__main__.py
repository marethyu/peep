import argparse
import sys

from lexer import Lexer
from parse import Parser
from astprinter import ASTPrinter
from intrp import Interpreter

peep_ver = "1.1.2"

def p_ast(file):
    root = Parser(Lexer(file)).parse()
    astprinter = ASTPrinter(root)
    astprinter.print_ast()

def i(file):
    root = Parser(Lexer(file)).parse()
    interpreter = Interpreter(root)
    interpreter.interpret()

def version():
    print('v' + peep_ver)

def main():
    parser = argparse.ArgumentParser()
    
    group = parser.add_mutually_exclusive_group(required=True)
    
    # only one of the arguments below can be used
    group.add_argument("-p", "--print-ast", help="Print AST (Abstract Syntax Tree) for the program in a seperate .xml file", action="store_true")
    group.add_argument("-i", help="Execute the program from the source file", action="store_true")
    
    parser.add_argument("file", type=str, help="file with a .peep extension")
    parser.add_argument("--version", help="Show current version of Peep", action="store_true")
    
    args = parser.parse_args()
    
    from util import get_file
    fh = get_file(args.file)
    
    if args.version:
        version()
    
    if args.p_ast:
        p_ast(fh)
        fh.close()
    elif args.i:
        i(fh)
        fh.close()

if __name__ == '__main__':
    main()

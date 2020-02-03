from lexer import Lexer
from parse import Parser
from astprinter import ASTPrinter
from intrp import Interpreter

all_options = {'-p-ast'      : 'Print AST (Abstract Syntax Tree) for the program in a seperate .xml file',
#              '-c'          : 'Generate an equivalent x86-64 assembly program for the given source code',
               '-i'          : 'Execute the program',
#              '-pbt'        : 'Run pbt (Peep Bug Tracker)',
               '--help'      : 'Display this information',
#              '--pbt-help'  : 'Show help information for pbt command option',
               '--version'   : 'Show current version of Peep'}

peep_ver = 1.0

def p_ast(file):
    root = Parser(Lexer(file)).parse()
    astprinter = ASTPrinter(root)
    astprinter.print_ast()

def i(file):
    root = Parser(Lexer(file)).parse()
    interpreter = Interpreter(root)
    interpreter.interpret()

def help():
    print("Usage: python peep.py [options] insert_file_name_here.peep\nOptions:")
    
    for k, v in all_options.items():
        print(' ' + k + ' ' * (16 - len(k)) + v)
    
    print("\nNote: You can't use options '-p-ast' and '-i' at the same time")

def version():
    print('v' + str(peep_ver))

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 1:
        help()
    else:
        options = sys.argv[1:]
        file = None
        
        for option in options:
            if option not in all_options.keys():
                if option.endswith('.peep'):
                    file = option
                    break
                else:
                    print('option {} unknown'.format(option))
                    sys.exit(1)
        
        for option in options:
            if option == '--help':
                help()
                sys.exit(0)
            elif option == '--version':
                version()
                sys.exit(0)
        
        if file is not None:
            for option in options:
                if option == '-p-ast':
                    from util import get_file
                    f = get_file(file)
                    p_ast(f)
                    f.close()
                    sys.exit(0)
                elif option == '-i':
                    from util import get_file
                    f = get_file(file)
                    i(f)
                    f.close()
                    sys.exit(0)
        
        help()
# originally this code was in peep.py but it was moved to this seperate file
# why? see https://stackoverflow.com/questions/60034869/python-global-variable-is-none-in-another-module

import sys

filename = None

def get_file(file):
    fh = None
    
    try:
        global filename
        filename = file[:-5]
        fh = open(file)
    except FileNotFoundError:
        print("That file does not exist!")
        sys.exit(1)
    finally:
        return fh
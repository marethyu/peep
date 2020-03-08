import os
import sys

from os.path import abspath, dirname, isfile, join, realpath
from unittest.mock import patch

def run(file):
    def exit(x):
        raise
    
    with patch("sys.argv", ["", "-i", file]), patch("sys.exit", exit):
        try:
            from peep.__main__ import main
            main()
        except:
            return

if __name__ == "__main__":
    sys.path.append(dirname(dirname(abspath(__file__))))
    current_dir = dirname(realpath(__file__))
    
    for v, dir in enumerate(os.listdir(current_dir)):
        child_dir = join(current_dir, dir)
        
        if not isfile(child_dir):
            print("VERSION {} TEST".format(v + 1))
            
            for no, file in enumerate(os.listdir(child_dir)):
                print("TEST {} (file={})".format(no + 1, file))
                run(join(child_dir, file))
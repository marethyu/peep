import os
import sys

from os.path import abspath, dirname, isfile, join
from unittest.mock import patch

def mock_exit():
    pass

def run(file):
    with patch(sys, "argv", ["", "-i", file]), patch(sys, "exit", mock_exit):
        from peep.peep import main
        main()

if __name__ == "__main__":
    sys.path.append(dirname(dirname(abspath(__file__))))
    current_dir = os.path.dirname(os.path.realpath(__file__))
    
    # use itertools
    
    v = 1
    
    for dir in os.listdir(current_dir):
        child_dir = join(current_dir, dir)
        
        if not isfile(child_dir):
            print("VERSION {} TEST".format(v))
            v += 1
            no = 1
            
            for file in os.listdir(child_dir):
                print("TEST {} (file={})".format(no, file))
                no += 1
                run(join(child_dir, file))
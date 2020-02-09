import os
import sys

from os.path import abspath, dirname, isfile, join
from unittest.mock import patch

def run(file):
    from peep.peep import main
    with patch.object(sys, 'argv', ["", "-i", file]):
        main()

if __name__ == "__main__":
    sys.path.append(dirname(dirname(abspath(__file__))))
    current_dir = os.path.dirname(os.path.realpath(__file__))
    
    v = 1
    
    for dir in os.listdir(current_dir):
        child_dir = join(current_dir, dir)
        
        if not isfile(child_dir):
            print("VERSION {} TEST".format(v))
            v += 1
            no = 1
            
            for file in os.listdir(child_dir):
                if "err" not in file:
                    print("TEST {} (file={})".format(no, file))
                    no += 1
                    run(join(child_dir, file))
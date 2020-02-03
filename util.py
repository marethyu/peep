# originally this code was in peep.py but moved to this seperate file
# why? see https://stackoverflow.com/questions/60034869/python-global-variable-is-none-in-another-module

dir_prefix = None
filename = None

def get_file(file):
    try:
        global filename
        filename = file[:-5]
        if filename.find('/') != -1:
            global dir_prefix
            dir_prefix = filename[:filename.rfind('/') + 1]
            filename = filename[filename.rfind('/') + 1:]
        f = open(file)
    except FileNotFoundError:
        print("That file does not exist!")
        sys.exit(1)
    finally:
        return f
import sys
from parser import *

def main():
    parser = Parser()
    parser.parse_file(sys.argv[1])
    parser.print_lexemes()

if __name__ == "__main__":
    main()

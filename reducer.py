# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
from parser import *

def main():
    if len(sys.argv) == 1:              # interavtive mode
        interactiveMode()
    elif len(sys.argv) == 2:            # read expression from file
        parser = Parser()
        parser.parse_file(sys.argv[1])
        parser.print_lexemes()
    else:                               # error
        print('usage: reducer.py')
        print('       reducer.py source_file')

def interactiveMode():
    parser = Parser()
    while True:
        new_line = raw_input('>> ')
        if new_line == 'exit':
            break
        elif new_line == 'help':
            print('-- enter \'exit\' to quit')
            print('-- lamda symbols can be either λ or \\')
        else:
            parser.parse_string(new_line)
            parser.print_lexemes()
        parser.clear_lexemes()

if __name__ == '__main__':
    main()

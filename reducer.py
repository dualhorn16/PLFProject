# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
from parser import *

def main():
    if len(sys.argv) == 1:              # interavtive mode
        interactiveMode()
    elif len(sys.argv) == 2:            # read expression from file
        parser = Parser()
        parser.parseFile(sys.argv[1])
        parser.printLexemes()
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
            parser.parseString(new_line)
            parser.printLexemes()
        parser.clearLexemes()

if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
from parser import Parser

def main():
    '''
    Main function
    '''
    if len(sys.argv) == 1:              # interavtive mode
        interactive_mode()
    elif len(sys.argv) > 3:             # error
        print('usage: reducer.py')
        print('       reducer.py [source_file]')
        print('       reducer.py [source_file] [output_tex_file]')
    else:
        parser = Parser()               # read expression from file
        parser.parse_file(sys.argv[1])
        parser.print_lexemes()
        parser.create_parse_tree()
        if len(sys.argv) == 3:          # output file
            parser.print_tree(sys.argv[2])

def interactive_mode():
    '''
    Interactive mode
    '''
    parser = Parser()
    while True:
        new_line = raw_input('>> ')
        if new_line == 'exit':
            break
        elif new_line == 'help':
            print('- commands:')
            print('-- \'output [file_name].tex\'    ouput tree representation of last reduction')
            print('-- \'exit\'                      quit')
            print('- lamda symbols can be either λ or \\')
        elif new_line[0:6] == 'output':
            if len(parser.lexemes) == 0:
                print('ERROR: no expression entered yet')
            else:
                parser.print_tree(new_line[7:])
        else:
            parser.clear_lexemes()
            parser.parse_string(new_line)
            parser.print_lexemes()
            parser.create_parse_tree()

if __name__ == '__main__':
    main()

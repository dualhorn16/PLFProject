# -*- coding: utf-8 -*-
#************************************************
#   Lamda Calculus Beta Redux Calculator
#
#   Programming Language Foundations
#
#   Kiel Martyn
#   Dustin Horner
#
#   -Fall 2016
#
#   -Tools main method is located here, handles CLI inputs,
#    creates parser, and reductions called from here.
#***********************************************/
from __future__ import print_function
import sys
from parser import Parser
from trees import *
import codecs

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
        if len(parser.lexemes) == 0:
            exit()
        parser.print_lexemes()
        parser.create_parse_tree()
        # if len(sys.argv) == 3:          # output file
        #     parser.print_tree(sys.argv[2])
        root = parser.return_root()
        if len(sys.argv) == 2:
            reduce(parser, root, None)

        if len(sys.argv) == 3:
            reduce(parser, root, sys.argv[2])


def interactive_mode():
    '''
    Interactive mode
    '''
    root = None
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
            if len(parser.lexemes) == 0:
                continue
            parser.create_parse_tree()
            root = parser.return_root()
            reduce(parser, root, None)

def reduce(parser, root, arg_filename):
    file_print = True
    if arg_filename == None:
        file_print = False
    if file_print:
        filename = str(arg_filename)
    item_number = 1
    tree = Tree()

    #create more complicated example tree until parsing is in
    # root = tree.create_test_tree()

    if file_print:
        tree.print_header(filename, item_number)
        tree.print_tree(filename, root, item_number)

    #[Console print expression HERE]
    flat_tree = u''
    flat_tree = tree.print_flat_tree(root, flat_tree)
    print(flat_tree, end='')

    #loop to perform redux, print each step
    while True:

        item_number += 1
        if tree.beta_redux_present(root, False):
            print(' ~>')
            root = tree.perform_beta_redux(root)
            #[Console print expression HERE]
            flat_tree = u''
            flat_tree = tree.print_flat_tree(root, flat_tree)
            print(flat_tree, end='')
            if file_print:
                tree.print_tree(filename, root, item_number)
        else:
            print('')
            break

    if file_print:
        tree.finish_print_nice(filename)

if __name__ == '__main__':
    main()

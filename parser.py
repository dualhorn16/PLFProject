# -*- coding: utf-8 -*-
from __future__ import print_function
import codecs

class LexemeTypes(object):
    '''
    LexemeTypes acts as enumerator for the five different kinds of lexemes.
    '''
    LAMDA = 1
    PERIOD = 2
    LEFT_PAREN = 3
    RIGHT_PAREN = 4
    IDENTIFIER = 5

class Lexeme(object):
    '''
    Simple object for lexical analyzer.
    '''
    lex_type = 0
    value = 0

    def __init__(self, lex_type, value):
        self.lex_type = lex_type
        self.value = value

    def to_string(self):
        '''
        Returns a string for this lexeme.
        '''
        if self.lex_type == LexemeTypes.LAMDA:
            return 'λ'
        elif self.lex_type == LexemeTypes.PERIOD:
            return '.'
        elif self.lex_type == LexemeTypes.LEFT_PAREN:
            return '('
        elif self.lex_type == LexemeTypes.RIGHT_PAREN:
            return ')'
        else:
            return self.value

class NodeTypes(object):
    '''
    NodeTypes acts as enumerator for the 3 different kinds of nodes.
    '''
    ABSTRACTION = 1
    APPLICATION = 2
    VARIABLE = 3

class Node(object):
    '''
    Object for parse tree.
    '''
    left = None
    right = None
    parent = None
    node_type = None
    value = 0

    def __init__(self, node_type):
        self.node_type = node_type

    def to_string(self):
        '''
        Returns a string for the provided node
        '''
        if self.node_type == NodeTypes.ABSTRACTION:
            return u'λ'
        elif self.node_type == NodeTypes.APPLICATION:
            return '@'
        else:
            return self.value


class Parser(object):
    '''
    Parsing structure for the project. Includes lexical analyzer.
    Rules:
        - only recognizes following punctuation: λ \\ . ( )
        - variable names must contain only alphabetical characters
    '''
    raw_string = ''
    lexemes = []
    root = 0

    def parse_file(self, filename):
        '''
        Parses the text inside the given file.
        '''
        try:
            input_file = codecs.open(filename, encoding='utf-8', mode='r')
        except IOError:
            print('cannot open file:', filename)
            exit(1)
        else:
            self.raw_string = input_file.read()
            input_file.close()
            self.lexical_analyzer()
            self.print_lexemes()

    def parse_string(self, input_string):
        '''
        Parses the given string.
        '''
        self.raw_string = input_string
        self.lexical_analyzer()

    def lexical_analyzer(self):
        '''
        Lexically analyzes the string. Fills in the class array, lexemes, with Lexeme objects.
        '''
        # main parse loop that iterates through all text
        cur_char = 0
        # for cur_char in range(0, len(self.raw_string)):
        while cur_char < len(self.raw_string):
            # skip whitspace
            while True:
                # EOF
                if cur_char >= len(self.raw_string):
                    return
                elif not self.raw_string[cur_char].isspace():
                    break
                cur_char = cur_char + 1
            # lamda case
            if self.raw_string[cur_char] == unichr(955) or self.raw_string[cur_char] == '\\':
                new_lexeme = Lexeme(LexemeTypes.LAMDA, 0)
                self.lexemes.append(new_lexeme)
            # period case
            elif self.raw_string[cur_char] == '.':
                new_lexeme = Lexeme(LexemeTypes.PERIOD, 0)
                self.lexemes.append(new_lexeme)
            # left parenthesis case
            elif self.raw_string[cur_char] == '(':
                new_lexeme = Lexeme(LexemeTypes.LEFT_PAREN, 0)
                self.lexemes.append(new_lexeme)
            # right parenthesis case
            elif self.raw_string[cur_char] == ')':
                new_lexeme = Lexeme(LexemeTypes.RIGHT_PAREN, 0)
                self.lexemes.append(new_lexeme)
            # identifier case
            elif self.raw_string[cur_char].isalpha():
                new_lexeme = Lexeme(LexemeTypes.IDENTIFIER, self.raw_string[cur_char])
                self.lexemes.append(new_lexeme)
            # other character is an error
            else:
                print('ERROR: unrecognized character: ' + self.raw_string[cur_char])
            # increment counter
            cur_char = cur_char + 1

    def create_parse_tree(self):
        '''
        Initiates the creation of parse tree.
        '''
        self.root = self.parse_expression(self.lexemes)

    def parse_expression(self, expression):
        '''
        Recursively parses an expression. Takes array of lexemes. Returns root node.
        '''
        # iterate through lexemes
        cur_lex = 0
        root = 0
        # If abstraction
        if expression[cur_lex].lex_type == LexemeTypes.LAMDA:
            # Set node to lamda
            root = Node(NodeTypes.ABSTRACTION)
            cur_lex += 1
            # put variable as left child
            root.left = Node(NodeTypes.VARIABLE)
            root.left.value = expression[cur_lex].value
            cur_lex += 1
            cur_lex += 1
            # put the rest as right child
            root.right = self.parse_expression(expression[cur_lex:])
        # If variable
        elif expression[cur_lex].lex_type == LexemeTypes.IDENTIFIER:
            root = Node(NodeTypes.APPLICATION)
            root.left = Node(NodeTypes.VARIABLE)
            root.left.value = expression[cur_lex].value
            cur_lex += 1
            root.right = Node(NodeTypes.VARIABLE)
            root.right.value = expression[cur_lex].value
        return root

    def print_lexemes(self):
        '''
        Prints the list of lexemes
        '''
        for i in range(0, len(self.lexemes)):
            print(self.lexemes[i].to_string(), end='')
        print()

    def print_tree(self, filename):
        '''
        Prints the parse tree using LaTex and QTree
        '''
        try:
            output_file = codecs.open(filename, encoding='utf-8', mode='w')
        except IOError:
            print('cannot write to file:', filename)
            return
        # begin file with headers
        output_file.write('\\documentclass[utf8]{article}\n')
        output_file.write('\\usepackage{qtree}\n')
        output_file.write('\\begin{document}\n\n')
        output_file.write('\\Tree ')
        # Traverse tree here
        self.print_tree_rec(output_file, self.root)
        # complete file
        output_file.write('\n\n\\end{document}\n')
        output_file.close()

    def print_tree_rec(self, output_file, node):
        '''
        Recursive function for print_tree()
        '''
        # A node has either 0 or 2 children. If 0, just output it's value (it must be a variable)
        if node.left is None:
            output_file.write(node.to_string())
        # If node has children, need to use brackets and period, and recurse
        else:
            output_file.write('[')
            output_file.write('.')
            if node.node_type == NodeTypes.ABSTRACTION:
                output_file.write('$\\lambda$')
            else:
                output_file.write(node.to_string())
            output_file.write(' ')
            self.print_tree_rec(output_file, node.left)
            output_file.write(' ')
            self.print_tree_rec(output_file, node.right)
            output_file.write(' ')
            output_file.write(']')

    def clear_lexemes(self):
        '''
        Re-initialize lexemes container to clear it
        '''
        self.lexemes = []

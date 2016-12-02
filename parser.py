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

    @staticmethod
    def to_string(lex_type):
        '''
        Returns a string for the provided lexeme type.
        '''
        if lex_type == LexemeTypes.LAMDA:
            return 'lamda'
        elif lex_type == LexemeTypes.PERIOD:
            return 'period'
        elif lex_type == LexemeTypes.LEFT_PAREN:
            return 'left parenthesis'
        elif lex_type == LexemeTypes.RIGHT_PAREN:
            return 'right parenthesis'
        else:
            return 'identifier'

class Lexeme(object):
    '''
    Simple object for lexical analyzer.
    '''
    lex_type = 0
    value = 0
    def __init__(self, lex_type, value):
        self.lex_type = lex_type
        self.value = value

class Parser(object):
    '''
    Parsing structure for the project. Includes lexical analyzer.
    Rules:
        - only recognizes following punctuation: λ \ . ( )
        - variable names must contain only alphabetical characters
    '''
    raw_string = ''
    lexemes = []

    def parse_file(self, filename):
        '''
        Parses the text inside the given file.
        '''
        try:
            input_file = codecs.open(filename, encoding='utf-8', mode='r')
        except IOError:
            print('cannot open file: ', filename)
        else:
            self.raw_string = input_file.read()
            input_file.close()
            print('parsing: ' + filename)
            print('########################################')
            print(self.raw_string)
            print('########################################')
            self.lexical_analyzer()

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

    def print_lexemes(self):
        '''
        Prints the list of lexemes
        '''
        for i in range(0, len(self.lexemes)):
            if self.lexemes[i].lex_type == LexemeTypes.IDENTIFIER:
                print(LexemeTypes.to_string(self.lexemes[i].lex_type), end='')
                print(': ' + self.lexemes[i].value)
            else:
                print(LexemeTypes.to_string(self.lexemes[i].lex_type))

    def clear_lexemes(self):
        '''
        Re-initialize lexemes container to clear it
        '''
        self.lexemes = []

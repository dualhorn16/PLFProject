# -*- coding: utf-8 -*-
#************************************************
#	Lamda Calculus Beta Redux Calculator
#	
#	Programming Language Foundations
#
#	Kiel Martyn
#	Dustin Horner
#	
#	-Fall 2016
#
#	-Purpose is to provide generic tree functionality
#	for storing lamda calculus expressions.
#***********************************************/

import copy
import codecs
import os

#A generic representation of a node to use in Tree below.

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
    value = None

    def __init__(self, node_type, value):
        self.left = None
        self.node_type = node_type
        self.right = None
        if node_type == NodeTypes.VARIABLE:
            self.value = value
        else:
            self.value = None

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

    def __str__(self, depth=0):
        ret = ""

        # Print right branch
        if self.right != None:
            ret += self.right.__str__(depth + 1)

        # Print own value
        ret += "\n" + ("       "*depth) + str(self.to_string())

        # Print left branch
        if self.left != None:
            ret += self.left.__str__(depth + 1)

        return ret



class Tree:
    '''
    A generic representation of a tree to use after parsing Lamda Calc Expression.
    '''
    recurse_num = 0

    def createNode(self, node_type, value):
        return Node(node_type, value)

    def insert(self, node , node_type, value):
        '''
        Will have to fix this guy for the parser, not sure this operates the way it needs to.
        Can create trees by using nodes themselves... [ex. root.right.left.data = Node("data")]
        '''
        if node is None:
            return self.createNode(node_type, value)
        if node.left == None:
            node.left = self.insert(node.left, node_type, value)
            return node
        elif node.right == None:
            node.right = self.insert(node.right, node_type, value)
            return node
        node.left = self.insert(node.left, node_type, value)
        node.right = self.insert(node.right, node_type, value)

    def beta_redux_present(self, node, prev_value):
        '''
        This function is called with arguements of (root_node, False) to test ...
        ...if any part of the entire tree contains a beta redux.
        '''
        return_value = prev_value
        if node is not None:
            if node.node_type == NodeTypes.APPLICATION and node.left.node_type == NodeTypes.ABSTRACTION:
                return_value = True
            return_value = self.beta_redux_present(node.left, return_value)
            return_value = self.beta_redux_present(node.right, return_value)
        return return_value

    def replacement(self, node, identifier, arguement):
        '''
        This function is only called by perform_beta_redux()
        '''
        if node is None:
            return None
        if node.value == identifier:
            return arguement
        node.left = self.replacement(node.left, identifier, arguement)
        node.right = self.replacement(node.right, identifier, arguement)
        # self.recurse_num += 1
        # print(self.recurse_num)
        return node

    def perform_beta_redux(self, node):
        '''
        This burrows down given node to LEFT first then RIGHT and finds a beta reduction...
        ...performs it and then returns what should be returned given its location.
        '''
        if node is not None:
            if node.node_type == NodeTypes.APPLICATION and node.left.node_type == NodeTypes.ABSTRACTION:
                identifier = node.left.left.value
                arguement = copy.deepcopy(node.right)
                node = self.replacement(node.left.right, identifier, arguement)
            else:
                if self.beta_redux_present(node.left, False):
                    node.left = self.perform_beta_redux(node.left)
                else:
                    node.right = self.perform_beta_redux(node.right)
        # self.recurse_num += 1
        # print(self.recurse_num)
        return node

    def height(self, root):
        '''
        Returns the height of a tree/subtree from ROOT.  Used to get height for printNice() arguement.
        '''
        if root is None:
            return 0
        else:
            return max(self.height(root.left), self.height(root.right)) + 1

    def is_evaluatable(self, node, prev_value):
        '''
        function to return true if tree only has variables, and can be arithmetically evaluatable 
        '''
        return_value = prev_value
        if node is not None:
            if node.node_type != NodeTypes.VARIABLE:
                return_value = False
            return_value = self.is_evaluatable(node.left, return_value)
            return_value = self.is_evaluatable(node.right, return_value) 
        return return_value

    def evaluate(self, node, string, count):
        '''
        if we have an arithmetic expression as final tree this func evaluates that
        '''
        #print('this is count: ', count)
        if node is not None and node.left is not None:
            if count % 3 == 1:
                string += '('

        if node is not None:
            string = self.evaluate(node.left, string, count)
            string = string + str(node.value)
            count += 1
            
            if count % 3 == 0:
                string += ')'

            string = self.evaluate(node.right, string, count)
        return string

    def traverseInorder(self, root):
        '''
        These are just tree printing functions.  Not pretty, but helps to see whats going on.
        A better method of illustrating a tree after a given iteration should prolly be looked at.
        '''
        if root is not None:
            self.traverseInorder(root.left)
            print root.data
            self.traverseInorder(root.right)

    def traversePreorder(self, root):
        '''
        These are just tree printing functions.  Not pretty, but helps to see whats going on.
        A better method of illustrating a tree after a given iteration should prolly be looked at.
        '''
        if root is not None:
            print root.data
            self.traversePreorder(root.left)
            self.traversePreorder(root.right)

    def traversePostorder(self, root):
        '''
        These are just tree printing functions.  Not pretty, but helps to see whats going on.
        A better method of illustrating a tree after a given iteration should prolly be looked at.
        '''
        if root is not None:
            self.traversePreorder(root.left)
            self.traversePreorder(root.right)
            print root.data

    def create_test_tree(self):
        root = None
        root = self.insert(root,NodeTypes.APPLICATION, None)
        root.left = Node(NodeTypes.ABSTRACTION, None)
        root.right = Node(NodeTypes.APPLICATION, None)
        root.left.left = Node(NodeTypes.VARIABLE,"x")
        root.left.right = Node(NodeTypes.VARIABLE,"+")
        root.left.right.left = Node(NodeTypes.VARIABLE,"x")
        root.left.right.right = Node(NodeTypes.VARIABLE,"1")
        root.right.left = Node(NodeTypes.ABSTRACTION, None)
        root.right.right = Node(NodeTypes.VARIABLE,"3")
        root.right.left.left = Node(NodeTypes.VARIABLE,"y")
        root.right.left.right = Node(NodeTypes.VARIABLE,"+")
        root.right.left.right.left = Node(NodeTypes.VARIABLE,"y")
        root.right.left.right.right = Node(NodeTypes.VARIABLE,"2")
        return root

    def print_header(self, filename, item):
        try:
            output_file = codecs.open(filename, encoding='utf-8', mode='w')
        except IOError:
            print('cannot write to file:', filename)
            return
        # begin file with headers
        output_file.write('\\documentclass[utf8]{article}\n')
        output_file.write('\\usepackage{qtree}\n')
        output_file.write('\\usepackage[margin=0.5in]{geometry}')
        output_file.write('\\begin{document}\n')
        output_file.write('\\textbf{Reduction Sequence:}\n')
        output_file.write('\\begin{enumerate}\n')
        #output_file.write('\\qtreecenterfalse\n')
        output_file.write('\\item[('+str(item)+')] ')
        output_file.close()

    def print_tree(self, filename, node, item):
        '''
        Prints the parse tree using LaTex and QTree
        '''
        output_file = codecs.open(filename, encoding='utf-8', mode='a')
        character = chr((96 + item) % 128 )
        output_file.write(character + '. ')
        output_file.write('\\Tree ')
        # Traverse tree here
        self.print_tree_rec(output_file, node, 1)

        output_file.write('\n')
        output_file.write('\hskip 0.3in')
        output_file.close()
        return

    def finish_print_nice(self, filename):
        '''
        function to close out the LaTeX and QTree file after all reductions are performed
        '''
        output_file = codecs.open(filename, encoding='utf-8', mode='a')
        output_file.write('\end{enumerate}\n')
        output_file.write('\n\n\\end{document}\n')
        output_file.close()

    def print_flat_tree(self, node, tree_string):
        '''
        Creates string rep. of tree. Needs empty string for initial call.
        '''
        # lamda
        if node.node_type == NodeTypes.ABSTRACTION:
            tree_string += '('
            tree_string += u'λ'
            tree_string += node.left.value
            tree_string += '.'
            if node.right.node_type == NodeTypes.VARIABLE:
                tree_string += node.left.value
            else:
                tree_string = self.print_flat_tree(node.right, tree_string)
            tree_string += ')'
        # application
        elif node.node_type == NodeTypes.APPLICATION:
            if node.right.node_type == NodeTypes.VARIABLE and \
               node.right.node_type == NodeTypes.VARIABLE:
                tree_string += '('
                tree_string = self.print_flat_tree(node.left, tree_string)
                tree_string = self.print_flat_tree(node.right, tree_string)
                tree_string += ')'
            else:
                tree_string += '('
                if self.height(node.left) != 1:
                    tree_string += '('
                    tree_string = self.print_flat_tree(node.left, tree_string)
                    tree_string += ')'
                else:
                    tree_string = self.print_flat_tree(node.left, tree_string)
                tree_string = self.print_flat_tree(node.right, tree_string)
                tree_string += ')'
        # variable
        else:
            tree_string += node.value
        return tree_string

    def print_tree_rec(self, output_file, node, level):
        '''
        Recursive function for print_tree()
        '''
        # A node has either 0 or 2 children. If 0, just output it's value (it must be a variable)
        # If level is 1 and no children... its a 1 node tree (just root)
        if node.left is None:
            if level == 1:
                output_file.write('[')
                output_file.write('.')
            output_file.write(node.to_string())
            if level == 1:
                output_file.write(' ')
                output_file.write(']')

        # If node has children, need to use brackets and period, and recurse
        else:
            
            output_file.write('[')
            output_file.write('.')
            if node.node_type == NodeTypes.ABSTRACTION:
                output_file.write('$\\lambda$')
            else:
                output_file.write(node.to_string())
            output_file.write(' ')
            self.print_tree_rec(output_file, node.left, level+1)
            output_file.write(' ')
            self.print_tree_rec(output_file, node.right, level+1)
            output_file.write(' ')
            output_file.write(']')








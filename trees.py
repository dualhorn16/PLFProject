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
    

    def insertLeft(self , node , node_type, value):
        '''
        Only wrote these next two functions to manually place data in tree w/out having to parse.
        ''' 
        if node is None:
            return self.createNode(node_type, value)
        if node.left == None:
            node.left = self.insertLeft(node.left, node_type, value)

    def insertRight(self , node , node_type, value):
        '''
        Only wrote these next two functions to manually place data in tree w/out haveing to parse.
        '''
        if node is None:
            return self.createNode(node_type, value)
        if node.right == None:
            node.right = self.insertRight(node.right, node_type, value)


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
                node.left = self.perform_beta_redux(node.left)
                node.right = self.perform_beta_redux(node.right)

        return node

    
    def height(self, root):
        '''
        Returns the height of a tree/subtree from ROOT.  Used to get height for printNice() arguement.
        '''
        if root is None:
            return 0
        else:
            return max(self.height(root.left), self.height(root.right)) + 1


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

    def printNice(self, rootnode, height):
        thislevel = [rootnode]
        level = 1
        a = "                                "
        a2 = "================"
        while thislevel:
            nextlevel = list()
            nextlevel2 = list()
            a = a[:len(a)/2]
            for n in thislevel:
                if level is 1:
                    print a[:len(a)-3]+n.to_string(),
                else:
                    print a+n.to_string(),
                if n.left: nextlevel.append(n.left),nextlevel2.append("/") 
                if not n.left and level < height: nextlevel.append(Node(NodeTypes.VARIABLE, a[:(len(a)/4)])),nextlevel2.append(a[:(len(a)/4)])
                if n.right: nextlevel.append(n.right),nextlevel2.append("\\")
                if not n.right and level < height: nextlevel.append(Node(NodeTypes.VARIABLE, a[:(len(a)/4)])),nextlevel2.append(a[:(len(a)/4)])
            print
            for m in nextlevel2:
                if m is "/":
                    print a[:(len(a)/2)] + m,
                elif m is "\\":
                    print a[:(len(a)/2)-1] + m,
                else:
                    print a[:(len(a)/2)] + m,
            print
            level=level+1
            thislevel = nextlevel

    def print_tree(self, filename, node, item):
        '''
        Prints the parse tree using LaTex and QTree
        '''
        if (os.path.exists(filename)):
            try:
                output_file = codecs.open(filename, encoding='utf-8', mode='a')
            except IOError:
                print('cannot write to file:', filename)
                return

        else:
            try:
                output_file = codecs.open(filename, encoding='utf-8', mode='w')
            except IOError:
                print('cannot write to file:', filename)
                return
            # begin file with headers
            output_file.write('\\documentclass[utf8]{article}\n')
            output_file.write('\\usepackage{qtree}\n')
            output_file.write('\\begin{document}\n')
            output_file.write('\\textbf{Reduction Sequence:}\n')
            output_file.write('\\begin{enumerate}\n')
            #output_file.write('\\qtreecenterfalse\n')
            output_file.write('\\item[('+str(item)+')] ')

        character = chr(96 + item)
        output_file.write(character + '. ')
        output_file.write('\\Tree ')
        # Traverse tree here
        self.print_tree_rec(output_file, node, 1)
        # complete file
        output_file.write('\n')
        output_file.write('\hskip 0.3in')
        output_file.close()
        return
            

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








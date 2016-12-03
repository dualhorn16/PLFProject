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

#A generic representation of a node to use in Tree below.
class Node:
    def __init__(self, value):
        self.left = None
        self.data = value
        self.right = None


#A generic representation of a tree to use after parsing Lamda Calc Expression.
class Tree:

    def createNode(self, data):
        return Node(data)
    
    #Will have to fix this guy for the parser, not sure this operates the way it needs to.
    #Can create trees by using nodes themselves... [ex. root.right.left.data = Node("data")]
    def insert(self, node , data):
        if node is None:
            return self.createNode(data)
        if node.left == None:
            node.left = self.insert(node.left, data)
            return node
        elif node.right == None:
            node.right = self.insert(node.right, data)
            return node
        node.left = self.insert(node.left, data)
        node.right = self.insert(node.right, data)
    
    #Only wrote these next two functions to manually place data in tree w/out haveing to parse.
    def insertLeft(self , node , data): 
        if node is None:
            return self.createNode(data)
        if node.left == None:
            node.left = self.insertLeft(node.left, data)

    def insertRight(self , node , data):
        if node is None:
            return self.createNode(data)
        if node.right == None:
            node.right = self.insertRight(node.right, data)

    #This function is called with arguements of (root_node, False) to test ... 
    #...if any part of the entire tree contains a beta redux.
    def beta_redux_present(self, node, prev_value):
        return_value = prev_value
        if node is not None:
            if node.data == "@" and node.left.data == "Lamda":
                return_value = True
            return_value = self.beta_redux_present(node.left, return_value)
            return_value = self.beta_redux_present(node.right, return_value) 
        return return_value

    #This function is only called by perform_beta_redux()
    def replacement(self, node, identifier, arguement):
        if node is None:
            return None
        if node.data == identifier:
            return arguement
        node.left = self.replacement(node.left, identifier, arguement)
        node.right = self.replacement(node.right, identifier, arguement)
        
        return node

    #This burrows down given node to LEFT first then RIGHT and finds a beta reduction...
    #...performs it and then returns what should be returned given its location.
    def perform_beta_redux(self, node):
        if node is not None:
            if node.data == "@" and node.left.data == "Lamda":
                identifier = node.left.left.data
                arguement = copy.deepcopy(node.right)
                self.traverseInorder(arguement)
                node = self.replacement(node.left.right, identifier, arguement)
            else:
                node.left = self.perform_beta_redux(node.left)
                node.right = self.perform_beta_redux(node.right)

        return node

    #These are just tree printing functions.  Not pretty, but helps to see whats going on.
    #A better method of illustrating a tree after a given iteration should prolly be looked at.
    def traverseInorder(self, root):
        if root is not None:
            self.traverseInorder(root.left)
            print root.data
            self.traverseInorder(root.right)

    def traversePreorder(self, root):
        if root is not None:
            print root.data
            self.traversePreorder(root.left)
            self.traversePreorder(root.right)

    def traversePostorder(self, root):
        if root is not None:
            self.traversePreorder(root.left)
            self.traversePreorder(root.right)
            print root.data

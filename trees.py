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
    
    #This will have to be tweaked for how to parse in input from expression.
    def insert(self, node , data):
        if node is None:
            return self.createNode(data)
        if data < node.data:
            node.left = self.insert(node.left, data)
        elif data > node.data:
            node.right = self.insert(node.right, data)
        return node
    
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

    def beta_redux_present(self, node):
        if node is not None:
            if node.data == "@" and node.left.data == "Lamda":
                return True
            self.beta_redux_present(node.left)
            self.beta_redux_present(node.right) 
        return False

    def search(self, node, data):
        if node is None or node.data == data:
            return node

        if node.data < data:
            return self.search(node.right, data)
        else:
            return self.search(node.left, data)

    def deleteNode(self,node,data):
        if node is None:
            return None
        if data < node.data:
            node.left = self.deleteNode(node.left, data)
        elif data > node.data:
            node.right = self.deleteNode(node.right, data)
        else: 
            if node.left is None and node.right is None:
                del node
            if node.left == None:
                temp = node.right
                del node
                return  temp
            elif node.right == None:
                temp = node.left
                del node
                return temp
        return node

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

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

from trees import *


def main():
    
    #EXAMPLE 1:
    #this expression is "(lamda x.x)y"
    tree = Tree()
    root = None
    root = tree.insert(root, "@")
    tree.insertLeft(root, "Lamda")
    tree.insertRight(root, "y")
    tree.insertLeft(root.left, "x")
    tree.insertRight(root.left, "x")
    #tree created... now doing something meaningful.

    print "\n"
    print "Traverse Inorder BEFORE:"
    tree.traverseInorder(root)
    if tree.beta_redux_present(root, False):
        root = tree.perform_beta_redux(root)
    else:
        print "no beta redux present"
    print "\nTraverse Inorder AFTER:"
    tree.traverseInorder(root)
    print "++++++++++++++++++++++\n\n"


    #EXAMPLE 2:
    #This expression (λf.λx.fx)λy.y+1 
    root = None
    tree = Tree()
    root = tree.insert(root, "@")
    root = tree.insert(root, "Lamda")
    root = tree.insert(root, "Lamda")
    #Manually burrowing down to place data in the tree...
    #The tree.insert() func needs to be rewrote to manually place items more than a level deep.
    root.left.left = Node("f")
    root.right.right = Node("+")
    root.right.left = Node("y")
    root.right.right.right = Node("1")
    root.right.right.left = Node("y")
    root.left.right = Node("Lamda")
    root.left.right.left = Node("x")
    root.left.right.right = Node("@")
    root.left.right.right.left = Node("f")
    root.left.right.right.right = Node("x")
    #tree created... now doing something meaningful.


    print "\nBEFORE:"
    tree.traverseInorder(root)
    
    while(1):
        if tree.beta_redux_present(root, False):
            #print "\n\nHere... we ... go!\n\n"
            root = tree.perform_beta_redux(root)
            print "\nAFTER an Iteration:"
            tree.traverseInorder(root)
            #print "WE FOUND ONE!"
            
        else:
            print "no beta redux present exiting...."
            break

    print "++++++++++++++++++++++\n\n"



if __name__ == "__main__":
    main()
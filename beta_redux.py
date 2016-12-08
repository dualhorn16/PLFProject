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
import codecs


def main():
    
    #EXAMPLE 1:
    #this expression is "(lamda x.x)y"
    tree = Tree()
    root = None
    root = tree.insert(root, NodeTypes.APPLICATION, None)
    tree.insertLeft(root, NodeTypes.ABSTRACTION, None)
    tree.insertRight(root, NodeTypes.VARIABLE, "y")
    tree.insertLeft(root.left, NodeTypes.VARIABLE, "x")
    tree.insertRight(root.left, NodeTypes.VARIABLE, "x")
    #tree created... now doing something meaningful.
    print "TREE MANUALLY ENTERED: (λx.x)y"
    print "\n"
    print "BEFORE:"
    item_number = 1
    tree.print_tree("output1.pdf", root, item_number)
    #print root
    tree.printNice(root, tree.height(root))
    #tree.traverseInorder(root)
    if tree.beta_redux_present(root, False):
        root = tree.perform_beta_redux(root)
    else:
        print "no beta redux present"
    print "\nAFTER an Iteration:"
    #print root
    tree.printNice(root, tree.height(root))
    tree.print_tree("output1.pdf", root, item_number+1)
    output_file = codecs.open("output1.pdf", encoding='utf-8', mode='a')
    output_file.write('\end{enumerate}\n')
    output_file.write('\n\n\\end{document}\n')
    output_file.close()
    #tree.traverseInorder(root)
    print "++++++++++++++++++++++\n\n"


    #EXAMPLE 2:
    #This expression (λf.λx.fx)λy.y+1 
    print "TREE MANUALLY ENTERED: (λf.λx.fx)λy.y+1"
    root = None
    tree = Tree()
    root = tree.insert(root, NodeTypes.APPLICATION, None)
    root = tree.insert(root, NodeTypes.ABSTRACTION, None)
    root = tree.insert(root, NodeTypes.ABSTRACTION, None)
    #Manually burrowing down to place data in the tree...
    #The tree.insert() func needs to be rewrote to manually place items more than a level deep.
    root.left.left = Node(NodeTypes.VARIABLE, "f")
    root.right.right = Node(NodeTypes.VARIABLE,"+")
    root.right.left = Node(NodeTypes.VARIABLE,"y")
    root.right.right.right = Node(NodeTypes.VARIABLE,"1")
    root.right.right.left = Node(NodeTypes.VARIABLE,"y")
    root.left.right = Node(NodeTypes.ABSTRACTION, None)
    root.left.right.left = Node(NodeTypes.VARIABLE,"x")
    root.left.right.right = Node(NodeTypes.APPLICATION, None)
    root.left.right.right.left = Node(NodeTypes.VARIABLE,"f")
    root.left.right.right.right = Node(NodeTypes.VARIABLE,"x")
    #tree created... now doing something meaningful.


    print "\nBEFORE:"
    item_number = 1
    tree.print_tree("output2.pdf", root, item_number)
    #print root
    #print 
    #print
    tree.printNice(root, tree.height(root))
    print "----------------------------"
    #tree.traverseInorder(root)
    
    while(1):
        if tree.beta_redux_present(root, False):
            #print "\n\nHere... we ... go!\n\n"
            root = tree.perform_beta_redux(root)
            item_number = item_number + 1
            print "\nAFTER an Iteration:"
            #tree.traverseInorder(root)
            tree.printNice(root, tree.height(root))
            tree.print_tree("output2.pdf", root, item_number)
            #print root
            print "----------------------------"
            #print "WE FOUND ONE!"
            
        else:
            print "No more beta reductions present. Exiting...."
            break

    output_file = codecs.open("output2.pdf", encoding='utf-8', mode='a')
    output_file.write('\end{enumerate}\n')
    output_file.write('\n\n\\end{document}\n')
    output_file.close()
    print "++++++++++++++++++++++\n\n"
    #tree.printNice(root, tree.height(root))
    #print "\nHeight: ",tree.height(root)

    root = None
    tree = Tree()
    root = tree.insert(root,NodeTypes.APPLICATION, None)
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
    print "TREE MANUALLY ENTERED: (λx.x+1)((λy.y+2)3)"

    print "\nBEFORE:"
    item_number = 1
    tree.print_tree("output3.pdf", root, item_number)
    tree.printNice(root, tree.height(root))
    print "----------------------------"
    while(1):
        if tree.beta_redux_present(root, False):
            #print "\n\nHere... we ... go!\n\n"
            root = tree.perform_beta_redux(root)
            print "\nAFTER an Iteration:"
            #tree.traverseInorder(root)
            tree.printNice(root, tree.height(root))
            item_number = item_number + 1
            tree.print_tree("output3.pdf", root, item_number)
            #print root
            print "----------------------------"
            #print "WE FOUND ONE!"
            
        else:
            print "No more beta reductions present. Exiting...."
            break

    print "++++++++++++++++++++++\n\n"

    output_file = codecs.open("output3.pdf", encoding='utf-8', mode='a')
    output_file.write('\end{enumerate}\n')
    output_file.write('\n\n\\end{document}\n')
    output_file.close()



if __name__ == "__main__":
    main()
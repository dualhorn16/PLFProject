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

from trees import Tree


def main():
    
    print "\n"
    tree = Tree()
    root = None
    root = tree.insert(root, "@")
    print root
    tree.insertLeft(root, "Lamda")
    tree.insertRight(root, "y")
    tree.insertLeft(root.left, "x")
    tree.insertRight(root.left, "x")

    print "\n"
    print "Traverse Inorder"
    tree.traverseInorder(root)
    print tree.beta_redux_present(root)

    root = None
    tree = Tree()
    root = tree.insert(root, "Lamda")
    tree.insertLeft(root, "x")
    tree.insertRight(root, "x")
    print "\n"
    print "Traverse Inorder"
    tree.traverseInorder(root)
    print tree.beta_redux_present(root)



if __name__ == "__main__":
    main()
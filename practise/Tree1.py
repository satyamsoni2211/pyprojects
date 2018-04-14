class Node():
    def __init__(self,data,name):
        self.data = data
        self.left = None
        self.right = None
        self.name = name
        self.gifts = 0

class Tree():

    def __init__(self):
        return None

    def addChild(self,node,data,name):
        if node is None:
            node = Node(data,name)
        elif data > node.data:
            node.right = self.addChild(node.right,data,name)
        else:
            node.left = self.addChild(node.left,data,name)
        return node

    def get_leaf_nodes(self,node):
        leafs = []
        self._collect_leaf_nodes(node, leafs)
        return leafs

    def is_leaf(self,node):
        return node.right is None and node.left is None

    def _collect_leaf_nodes(self, node, leafs):
        if node is None:
            return None
        if self.is_leaf(node):
            leafs.append(node)
        if node is not None:
            self._collect_leaf_nodes(node.left,leafs)
            self._collect_leaf_nodes(node.right,leafs)

    def traverseInorder(self, node):
        """
        traverse function will print all the node in the tree.
        """
        if node is not None:
            self.traverseInorder(node.left)
            print node.data,node.name
            self.traverseInorder(node.right)

    def search(self, node, data):
        """
        Search function will search a node into tree.
        """
        # if root is None or root is the search data.
        if node is None or node.data == data:
            return node

        if node.data < data:
            return self.search(node.right, data)
        else:
            return self.search(node.left, data)

    def delete_node(self,node,name,parent):
        if node.name == name:
            if parent.left and parent.left.name == name:
                parent.left = None
            else:
                parent.right = None
        else:
            if node.right:
                self.delete_node(node.right,name,node)
            if node.left:
                self.delete_node(node.left,name,node)
        return True


tree = Tree()
root = None
n = 5
a = [-1,0,0,1,1]
for i in range(n):
    if root is None:
        root = tree.addChild(root,a[i],i)
    else:
        tree.addChild(root,a[i],i)
tree.traverseInorder(root)
print len(tree.get_leaf_nodes(root))
tree.delete_node(root,2,None)
print(len(tree.get_leaf_nodes(root)))
tree.delete_node(root,3,None)
print(len(tree.get_leaf_nodes(root)))
tree.delete_node(root,4,None)
print(len(tree.get_leaf_nodes(root)))
# tree.traverseInorder(root)

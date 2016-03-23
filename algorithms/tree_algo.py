#!/usr/bin/env python

class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Tree(object):
    def __init__(self, string):
        self.root = self.deserialize(string)

    def deserialize(self, string):
        if string == '{}' or string == '[]':
            return None
        nodes = [None if val == 'null' else TreeNode(int(val))
                 for val in string.strip('[]{}').split(',')]
        kids = nodes[::-1]
        root = kids.pop()
        for node in nodes:
            if node:
                if kids: node.left  = kids.pop()
                if kids: node.right = kids.pop()
        return root

    def insert_BST(self, root, elem):
        if root == None: root = TreeNode(elem)
        elif elem == root.val: return
        elif elem > root.val: # insert right
            if root.right == None: root.right = TreeNode(elem)
            else: self.insert_BST(root.right, elem)
        else: # insert left
            if root.left == None: root.left = TreeNode(elem)
            else: self.insert_BST(root.left, elem)


class TreeAlgo(object):
    def kthSmallest(self, root, k):
        """https://leetcode.com/problems/kth-smallest-element-in-a-bst/
        :type root: TreeNode
        :type k: int
        :rtype: int
        """
        current = root
        res = 0
        while k > 0:
            if current.left == None:
                res = current.val
                k -= 1
                current = current.right
            else:
                pointer = current.left
                while pointer.right != None and pointer.right != current:
                    pointer = pointer.right
                if pointer.right == None:
                    pointer.right = current
                    current = current.left
                else:
                    pointer.right = None
                    res = current.val
                    k -= 1
                    current = current.right
        return res

        def morris_inorder(self, root):
        current = root
        while current != None:
            if current.left == None:
                yield current.val
                current = current.right
            else:
                pointer = current.left
                while pointer.right != None and pointer.right != current:
                    pointer = pointer.right
                if pointer.right == None:
                    pointer.right = current
                    current = current.left
                else:
                    pointer.right = None
                    yield current.val
                    current = current.right

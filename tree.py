import numpy as np
import math


class tree:

    def is_leaf(self, node):
        if node.left == None and node.right == None:
            return True
        else:
            return False
    #####
    # xval and yval are neither NULL if the node is a leaf, counts is int, middle is None for #a leaf node, for other non-leaf node, middle is a root of 1D range tree sorted by y #value
    #####

    class Node:

        def __init__(self, counts, xval=None, yval=None, xRange=None, yRange=None, left=None, right=None, middle=None):
            self.xval = xval
            self.yval = yval
            self.xRange = xRange
            self.yRange = yRange
            self.counts = counts
            self.left = left
            self.right = right
            self.middle = middle

        def getCounts(self):
            return self.counts

        def getxVal(self):
            return self.xval

        def setxVal(self, newval):
            self.xval = newval

        def getyVal(self):
            return self.yval

        def setyVal(self, newval):
            self.yval = newval

        def getxRange(self):
            return self.xRange

        def setxRange(self, newval):
            self.xRange = newval

        def getyRange(self):
            return self.yRange

        def setyRange(self, newval):
            self.yRange = newval

        def getLeft(self):
            return self.left

        def getRight(self):
            return self.right

        def getMiddle(self):
            return self.middle

        def setMiddle(self, newmiddle):
            self.middle = newmiddle

        def setLeft(self, newleft):
            self.left = newleft

        def setRight(self, newright):
            self.right = newright

        # This method deserves a little explanation. It does an inorder traversal
        # of the nodes of the tree yielding all the values. In this way, we get
        # the values in ascending order.
        def __iter__(self):
            if self.left != None:
                for elem in self.left:
                    yield elem

            yield [self.xval, self.yval]

            if self.right != None:
                for elem in self.right:
                    yield elem

        def __repr__(self):
            return "2DRangeTree.Node(counts: " + repr(self.counts) + ",xval: " + repr(self.xval) + ",yval: " + repr(self.yval) + ",leftchild: " + repr(self.left) + ",rightchild: " + repr(self.right) + ",middle: " + repr(self.middle) + ")"
    # Below are the methods of the Tree class.

    def build2dtree(self, array, axis=0):
        # axis = 0 ,sorted by x value, 1 by y value
        # print(array)
        if axis == 0:
            sortarray = np.array(sorted(array, key=lambda x: x[axis]))
            # l = len(sortarray)
            # l is the number of unique x, c is the total count
            uni_0_array = np.unique(sortarray.T[0])
            l = len(uni_0_array)
            c = len(sortarray)
            if l == 1:
                # in this case, all the data points has the same x, maybe different y
                a = tree.Node(c, sortarray[0][0], None, [sortarray[0][0], sortarray[-1][0]], None)
                middle = self.build2dtree(sortarray, 1)
                a.setMiddle(middle)
                # print(a)
                return a
            else:
                k = math.ceil(l / 2)
                # print(k, sortarray)
                root = tree.Node(c, (uni_0_array[k - 1] + uni_0_array[k]) / 2, None, [sortarray[0][axis], sortarray[-1][axis]], None)
                d = list(sortarray[:, 0]).index(uni_0_array[k])
                left = self.build2dtree(sortarray[:d], axis)
                right = self.build2dtree(sortarray[d:], axis)
                middle = self.build2dtree(sortarray, 1)
                root.setMiddle(middle)
                root.setLeft(left)
                root.setRight(right)
                return root

        else:
            sortarray = np.array(sorted(array, key=lambda x: x[axis]))
            uni_1_array = np.unique(sortarray.T[1])
            # l = len(sortarray)
            # l is the number of unique y, c is the total count
            l = len(uni_1_array)
            c = len(sortarray)
            if l == 1:
                return tree.Node(c, None, sortarray[0][1], None, [sortarray[0][1], sortarray[-1][1]])
            else:
                k = math.ceil(l / 2)
                root = tree.Node(c, None, (uni_1_array[k - 1] + uni_1_array[k]) / 2, None, [sortarray[0][axis], sortarray[-1][axis]])
                d = list(sortarray[:, 1]).index(uni_1_array[k])
                left = self.build2dtree(sortarray[:d], axis)
                right = self.build2dtree(sortarray[d:], axis)
                root.setLeft(left)
                root.setRight(right)
                return root

    def __init__(self, array):
        self.tree = self.build2dtree(array)

#####

    def OneDSearch(self, B, E, T, axis=0):
        nodelist = 0
        if axis == 0:
            if self.is_leaf(T):
                if T.xval >= B and T.xval <= E:
                    return T.counts
                else:
                    return 0
            else:
                if T.xRange[0] >= B and T.xRange[1] <= E:
                    print("all")
                    nodelist += T.counts
                elif T.xRange[0] > E or T.xRange[1] < B:
                    print("out of bound")
                    nodelist += 0
                elif T.xval > E:
                    print("left")
                    nodelist += self.OneDSearch(B, E, T.left, 0)
                elif T.xval < B:
                    print("right")
                    nodelist += self.OneDSearch(B, E, T.right, 0)
                else:
                    print("between")
                    nodelist += self.OneDSearch(B, E, T.left, 0)
                    nodelist += self.OneDSearch(B, E, T.right, 0)

        else:
            if self.is_leaf(T):
                if T.yval >= B and T.yval <= E:
                    return T.counts
                else:
                    return 0
            else:
                if T.yRange[0] >= B and T.yRange[1] <= E:
                    print("all")
                    nodelist += T.counts
                elif T.yRange[0] > E or T.yRange[1] < B:
                    print("out of bound")
                    nodelist += 0
                elif T.yval > E:
                    print("left")
                    nodelist += self.OneDSearch(B, E, T.left, 1)
                elif T.yval < B:
                    print("right")
                    nodelist += self.OneDSearch(B, E, T.right, 1)
                else:
                    print("between")
                    nodelist += self.OneDSearch(B, E, T.left, 1)
                    nodelist += self.OneDSearch(B, E, T.right, 1)

        return nodelist

    def twoDSearch(self, Bx, Ex, By, Ey, T):
        nodelist = 0
        if T.xRange[0] >= Bx and T.xRange[1] <= Ex:
            print("all")
            nodelist += self.OneDSearch(By, Ey, T.middle, 1)

        elif T.xRange[0] > Ex or T.xRange[1] < Bx:
            print("out of bound")
            nodelist += 0

        elif T.xval > Ex:
            print("left")
            nodelist += self.twoDSearch(Bx, Ex, By, Ey, T.left)

        elif T.xval < Bx:
            print("right")
            nodelist += self.twoDSearch(Bx, Ex, By, Ey, T.right)
        else:
            print("between")
            nodelist += self.twoDSearch(Bx, Ex, By, Ey, T.left)
            nodelist += self.twoDSearch(Bx, Ex, By, Ey, T.right)

        return nodelist

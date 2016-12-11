from enumeration import enum

class RBTree(object):
    
    NodeColor = enum('NodeColor', RED = 1, BLACK = 2)
    
    NIL = 0
    
    __INDEX_OUT_OF_RANGE_ERROR = 'Index out of range: %(index)s; allowed indexes: %(allowed)s'
    
    def __init__(self):
        self.__root = RBTree.NIL
        self.__key = [None]
        self.__left = [RBTree.NIL]
        self.__right = [RBTree.NIL]
        self.__parent = [RBTree.NIL]
        self.__color = [RBTree.NodeColor.BLACK]
        self.__freeList = []
    
    def traverse(self):
        self.__tree_walk(self.__root)
    
    def is_empty(self):
        return self.__root == RBTree.NIL
    
    def print_tree(self):
        self.__print_tree(self.__root, 1)
    
    def insert(self, elem):
        y = RBTree.NIL
        x = self.__root
        while x <> RBTree.NIL:
            y = x
            x = (self.__left[x] if elem < self.__key[x] else
                 self.__right[x])
        newIndex = self.__allocate_node()
        self.__parent[newIndex] = y
        self.__key[newIndex] = elem
        if y == RBTree.NIL:
            self.__root = newIndex
        elif self.__key[newIndex] < self.__key[y]:
            self.__left[y] = newIndex
        else:
            self.__right[y] = newIndex
        self.__color[newIndex] = RBTree.NodeColor.RED
        self.__insert_fixup(newIndex)
    
    def search(self, elem):
        return self.__search_iter(elem)
    
    def min(self):
        return self.__subtree_min(self.__root)
    
    def max(self):
        return self.__subtree_max(self.__root)
    
    def successor(self, x):
        self.__check_index(x)
        if self.__right[x] <> RBTree.NIL:
            return self.subtree_min(self.__right[x])
        y = self.__parent[x]
        while y <> RBTree.NIL and x == self.__right[y]:
            x = y
            y = self.__parent[y]
        return y
    
    def delete(self, p):
        self.__check_index(p)
        y = (p if self.__left[p] == RBTree.NIL or self.__right[p] == RBTree.NIL else
             self.successor(p))
        x = (self.__left[y] if self.__left[y] <> RBTree.NIL else
             self.__right[y])
        self.__parent[x] = self.__parent[y]
        if self.__parent[y] == RBTree.NIL:
            self.__root = x
        elif y == self.__left[self.__parent[y]]:
            self.__left[self.__parent[y]] = x
        else:
            self.__right[self.__parent[y]] = x
        if y <> p:
            self.__key[p] = self.__key[y]
            self.__left[p] = self.__left[y]
            self.__right[p] = self.__right[y]
            self.__parent[p] = self.__parent[y]
            self.__color[p] = self.__color[y]
        if self.__color[y] == RBTree.NodeColor.BLACK:
            self.__delete_fixup(x)
        self.__deallocate_node(y)
        return y
    
    def delete_elem(self, elem):
        try:
            p = self.search(elem)
            return self.delete(p)
        except IndexError:
            print 'No such element in the tree'
            return None
    
    def get_value(self, p):
        self.__check_index(p)
        return self.__key[p]
        
    def values(self):
        return [e for e in self.__key if not (e is None)]
    
    def __subtree_min(self, p):
        self.__check_index(p)
        while self.__left[p] <> RBTree.NIL:
            p = self.__left[p]
        return p
    
    def __subtree_max(self, p):
        self.__check_index(p)
        while self.__right[p] <> RBTree.NIL:
            p = self.__right[p]
        return p
    
    def __left_rotate(self, x):
        if self.__right[x] <> RBTree.NIL:
            y = self.__right[x]
            self.__right[x] = self.__left[y]
            if self.__left[y] <> RBTree.NIL:
                self.__parent[self.__left[y]] = x
            self.__parent[y] = self.__parent[x]
            if self.__parent[x] == RBTree.NIL:
                self.__root = y
            elif x == self.__left[self.__parent[x]]:
                self.__left[self.__parent[x]] = y
            else:
                self.__right[self.__parent[x]] = y
            self.__left[y] = x
            self.__parent[x] = y
    
    def __right_rotate(self, x):
        if self.__left[x] <> RBTree.NIL:
            y = self.__left[x]
            self.__left[x] = self.__right[y]
            if self.__right[y] <> RBTree.NIL:
                self.__parent[self.__right[y]] = x
            self.__parent[y] = self.__parent[x]
            if self.__parent[x] == RBTree.NIL:
                self.__root = y
            elif x == self.__right[self.__parent[x]]:
                self.__right[self.__parent[x]] = y
            else:
                self.__left[self.__parent[x]] = y
            self.__right[y] = x
            self.__parent[x] = y
    
    def __insert_fixup(self, p):
        while self.__color[self.__parent[p]] == RBTree.NodeColor.RED:
            if self.__parent[p] == self.__left[self.__parent[self.__parent[p]]]:
                y = self.__right[self.__parent[self.__parent[p]]]
                if self.__color[y] == RBTree.NodeColor.RED:
                    self.__color[self.__parent[p]] = RBTree.NodeColor.BLACK
                    self.__color[y] = RBTree.NodeColor.BLACK
                    self.__color[self.__parent[self.__parent[p]]] = RBTree.NodeColor.RED
                    p = self.__parent[self.__parent[p]]
                else:
                    if p == self.__right[self.__parent[p]]:
                        p = self.__parent[p]
                        self.__left_rotate(p)
                    self.__color[self.__parent[p]] = RBTree.NodeColor.BLACK
                    self.__color[self.__parent[self.__parent[p]]] = RBTree.NodeColor.RED
                    self.__right_rotate(self.__parent[self.__parent[p]])
            else:
                y = self.__left[self.__parent[self.__parent[p]]]
                if self.__color[y] == RBTree.NodeColor.RED:
                    self.__color[self.__parent[p]] = RBTree.NodeColor.BLACK
                    self.__color[y] = RBTree.NodeColor.BLACK
                    self.__color[self.__parent[self.__parent[p]]] = RBTree.NodeColor.RED
                    p = self.__parent[self.__parent[p]]
                else:
                    if p == self.__left[self.__parent[p]]:
                        p = self.__parent[p]
                        self.__left_rotate(p)
                    self.__color[self.__parent[p]] = RBTree.NodeColor.BLACK
                    self.__color[self.__parent[self.__parent[p]]] = RBTree.NodeColor.RED
                    self.__right_rotate(self.__parent[self.__parent[p]])
        self.__color[self.__root] = RBTree.NodeColor.BLACK
    
    def __delete_fixup(self, p):
        while p <> RBTree.NIL and self.__color[p] == RBTree.NodeColor.BLACK:
            if p == self.__left[self.__parent[p]]:
                w = self.__right[self.__parent[p]]
                if self.__color[w] == RBTree.NodeColor.RED:
                    self.__color[w] = RBTree.NodeColor.BLACK
                    self.__color[self.__parent[p]] = RBTree.NodeColor.RED
                    self.__left_rotate(self.__parent[p])
                    w = self.__right[self.__parent[p]]
                if (self.__color[self.__left[w]] == RBTree.NodeColor.BLACK and
                    self.__color[self.__right[w]] == RBTree.NodeColor.BLACK):
                    self.__color[w] = RBTree.NodeColor.RED
                    p = self.__parent[p]
                else:
                    if self.__color[self.__right[w]] == RBTree.NodeColor.BLACK:
                        self.__color[self.__left[w]] = RBTree.NodeColor.BLACK
                        self.__color[w] = RBTree.NodeColor.RED
                        self.__right_rotate(w)
                        w = self.__right[self.__parent[p]]
                    self.__color[w] = self.__color[self.__parent[p]]
                    self.__color[self.__parent[p]] = RBTree.NodeColor.BLACK
                    self.__color[self.__right[w]] = RBTree.NodeColor.BLACK
                    self.__left_rotate(self.__parent[p])
                    p = self.__root
            else:
                w = self.__left[self.__parent[p]]
                if self.__color[w] == RBTree.NodeColor.RED:
                    self.__color[w] = RBTree.NodeColor.BLACK
                    self.__color[self.__parent[p]] = RBTree.NodeColor.RED
                    self.__left_rotate(self.__parent[p])
                    w = self.__left[self.__parent[p]]
                if (self.__color[self.__right[w]] == RBTree.NodeColor.BLACK and
                    self.__color[self.__left[w]] == RBTree.NodeColor.BLACK):
                    self.__color[w] = RBTree.NodeColor.RED
                    p = self.__parent[p]
                else:
                    if self.__color[self.__left[w]] == RBTree.NodeColor.BLACK:
                        self.__color[self.__right[w]] = RBTree.NodeColor.BLACK
                        self.__color[w] = RBTree.NodeColor.RED
                        self.__right_rotate(w)
                        w = self.__left[self.__parent[p]]
                    self.__color[w] = self.__color[self.__parent[p]]
                    self.__color[self.__parent[p]] = RBTree.NodeColor.BLACK
                    self.__color[self.__left[w]] = RBTree.NodeColor.BLACK
                    self.__left_rotate(self.__parent[p])
                    p = self.__root
        self.__color[p] = RBTree.NodeColor.BLACK

    def __search_subtree(self, elem, curr):
        if curr <> RBTree.NIL or elem == self.__key[curr]:
            return curr
        elif elem < self.__key[curr]:
            return self.__search_subtree(elem, self.__left[curr])
        else:
            return self.__search_subtree(elem, self.__right[curr])
        
    def __search_iter(self, elem):
        curr = self.__root
        while curr <> RBTree.NIL and elem <> self.__key[curr]:
            curr = (self.__left[curr] if elem < self.__key[curr] else
                    self.__right[curr])
        return curr
    
    def __allocate_node(self):
        if len(self.__freeList) == 0:
            self.__key.append(None)
            self.__left.append(RBTree.NIL)
            self.__right.append(RBTree.NIL)
            self.__parent.append(RBTree.NIL)
            self.__color.append(None)
            return len(self.__key) - 1
        else:
            return self.__freeList.pop()
    
    def __deallocate_node(self, index):
        self.__freeList.append(index)
        self.__key[index] = None
        self.__left[index] = RBTree.NIL
        self.__right[index] = RBTree.NIL
        self.__parent[index] = RBTree.NIL
        self.__color[index] = None
        self.__trim_size()
    
    def __trim_size(self):
        if len(self.__freeList) > 100:
            lastOccupied = len(self.__key) - 1
            for i in range(len(self.__key) - 1, 1, -1):
                if not (self.__key[i] is None):
                    lastOccupied = i
                    break 
            del self.__key[lastOccupied + 1:]
            del self.__parent[lastOccupied + 1:]
            del self.__left[lastOccupied + 1:]
            del self.__right[lastOccupied + 1:]
            del self.__color[lastOccupied + 1:]
            self.__freeList = filter(lambda i: i <= lastOccupied, self.__freeList)
            
    def __check_index(self, index):
        if not ((0 <= index < len(self.__key)) and not (index in self.__freeList)):
            msg = RBTree.__INDEX_OUT_OF_RANGE_ERROR % { 
             'index': index, 
             'allowed': [i for i in range(0, len(self.__key)) if not (i in self.__freeList)] 
            }
            raise IndexError(msg)
    
    def __tree_walk(self, x):
        if x <> RBTree.NIL:
            self.__tree_walk(self.__left[x])
            print self.__key[x]
            self.__tree_walk(self.__right[x])
    
    def __print_tree(self, x, h):
        if x <> RBTree.NIL:
            self.__print_tree(self.__right[x], h + 1)
            s = '   ' * h
            print s + str(self.__key[x])
            self.__print_tree(self.__left[x], h + 1)
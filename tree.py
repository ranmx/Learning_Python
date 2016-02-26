class TreeBase(object):
    def __init__(self):
        self._size = 0
        self._root = None

    def root(self):
        raise NotImplementedError

    def is_root(self, p):
        return p == self.root()

    def parent(self, p):
        raise NotImplementedError

    def num_children(self, p):
        raise NotImplementedError

    def children(self, p):
        raise NotImplementedError

    def is_leaf(self, p):
        return 0 == self.num_children(p)

    def is_empty(self):
        return self._size == 0

    def positions(self):
        raise NotImplementedError

    def __len__(self):
        return self._size

    def depth(self, p):
        if self.is_root(p):
            return 0
        else:
            parent = self.parent(p)
            depth = self.depth(parent) + 1
            return depth

    def _height(self, p):
        if self.is_leaf(p):
            height = 0
        else:
            height = 1 + max(self._height(c) for c in self.children(p))
        return height

    def height(self, p=None):
        if p is None:
            return self._height(self.root())
        else:
            return self._height(p)


class LinkTree(TreeBase):
    def __init__(self):
        super(LinkTree, self).__init__()

    class Position(object):
        __slots__ = 'container', 'node'

        def __init__(self, container, node):
            self.container = container
            self.node = node

        def element(self):
            return self.node._element

        def __eq__(self, other):
            return (type(self) == type(other)) and (self.element() == other.element())

        def __ne__(self, other):
            return not (self == other)

    class Node(object):
        __slots__ = ''

        def __init__(self):
            raise NotImplementedError

    def _make_position(self, node):
        if not isinstance(node, self.Node):
            raise TypeError('%s is not a node!' % node)
        else:
            return self.Position(self, node)

    def _is_valid(self, p):
        if not isinstance(p, self.Position):
            raise TypeError(p, 'is not a Position!')
        elif p.container != self:
            raise ValueError(p, 'is not contained in', self)
        elif p.element() is None:
            raise ValueError(p, 'is not valid!')
        return p.node

    def add_root(self, e):
        if self.root() is not None:
            raise ValueError("There is already a root!")
        else:
            self._root = self.Node(e)
            self._size = 1
            return self._make_position(self._root)

    def root(self):
        if self.is_empty():
            return None
        else:
            return self._make_position(self._root)

    def parent(self, p):
        node = self._is_valid(p)
        if node._parent is not None:
            return self._make_position(node._parent)
        return None

    def replace(self, p, element):
        node = self._is_valid(p)
        node._element = element
        return p

    def _deepfirst(self, p, d, path):
        self._is_valid(p)
        self._dprehandle(p, d, path)
        path.append(0)
        for child in self.children(p):
            path[-1] += 1
            self._deepfirst(child, d+1, path)
        path.pop()
        result = self._dposthandle(p, d, path)
        return result

    def _broadfirst(self):
        traversal_list = []
        d = 0
        traversal_list.append([d, self.root()])
        while len(traversal_list) != 0:
            d, p = traversal_list.pop(0)
            self._bprehandle(p, d)
            for child in self.children(p):
                traversal_list.append([d+1, child])
            self._bposthandle(p, d)
        self._bendhandle()

    def _dprehandle(self, p, d, path):
        pass

    def _dposthandle(self, p, d, path):
        return None
        pass

    def _bprehandle(self, p, d):
        pass

    def _bposthandle(self, p, d):
        return None
        pass

    def _bendhandle(self):
        return None
        pass

    def positions(self, broad_first=False):
        if not broad_first:
            self._deepfirst(self.root(), 1, [])
        else:
            self._broadfirst()


class BiTreeBase(TreeBase):
    def __init__(self):
        super(BiTreeBase, self).__init__()

    def left(self, p):
        raise NotImplementedError

    def right(self, p):
        raise NotImplementedError

    def sibling(self, p):
        if p == self.root():
            return None
        parent = self.parent(p)
        if p == self.left(parent):
            return self.left(parent)
        else:
            return self.right(parent)

    def children(self, p):
        if self.left(p) is not None:
            yield self.left(p)
        if self.right(p) is not None:
            yield self.right(p)

    def num_children(self, p):
        count = 0
        for child in self.children(p):
            count += 1
        return count


class BinaryTreeLink(BiTreeBase, LinkTree):
    def __init__(self):
        super(BinaryTreeLink, self).__init__()

    class Node(object):
        __slots__n = '_element', '_parent', '_left', '_right'

        def __init__(self, element, parent=None, left=None, right=None):
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right

    def left(self, p):
        node = self._is_valid(p)
        if node._left is not None:
            return self._make_position(node._left)
        else:
            return None

    def right(self, p):
        node = self._is_valid(p)
        if node._right is not None:
            return self._make_position(node._right)
        return None

    def add_left(self, p, element):
        node = self._is_valid(p)
        if node._left is not None:
            raise ValueError('The node already has a left node')
        new_node = self.Node(element, node)
        node._left = new_node
        self._size += 1
        return self._make_position(new_node)

    def add_right(self, p, element):
        node = self._is_valid(p)
        if node._right is not None:
            raise ValueError('The node already has a right node ')
        new_node = self.Node(element, node)
        node._right = new_node
        self._size += 1
        return self._make_position(new_node)

    def _delete(self, p):
        node = self._is_valid(p)
        if self.num_children(p) > 1:
            raise ValueError('There are more than 2 children')
        else:
            abandoned = p
            orphans = node._left if node._left else node._right
            self._size -= 1
            if p == self.root():
                self._root = orphans
            else:
                parent = self.parent(p)
                if self.left(parent) == p:
                    parent.node._left = orphans
                else:
                    parent.node._right = orphans
                orphans.node._parent = parent
                node._parent = node
                return abandoned.element()

    def attach(self, p, t1, t2=None):
        node = self._is_valid(p)
        if not (type(self) == type(t1)):
            raise TypeError('The input must be an tree')
        if t2 is not None:
            if not (type(self) == type(t2)):
                raise TypeError('The input must be an tree')
            if not self.is_leaf(p):
                raise ValueError("The node doesn't have enough space")
            if not t1.is_empty():
                node._left = t1._root
            if not t2.is_empty():
                node._right = t2._root
                t2._root._parent = node
                self._size += len(t2)
                t2._root = None
                t2._size = 0
        else:
            num_children = self.num_children(p)
            if num_children == 0:
                if not t1.is_empty():
                    node._left = t1._root
            if num_children == 1:
                if not t1.is_empty():
                    if node._left is not None:
                        node._left = t1._root
                    else:
                        node._right = t1._root
            else:
                raise ValueError('The node is full')
        t1._root._parent = node
        self._size += len(t1)
        t1._root = None
        t1._size = 0

    def _inorder(self, p, d, path):
        node = self._is_valid(p)
        if self.left(p) is not None:
            path.append(0)
            self._inorder(self.left(p), d+1, path)
            path.pop(-1)

        self._inorder_func(p, d+1, path)

        if self.right(p) is not None:
            path.append(1)
            self._inorder(self.right(p), d+1, path)
            path.pop(-1)

    def _inorder_func(self, p, d, path):
        path = map(str, path)
        mark = '.'.join(path)
        print d*'  ', '(', mark, ')', p.element()

    def positions(self, broad_first=False):
        return self._inorder(self.root(), 0, [1])


class BinaryTreeArray(TreeBase, BiTreeBase):
    def __init__(self):
        self._list = list()
        self._size = len(self._list)
        super(BinaryTreeArray, self).__init__()

    class Item(object):
        __slots__ = "_value"

        def __init__(self, value, index):
            self._value = value
            self._index = index

        def value(self):
            return self._value

        def index(self):
            return self._index

        def __eq__(self, other):
            return type(self) == type(other) and self.value() == other.value()

        def __ne__(self, other):
            return not self.__eq__(other)

    def root(self):
        if not self.is_empty():
            return self._list[0]
        else:
            return None

    def _is_valid_location(self, j):
        if 0 <= j < self._size:
            if self._list[j].index() == j:
                return self._list[j]
            else:
                ValueError('Index not match')
        else:
            raise IndexError('Not a valid index')

    # j is the index in the list
    # return an index
    def parent_index(self, j):
        item = self._is_valid_location(j)
        if self.is_root(item):
            return None
        else:
            return (j-1)/2

    def parent(self, j):
        parent_index = self.parent_index(j)
        if parent_index:
            return self._list[parent_index]
        else:
            return None

    def add_root(self, element):
        if not self.is_empty():
            raise ValueError('The tree already has a root')
        else:
            item = self.Item(element, 0)
            self._list[0] = item
            return item

    def _deepfirst(self, j, d, path):
        self._is_valid_location(j)
        self._dprehandle(j, d, path)
        path.append(0)
        for child_index in self.children_index(j):
            path[-1] += 1
            self._deepfirst(child_index, d+1, path)
        path.pop()
        self._dposthandle(j, d, path)


    def _dprehandle(self, p, d, path):
        pass

    def _dposthandle(self, p, d, path):
        return None
        pass

    def _bprehandle(self, p, d):
        pass

    def _bposthandle(self, p, d):
        return None
        pass

    def _bendhandle(self):
        return None
        pass

class GeneralTreeLink(LinkTree):
    def __init__(self):
        super(GeneralTreeLink, self).__init__()

    class Node(object):
        __slots__ = '_element', '_parent', '_children'

        def __init__(self, element, parent=None):
            self._element = element
            self._parent = parent
            self._children = []

    def children(self, p):
        node = self._is_valid(p)
        for child in node._children:
            yield self._make_position(child)

    def num_children(self, p):
        node = self._is_valid(p)
        return len(node._children)

    def add_child(self, p, element):
        node = self._is_valid(p)
        child = self.Node(element, node)
        node._children.append(child)
        self._size += 1
        return self._make_position(child)

    def _delete(self, p):
        node = self._is_valid(p)
        abandon = node._element
        if node == self._root:
            self._root = None
            self._size = 0
        else:
            parent = node._parent
            parent._children.remove(node)
            if self.num_children(p) > 0:
                orphans = node._children
                parent._children.extend(orphans)
                for child in orphans:
                    child._parent = parent
            self._size -= 1
        return abandon

    def attach(self, p, tree):
        node = self._is_valid(p)
        if not (isinstance(tree, BinaryTreeLink) or isinstance(tree, GeneralTreeLink)):
            raise TypeError('There must be a tree')
        node._children.append(tree._root)
        tree._root._parent = node
        self._size += len(tree)
        tree._root = None
        tree._size = 0

    def _dprehandle(self, p, d, path):
        mark = '.'.join(map(str, path))
        print '    '*d, "(", mark, ")", p.element()

    d_g = 0

    def _bprehandle(self, p, d):
        if d != self.d_g:
            self.d_g = d
            mark = '\n'
        else:
            mark = ''
        print mark, p.element(), ' ',

    def _bendhandle(self):
        self.d_g = 0
        print ''
        pass




def test_binary_tree():
    bt = BinaryTreeLink()
    root = bt.add_root(5)
    bt_left = bt.add_left(root, 3)
    bt_right = bt.add_right(root, 7)
    bt1 = BinaryTreeLink()
    root1 = bt1.add_root(15)
    bt1.add_left(root1, 13)
    bt1.add_right(root1, 17)
    bt2 = BinaryTreeLink()
    root2 = bt2.add_root(25)
    bt2.add_left(root2, 23)
    bt2.add_right(root2, 27)
    print "-"*40
    bt.positions()
    bt.attach(bt_left, bt1, bt2)
    print "-"*40
    bt.positions()
    print "-"*40
    print 'size of bt:', len(bt)
    print "-"*40
    print 'root of bt:', bt.root().element()
    print "-"*40
    bt_root_left = bt.left(root)
    print 'left node of root:', bt_root_left.element()
    print "-"*40
    bt_root_right = bt.right(root)
    print 'right node of root:', bt_root_right.element()
    print "-"*40
    bt_root_parent = bt.parent(root)
    print 'parent of root:', bt_root_parent
    print "-"*40
    bt_root_left_partent = bt.parent(bt_root_left)
    print 'left node of root:', bt_root_left_partent.element()
    print "-"*40
    bt_root = bt.replace(bt.root(), 42)
    print 'replaced root:', bt_root.element()
    print "-"*40
    bt.positions()
    print "-"*40
    print "depth of the root's left node", bt.depth(bt_root_left)
    print "-"*40
    print "height of the root's left node", bt.height(bt_root_left)


def test_general_tree():
    gt = GeneralTreeLink()
    root = gt.add_root(5)
    jarry = gt.add_child(root, 1)
    kate = gt.add_child(root, 3)
    tom = gt.add_child(root, 7)
    gt.add_child(tom, 10)
    gt.add_child(tom, 12)
    gt.add_child(tom, 15)
    gt.add_child(jarry, 20)
    gig = gt.add_child(jarry, 22)
    gt.add_child(jarry, 25)
    may = gt.add_child(kate, 30)
    gt.add_child(kate, 32)
    gt.add_child(kate, 35)
    delete = kate
    print "-"*40
    for child in gt.children(root):
        print 'chidren of root:', child.element()

    print "-"*40
    gt.positions()
    print "-"*40
    print "broad first"
    gt.positions(broad_first=True)

    gt1 = GeneralTreeLink()
    root = gt1.add_root(5)
    jarry = gt1.add_child(root, 1)
    kate = gt1.add_child(root, 3)
    tom = gt1.add_child(root, 7)
    gt1.add_child(tom, 10)
    gt1.add_child(tom, 12)
    gt1.add_child(tom, 15)
    gt1.add_child(jarry, 20)
    gt1.add_child(jarry, 22)
    gt1.add_child(jarry, 25)
    gt1.add_child(kate, 30)
    gt1.add_child(kate, 32)
    gt1.add_child(kate, 35)

    gt.attach(may, gt1)
    print "-"*40
    gt.positions()

    print "-"*40
    print 'size of bt:', len(gt)
    print "-"*40
    print 'root of bt:', gt.root().element()
    print "-"*40
    print "depth of may", gt.depth(may)
    print "-"*40
    print "height of may", gt.height(may)
    print "-"*40
    print "delete gig", gt._delete(delete)
    gt.positions()
    print "-"*40
    print "broad first"
    gt.positions(broad_first=True)


test_general_tree()

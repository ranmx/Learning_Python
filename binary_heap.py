import tree


class BinaryHeap(tree.BinaryTreeArray):
    def __init__(self):
        super(BinaryHeap, self).__init__()

    def _add_at_end(self, element):
        index = len(self._list)
        new_item = self.Item(element, index)
        self._list.insert(index, new_item)


def test():
    lh = BinaryHeap()
    lh._add_at_end(1)
    lh._add_at_end(2)
    lh._add_at_end(3)

    print "-"*40
    print "list is"
    for items in lh._list:
        print items.value()
    print "-"*40
    print 'is empty:', lh.is_empty()
    print "-"*40
    root = lh.root()
    print 'root of lh:', lh.root().value()
    print "-"*40
    lh_root_left = lh.left(root)
    print 'left node of root:', lh_root_left.value()
    print "-"*40
    lh_root_right = lh.right(root)
    print 'right node of root:', lh_root_right.value()
    print "-"*40
    lh_root_parent = lh.parent(root)
    print 'parent of root:', lh_root_parent
    print "-"*40
    lh_root_left_partent = lh.parent(lh_root_left)
    print 'parent of the left node of root:', lh_root_left_partent.value()
    print "-"*40
    lh.positions()
    print "-"*40
    print "depth of the root's left node", lh.depth(lh_root_left)
    print "-"*40
    print "height of the root's left node", lh.height(lh_root_left)
    print "-"*40
    print "sibling root's left node", lh.sibling(lh_root_left).value()


test()

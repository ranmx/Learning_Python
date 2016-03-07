import tree
import math


class BinaryHeap(tree.BinaryTreeArray):
    def __init__(self):
        super(BinaryHeap, self).__init__()

    class Item(tree.BinaryTreeArray.Item):
        def __lt__(self, other):
            if type(self) == type(other):
                return self.value() < other.value()
            else:
                raise TypeError('Not a item')

    def _add_at_end(self, element):
        index = len(self._list)
        new_item = self.Item(element, index)
        self._list.insert(index, new_item)
        return index

    def _heap_down(self, j):
        item = self._is_valid_location(j)
        mini = item
        for child in self.children(item):
            if child < mini:
                mini = child
        if mini.index() != item.index():
            mini, item = self._swap(mini, item)
            self._heap_down(mini.index())

    def _heap_up(self, j):
        item = self._is_valid_location(j)
        if self.root() != item:
            parent = self.parent(item)
            if item < parent:
                parent, item = self._swap(parent, item)
                new_index = parent.index()
                self._heap_up(new_index)

    def _swap(self, a_item, b_item):
        a_item._value, b_item._value = b_item._value, a_item._value
        return a_item, b_item

    def positions(self):
        return self._broadfirst()

    def _broadfirst(self):
        for item in self._list:
            index = item.index() + 1
            space = math.log(index, 2)
            space = int(space)
            print '|--|'*space, item.value()

    def add_heap(self, element):
        new_index = self._add_at_end(element)
        self._heap_up(new_index)

    def pop_min(self):
        if self.is_empty():
            raise ValueError('The list is empty')
        last_index = len(self._list) - 1
        first = self.root()
        last = self._is_valid_location(last_index)
        self._swap(first, last)
        minimal = self._list.pop()
        if not self.is_empty():
            self._heap_down(0)
        return minimal.value()


def sort_list_with_heap(list_unsort):
    lh = BinaryHeap()
    if not isinstance(list_unsort, list):
        raise TypeError('Not a list')
    length = len(list_unsort)
    for n in range(length):
        item = list_unsort.pop()
        lh.add_heap(item)

    for n in range(length):
        item = lh.pop_min()
        list_unsort.append(item)

    return list_unsort


def test():
    lh = BinaryHeap()
    item_list = [87, 61, 81, 83, 67, 40, 50, 86, 95, 31, 10, 61, 16, 17, 20]
    print 'raw list:', item_list
    for n in range(15):
        lh._add_at_end(item_list[n])

    print "-"*40
    print "list is"
    lh.positions()
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
    print 'child of root:'
    for items in lh.children(root):
        print items.value()
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
    print "-"*40
    lh._heap_down(0)
    print "After heap down, the list is"
    lh.positions()
    print "-"*40
    lh._heap_up(10)
    print "After heap up, the list is"
    lh.positions()
    print "-"*40
    slh = BinaryHeap()
    for n in range(15):
        slh.add_heap(item_list[n])
    print "Heap down while insert, the list is"
    slh.positions()

    print "-"*40
    print "The minimal of the heap is:",
    print slh.pop_min()

    print "-"*40
    print "list is"
    slh.positions()

    print "-"*40
    print "The minimal of the heap is:",
    print slh.pop_min()

    print "-"*40
    print "list is"
    slh.positions()

    print "-"*40
    print "sort a list:"
    item_list = [87, 61, 81, 83, 67, 40, 50, 86, 95, 31, 10, 61, 16, 17, 20]
    print item_list
    sorted_list = sort_list_with_heap(item_list)
    print "after sort: "
    print sorted_list


test()

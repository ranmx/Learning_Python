class SigNode(object):
    def __init__(self, element, next = None):
        self._element = element
        self._next = next


class SigLink(object):

    def __init__(self):
        self.len = 0
        self._head = None
        self._tail = None

    def _is_empty(self):
        return self.len == 0

    def get_head(self):
        if self._is_empty():
            return None
        return self._head._element

    def get_tail(self):
        if self._is_empty():
            return None
        return self._tail._element

    def pop(self):
        head = self.get_head()
        self._del_at_head()
        return head

    def _add_at_tail(self, element):
        new_node = SigNode(element)

        if self._is_empty():
            self._head = self._tail = new_node
        else:
            self._tail._next = new_node
            self._tail = new_node

        self.len += 1
        return new_node._element

    def _add_at_head(self, element):
        new_node = SigNode(element)

        if self._is_empty():
            self._head = self._tail = new_node
        else:
            old_head = self._head
            new_node._next = old_head
            self._head = new_node

        self.len += 1
        return new_node._element

    def _del_at_head(self):

        if self._is_empty():
            raise ValueError('The list is empty!')

        else:
            old_node = self._head
            self._head = old_node._next
            old_node._element = old_node._next = None
            self.len -= 1

    def __iter__(self):
        cursor = self._head
        while cursor is not None:
            yield cursor._element
            cursor = cursor._next

    def swap(self, n1, n2):
        n1_bef = None
        n1_nod = None
        n1_aft = None
        n2_bef = None
        n2_nod = None
        n2_aft = None
        n1_at_head = False
        n2_at_head = False
        cursor = self._head

        if self._head._element == n1:
            n1_nod = cursor
            n1_aft = n1_nod._next
            print "n1= ", n1_nod
            n1_at_head = True
        elif self._head._element == n2:
            n2_nod = cursor
            n2_aft = n2_nod._next
            print "n2= ", n2_nod
            n2_at_head = True

        while cursor._next is not None:

            if cursor._next._element == n1:
                n1_bef = cursor
                n1_nod = n1_bef._next
                n1_aft = n1_nod._next
            elif cursor._next._element == n2:
                n2_bef = cursor
                n2_nod = n2_bef._next
                n2_aft = n2_nod._next

            cursor = cursor._next

        if (n1_nod is not None) and (n2_nod is not None):
            if n1_at_head:
                self._head = n2_nod
            else:
                n1_bef._next = n2_nod
            if n2_at_head:
                self._head = n1_nod
            else:
                n2_bef._next = n1_nod

            n1_nod._next = n2_aft
            n2_nod._next = n1_aft


class SigQueue(SigLink):
    def __init__(self):
        super(SigQueue, self).__init__()

    def add(self, element):
        return self._add_at_tail(element)


class SigStack(SigLink):
    def __init__(self):
        super(SigStack, self).__init__()

    def add(self, element):
        return self._add_at_head(element)


def r7_5():
    link = SigQueue()
    for n in range(10):
        link.add(n)

    for node in link:
        print "node:", node

    # swap n1 and n2:
    n1 = input("type number to be swapped, 1):")
    n2 = input("type number to be swapped, 2):")

    link.swap(n1, n2)

    for node in link:
        print "node:", node


r7_5()








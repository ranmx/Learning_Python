class DlinkBase(object):

    class _DNode(object):

        __slots__ = '_element', '_prev', '_next'

        def __init__(self, element, before, after):
            self._element = element
            self._prev = before
            self._next = after

    def __init__(self):
        self._size = 0
        self.h_sentinel = self._DNode(None, None, None)
        self.t_sentinel = self._DNode(None, None, None)
        self.h_sentinel._next = self.t_sentinel
        self.t_sentinel._prev = self.h_sentinel

    def _is_empty(self):
        return self._size == 0

    def __len__(self):
        return self._size

    def _insert_between(self, element, before, after):
        new_node = self._DNode(element, before, after)
        before._next = new_node
        after._prev = new_node
        self._size += 1
        return new_node

    def _remove_node(self, node):
        prev_node = node._prev
        next_node = node._next
        prev_node._next = next_node
        next_node._prev = prev_node
        node._element = node._next = node._prev = None
        self._size -= 1

    def reverse(self):
        if self._is_empty():
            print "The list is empty!"
            raise ValueError

        cursor = self.h_sentinel._next
        while cursor is not self.t_sentinel:
            cursor._next, cursor._prev = cursor._prev, cursor._next
            cursor = cursor._prev

        self.t_sentinel._prev._prev = self.h_sentinel
        self.h_sentinel._next._next = self.t_sentinel
        self.t_sentinel._prev, self.h_sentinel._next = self.h_sentinel._next, self.t_sentinel._prev


    def __iter__(self):
        if self._is_empty():
            print "The list is empty!"
            raise ValueError
        cursor = self.h_sentinel._next
        while (cursor is not self.t_sentinel) and (cursor is not None):
            yield cursor._element
            cursor = cursor._next


class Dlink(DlinkBase):
    def __init__(self):
        super(Dlink, self).__init__()

    def add_at_head(self, element):
        return self._insert_between(element, self.h_sentinel, self.h_sentinel._next)

    def add_at_tail(self, element):
        return self._insert_between(element, self.t_sentinel._prev, self.h_sentinel)

    def del_at_head(self):
        return self._remove_node(self.h_sentinel._next)

    def del_at_tail(self):
        return self._remove_node(self.t_sentinel._prev)


class PositionalList(DlinkBase):
    def __init__(self):
        super(PositionalList, self).__init__()

    class Position(object):
        def __init__(self, list, node):
            self.list = list
            self.node = node

        def element(self):
            return self.node._element

        def __eq__(self, other):
            return type(self) is type(other) and self.node is other.node

        def __ne__(self, other):
            return not (self == other)

    def _validate_postion(self, p):
        if not isinstance(p, self.Position):
            raise TypeError('P is not a position!')
        if p.node is None:
            raise ValueError('P has no node info!')
        if p.list != self:
            raise ValueError('P is not belong to the list!')
        if (p.node._next is None) or (p.node._prev is None):
            raise ValueError('P is not valid anymore!')

    def _make_position(self, node):
        return self.Position(self, node)

    def _add_position(self, element, prev, next):
        node = self._insert_between(element, prev, next)
        p = self._make_position(node)
        return p

    def add_at_head(self, element):
        return self._add_position(element, self.h_sentinel, self.h_sentinel._next)

    def add_at_tail(self,element):
        return self._add_position(element, self.t_sentinel._prev, self.t_sentinel)

    def first(self):
        if self._is_empty():
            return None
        return self._make_position(self.h_sentinel._next)

    def last(self):
        if self._is_empty():
            return None
        return self._make_position(self.t_sentinel._prev)

    def before(self, p):
        try:
            self._validate_postion(p)
            return self._make_position(p.node._prev)
        except ValueError:
            return None

    def after(self, p):
        try:
            self._validate_postion(p)
            return self._make_position(p.node._next)
        except ValueError:
            return None

    def add_before_position(self, p, element):
        self._validate_postion(p)
        return self._add_position(element, p.node._prev, p.node)

    def add_after_position(self, p, element):
        self._validate_postion(p)
        return self._add_position(element, p.node, p.node._next)

    def get_position(self, p):
        self._validate_postion(p)
        return p.element()

    def pop(self, p):
        element = p.element()
        self._remove_node(p.node)
        p.node = p.list = None
        return element

    def swap(self, p, q):
        self._validate_postion(p)
        self._validate_postion(q)
        p_prev = p.node._prev
        p_next = p.node._next
        q_prev = q.node._prev
        q_next = q.node._next

        p.node._prev, q.node._prev = q.node._prev, p.node._prev
        p.node._next, q.node._next = q.node._next, p.node._next
        p_prev._next = q.node
        p_next._prev = q.node
        q_prev._next = p.node
        q_next._prev = p.node


class PositionalListIt(PositionalList):
    def __init__(self):
        super(PositionalListIt, self).__init__()

    def __iter__(self):
        if self._is_empty():
            raise ValueError('The list is empty!')
        cursor = self.first()
        while cursor.node._next is not None:
            yield cursor
            cursor = self.after(cursor)


def c7_33():
    link = Dlink()
    for n in range(10):
        link.add_at_head(n)

    for node in link:
        print "node:", node

    link.reverse()

    for node in link:
        print "node:", node


def check_link(link):
    print'-'*10, 'check', '-'*10
    for node in link:
        print "node:", node


def c7_36():
    link = PositionalList()
    num = 10
    half = num / 2
    for n in range(num):
        if n == half:
            p_half = link.add_at_head(n)
        else:
            link.add_at_head(n)

    check_link(link)

    print'-'*10, 'reverse', '-'*10
    link.reverse()

    check_link(link)

    print'-'*10, 'operations:', '-'*10
    print 'first:', link.first().element()
    print 'last:', link.last().element()
    print 'The half node:', link.get_position(p_half)
    print 'The node before half:', link.before(p_half).element()
    print 'The node after half:', link.after(p_half).element()
    before = link.add_before_position(p_half, 121)
    after = link.add_after_position(p_half, 132)
    print 'The node added before half:', link.before(p_half).element()
    print 'The node added after half:', link.after(p_half).element()
    print 'The node previous before half:', link.before(before).element()
    print 'The node previous after half:', link.after(after).element()

    print 'Add at head:', link.add_at_head(59).element()
    print 'Add at tail:', link.add_at_tail(62).element()

    check_link(link)

    link.swap(before, after)
    link.swap(link.first(), link.last())
    print'-'*10, 'swap added nodes:', '-'*10
    check_link(link)

    print 'pop the node added before half:', link.pop(before)
    print 'pop the node added after half:', link.pop(after)

    check_link(link)


def check_pos(link):
    print'-'*10, 'check', '-'*10
    for node in link:
        print "node:", node.element()


def c7_37():
    link = PositionalListIt()
    str = raw_input('Give the length of the list')
    try:
        num = int(str)
    except (ValueError, TypeError):
        print "you must type in a integer number"

    dubnum = num * 4
    import random
    for n in range(num):
        element = random.randint(0, dubnum)
        link.add_at_head(element)

    check_pos(link)
    print'-'*10, 'start sorting', '-'*10
    sort_insert(link)

    check_pos(link)


def sort_insert(link):
    mark = link.after(link.first())
    while mark.element() is not None:
        cursor = link.before(mark)
        at_head = None
        while link.before(cursor) is not None:
            if mark.element() > cursor.element():
                if cursor == link.first():
                    at_head = True
                    break
                else:
                    cursor = link.before(cursor)
            else:
                break

        pos = mark
        if mark is not link.last():
            mark = link.after(mark)

        if at_head:
            link.add_at_head(pos.element())
            link.pop(pos)
        else:
            link.add_after_position(cursor, pos.element())
            link.pop(pos)






import random


class SkipList(object):

    class Item(object):
        def __init__(self, value, left=None, right=None, up=None, down=None):
            self._value = value
            self._left = left
            self._right = right
            self._up = up
            self._down = down

        def __eq__(self, other):
            return self._value == other._value

        def __ne__(self, other):
            return not self == other

        def __gt__(self, other):
            return self._value > other._value

    def __init__(self):
        lvl_0_ninf = self._def_ninf()
        lvl_0_pinf = self._def_pinf()
        lvl_0_ninf._right = lvl_0_pinf
        lvl_0_pinf._left = lvl_0_ninf

        self.list = [[]]
        self.left_up = lvl_0_ninf
        self.right_up = lvl_0_pinf
        self._n = 0
        self._h = 0

    def _def_ninf(self):
        ninf = float('-Inf')
        item = self.Item(ninf)
        return item

    def _def_pinf(self):
        pinf = float('Inf')
        item = self.Item(pinf)
        return item

    def __len__(self):
        return self._n

    def __getitem__(self, value):
        pointer = self.left_up
        while True:
            point_r = pointer._right
            if value >= point_r._value:
                pointer = point_r
            elif pointer._down is not None:
                pointer = pointer._down
            elif pointer._value == value:
                return True, pointer
            else:
                return False, pointer

    def add(self, value):
        item = self.Item(value)
        find, pointer = self[value]
        if find is True:
            print "The value is already exist"
        else:
            self._n += 1
            self._h = 0

            while True:
                pointer_r = pointer._right
                item._left = pointer
                item._right = pointer_r
                pointer._right = item
                pointer_r._left = item

                build_up = random.randrange(2)
                if build_up == 0:
                    return
                else:
                    while (pointer._up is None):
                        if pointer == self.left_up:

                            new_ninf = self._def_ninf()
                            new_pinf = self._def_pinf()
                            new_ninf._right = new_pinf
                            new_pinf._left = new_ninf

                            new_ninf._down = self.left_up
                            self.left_up._up = new_ninf
                            new_pinf._down = self.right_up
                            self.right_up._up = new_pinf

                            self.left_up = new_ninf
                            self.right_up = new_pinf

                            self._h += 1
                            self.list.append([])

                        else:
                            pointer = pointer._left
                    pointer = pointer._up

                    new_item = self.Item(value)
                    new_item._down = item
                    item._up = new_item
                    item = new_item

    def print_all(self):
        printer = self.left_up
        left = self.left_up
        while left._down is not None:
            while printer._right is not None:
                print printer._value, ' ',
                printer = printer._right
            print ''
            left = left._down
            printer = left

        while printer._right is not None:
            print printer._value, ' ',
            printer = printer._right
        print ''

    def _print_item(self):
        pointer = self.left_up
        left = self.left_up
        while left._down is not None:
            while pointer._right is not None:
                print pointer, '=', pointer._value, ' ',
                pointer = pointer._right
            print ''
            left = left._down
            pointer = left

        while pointer._right is not None:
            print pointer, '=', pointer._value, ' ',
            pointer = pointer._right


def test():
    skip_list = SkipList()
    skip_list.add(1)
    skip_list.add(2)
    skip_list.add(13)
    skip_list.add(4)
    skip_list.add(14)
    skip_list.add(6)
    skip_list.add(12)
    skip_list.add(7)
    skip_list.add(3)
    skip_list.add(5)
    skip_list.add(15)
    skip_list.add(18)
    print '-' * 25
    skip_list.print_all()


test()

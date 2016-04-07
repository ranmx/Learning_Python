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

        lvl_1_ninf = self._def_ninf()
        lvl_1_pinf = self._def_pinf()
        lvl_1_ninf._right = lvl_1_pinf
        lvl_1_pinf._left = lvl_1_ninf

        lvl_0_ninf._up = lvl_1_ninf
        lvl_1_ninf._down = lvl_0_ninf
        lvl_0_pinf._up = lvl_1_pinf
        lvl_1_pinf._down = lvl_0_pinf

        self.list = [[lvl_0_ninf, lvl_0_pinf]]
        self.left_up = lvl_1_ninf
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
            if value > point_r._value:
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
            pointer._value = value
            while pointer._up is not None:
                if pointer._up == self.left_up:

                    new_ninf = self._def_ninf()
                    new_pinf = self._def_pinf()
                    new_ninf._right = new_pinf
                    new_pinf._left = new_ninf

                    new_ninf._down = self.left_up
                    self.left_up._up = new_ninf
                    new_pinf._down = self.left_up._right
                    self.left_up._right._up = new_pinf
                    self.left_up = new_ninf

                    self._h += 1

                pointer = pointer._up
                pointer._value = value
        else:
            pointer_r = pointer._right
            self._n += 1

            while True:
                item._left = pointer
                item._right = pointer_r
                pointer._right = item
                pointer_r._left = item

                build_up = random.randrange(2)
                if build_up == 0:
                    break
                else:
                    if pointer._up is not None:
                        pointer = pointer._up
                    else:
                        pointer = pointer._left


def test():
    skip_list = SkipList()
    skip_list.add(1)
    skip_list.add(2)
    skip_list.add(3)
    skip_list.add(4)
    skip_list.add(5)
    skip_list.add(6)


test()

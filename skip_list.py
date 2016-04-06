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
        self.list = [[lvl_0_ninf, lvl_0_pinf]]
        self.left_up = lvl_0_ninf

    def _def_ninf(self):
        ninf = float('-Inf')
        item = self.Item(ninf)
        return item

    def _def_pinf(self):
        pinf = float('Inf')
        item = self.Item(pinf)
        return item

    def __get__(self, value):
        pointer = self.left_up
        while True:
            if pointer._right is not None:
                point_r = pointer._right
                if value > point_r._value:
                    pointer = point_r
                else:

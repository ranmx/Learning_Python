import random


class MutableMapping(object):

    def __setitem__(self, key, value):
        raise NotImplementedError

    def __getitem__(self, key):
        raise NotImplementedError

    def __delitem__(self, key):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def __contains__(self, key):
        try:
            self[key]
            return True
        except KeyError:
            return False

    def get(self, key, return_value=None):
        if key in self:
            return self[key]
        else:
            if return_value is not None:
                raise KeyError("The %s is not in the dictionary" % key)
            else:
                return return_value

    def setdefault(self, key, value):
        """
        This function is not efficient because __getitem__ will go though all the position
        while __setitem__ will repeat again
        """
        if key in self:
            return self[key]
        else:
            self[key] = value
            return value

    def pop(self, key, return_value=None):
        if key in self:
            value = self[key]
            del self[key]
            return value
        elif return_value is not None:
            return return_value
        else:
            raise KeyError("The %s is not in the dictionary" % key)

    def popitem(self):
        for key, value in self:
            del self[key]
            return key, value

    def clear(self):
        for key, value in self:
            del self[key]

    def keys(self):
        key_set = []
        for key, value in self:
            key_set.append(key)
        return set(key_set)

    def values(self):
        value_set = []
        for key, value in self:
            value_set.append(self[key])
        return set(value_set)

    def items(self):
        item_set = []
        for key, value in self:
            item_set.append((key, value))
        return set(item_set)

    def update(self, map2):
        for key, value in map2:
            self[key] = value

    def __eq__(self, other):
        for key, value in self:
            if other[key] != value:
                return False
        return True

    def __ne__(self, other):
        return not (self == other)


class MapBase(MutableMapping):
    __slot__ = "key", "value"

    class Item(object):
        def __init__(self, key, value):
            self._key = key
            self._value = value

        def __eq__(self, other):
            return self._key == other._key

        def __ne__(self, other):
            return not (self == other)

        def __lt__(self, other):
            return self._key < other._key


class HashMap(MapBase):
    def __init__(self, cp=11, p=42518164):
        self.a = random.randrange(p - 1)
        self.b = random.randrange(p - 1)
        self.p = p
        self.scale = cp
        self._table = [None] * cp
        self._n = 0

    def _hash_function(self, key):
        i = hash(key)
        hash_num = ((i * self.a + self.b) % self.p) % self.scale
        return hash_num

    def _get_addr(self, key):
        index = self._hash_function(key)
        while True:
            if self._table[index] is 'empty' or self._table[index] is None:
                first_avai = index
                if self._table[index] is None:
                    return False, first_avai
                else:
                    index = (index + 1) % self.scale
            elif self._table[index]._key == key:
                return True, index
            else:
                index = (index + 1) % self.scale

    def __setitem__(self, key, value):
        if self._n >= 0.5*self.scale:
            self.scale *= 2
            self._n = 0
            self._rescale()
        get, index = self._get_addr(key)
        item = self.Item(key, value)
        self._table[index] = item
        if not get:
            self._n += 1

    def _rescale(self):
        old_table = self._table
        self._table = [None] * self.scale
        for item in old_table:
            if item is not None and item is not 'empty':
                self[item._key] = item._value

    def __getitem__(self, key):
        get, index = self._get_addr(key)
        if not get:
            raise KeyError("Key is not found")
        else:
            return self._table[index]._value

    def __delitem__(self, key):
        get, index = self._get_addr(key)
        if not get:
            raise KeyError("Key is not found")
        else:
            item = self._table[index]
            self._table[index] = 'empty'
            self._n -= 1
            if self._n <= 0.25*self.scale:
                print "down scale"
                self.scale //= 2
                self._n = 0
                self._rescale()

    def __len__(self):
        return self._n

    def __iter__(self):
        for item in self._table:
            if item is not 'empty' and \
                            item is not None:
                yield item._key, item._value


def test_map():
    testmap = HashMap()
    testmap[1] = 'a'
    print testmap[1]
    testmap[1] = 'b'
    print testmap[1]
    testmap['a'] = '23'
    testmap['abcd'] = '123'
    testmap[3] = '4'
    testmap[5] = '6'
    testmap['1'] = 'f'
    testmap['2'] = 'fd'
    testmap['431265'] = 'fdsadf'
    testmap['2323aadf'] = 'c'
    testmap[(1, 2, 3)] = 'fdfd'
    for k, v in testmap:
        print "key =", k, "value =", v

    print "delete an item"
    print testmap.pop(3)
    print "delete an item"
    print testmap.pop(8, 'default')
    for k, v in testmap:
        print "key =", k, "value =", v

    print '-' * 20
    print "delete item"
    del testmap[1]
    print "delete 431265"
    del testmap['431265']
    print "delete 2323aadf"
    del testmap['2323aadf']
    print "delete (1, 2, 3)"
    del testmap[(1, 2, 3)]
    for k, v in testmap:
        print "key =", k, "value =", v

    print '-'*20
    print "pop an item:"
    print testmap.popitem()


test_map()

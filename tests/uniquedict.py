class UniqueDict(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)

    def __setitem__(self, key, value):
        if key not in self:
            print "key not in"
            dict.__setitem__(self, key, value)

attr_dict = UniqueDict(dict())
attr_dict['a'] = 'abc'
print attr_dict['a']

attr_dict['a'] = 'def'
print attr_dict['a']


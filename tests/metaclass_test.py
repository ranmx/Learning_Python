import six


class MetaClass (type):
    def __new__(mcs, name, bases, dict):
        print "msc =", mcs
        print "name =", name
        print "bases =", bases
        print "dict ="
        for keys in dict.keys():
            print "    key = ", keys, ", value = ", dict[keys]
        print "\r"
        return super(MetaClass, mcs).__new__(mcs, name, bases, dict)


@six.add_metaclass(MetaClass)
class TestClass(object):
    def __init__(self):
        print "TestClass is called"
        print "\r"


class TestChild(TestClass):
    def __int__(self):
        print "TestChild is called"
        print "\r"
        super(TestChild, self).__init__()


'''
test = TestClass
print "test dict ="
for keys in test.__dict__.keys():
    print "    key = ", keys, ", value = ", test.__dict__[keys]
print "\r"


child = TestChild
print "child dict ="
for keys in child.__dict__.keys():
    print "    key = ", keys, ", value = ", child.__dict__[keys]
print "\r"

'''
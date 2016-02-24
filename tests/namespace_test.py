class InnerClass (object):

    def __init__(self):
        print self.value


class OuterClass (object):

    def __init__(self):
        self.value = "Value got here"
        InnerClass()


OuterClass()


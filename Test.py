class Hi:

    def __init__(self):
        self.a = 2

    def use_a(self):
        print(self.a)

    def test(self):
        self.__dict__['a'] = 'hi'

h = Hi()
print(h.__dict__)
h.test()
print(h.__dict__)
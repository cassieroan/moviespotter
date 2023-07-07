
class Foo(object):
    pass
    # def __repr__(self):
    #     return f"<Foo " + str(self.id) + ">"

b = Foo()
b.id = 5
b.qoux = "Hello world"
b.bar = "More stuff"
b.baz = "Manhattan"

print(b)
print(b.bar)

"""
# data types:
string = "hello"
number = 5
boolean = True
list = ["hello", 5, True]
dict = {"hello": "world", "bar": "Manhattan", "qoux": "More stuff"}

# objects are a lot like dictionaries, but you can customize them more

"""

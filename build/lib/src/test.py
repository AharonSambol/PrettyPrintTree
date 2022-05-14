from PrintTree import PrettyPrintTree
from dataclasses import dataclass


class Tree:
    def __init__(self, value):
        self.val = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)
        return child


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"""Person {{ 
    age: {self.age}, 
    name: {self.name} 
}}"""


from colorama import Back

print()
pt = PrettyPrintTree(lambda x: filter(lambda n: "N" in str(n.val), x.children), lambda x: x.val)
tree = Tree("parent Node")
tree.add_child(Tree(Person("Name", 16)))
# child1 = .add_child(Tree(100))
child2 = tree.add_child(Tree("this is a interesting story\\n"))
child2.add_child(Tree("first line\nsecond line"))
# child2.add_child(Tree("node"))
# child2.add_child(Tree(6))

child2.add_child(Tree(Person("child Node", age=10)))
pt(tree)



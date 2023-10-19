from colorama import Back
from cmd2.ansi import style_aware_wcswidth as wcswidth
from OldPrintTree import PrettyPrintTree


class Tree:
    def __init__(self, value, label=None):
        self.val = value
        self.children = []
        self.label = label

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


tree = Tree("head")
child1 = tree.add_child(Tree(1))
child2 = tree.add_child(Tree(2))
child1_1 = child1.add_child(Tree("!!!!!!!!!!\n::::::::"))
child1_2 = child1.add_child(Tree("wow", label='4%'))
child1_2_1 = child1_2.add_child(Tree("wow's child", label='10%'))
child2_1 = child2.add_child(Tree("an interesting story", label=0.5))
child2_2 = child2.add_child(Tree("an boring story"))
child2_2.add_child(Tree("abc\x1b[31mdgs\x1b[39mdf\nghij\nklmnopqrstuv\nwxyz"))
PrettyPrintTree(lambda x: x.children, lambda x: x.val)(tree)
print()
PrettyPrintTree(lambda x: x.children, lambda x: x.val, border=True)(tree)
print()
PrettyPrintTree(lambda x: x.children, lambda x: x.val, show_newline_literal=True)(tree)
print()
PrettyPrintTree(lambda x: x.children, lambda x: x.val, trim=5, color=Back.BLACK)(tree)
print()
mx_depth1 = PrettyPrintTree(lambda x: x.children, lambda x: x.val, max_depth=3, return_instead_of_print=True)
mx_depth2 = PrettyPrintTree(lambda x: x.children, lambda x: x.val, return_instead_of_print=True)
mx1 = mx_depth1(tree)
mx2 = mx_depth2(tree, max_depth=3)
print(mx1)
print()
assert mx1 == mx2
PrettyPrintTree(lambda x: x.children, lambda x: x.val, lambda x: x.label)(tree)
print()
PrettyPrintTree(lambda x: x.children, lambda x: x.val, lambda x: x.label, label_color=Back.BLACK)(tree)
print()


PrettyPrintTree(lambda x: x.children, lambda x: x.val, default_orientation=PrettyPrintTree.HORIZONTAL)(tree)
print()
PrettyPrintTree(lambda x: x.children, lambda x: x.val,
                default_orientation=PrettyPrintTree.HORIZONTAL,
                show_newline_literal=True)(tree)
print()
PrettyPrintTree(lambda x: x.children, lambda x: x.val,
                default_orientation=PrettyPrintTree.HORIZONTAL, border=True, max_depth=3)(tree)
print()
PrettyPrintTree(lambda x: x.children, lambda x: x.val, trim=5, color=Back.BLACK,
                default_orientation=PrettyPrintTree.HORIZONTAL)(tree)
print()

some_json = {'foo': 1, 'bar': (('a', 'a2'), 'b'), 'qux': {'foo': 1, 'arr': [{1: 2, 2: 1}], 'bar': ['a', 'b']}}
PrettyPrintTree(color=Back.WHITE)(some_json)
print()
PrettyPrintTree().print_json(some_json, name="DICT", max_depth=3)

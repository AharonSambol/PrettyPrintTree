# PrettyPrintTree

This package allows you to print the tree datastructure in a readable fashion (in python).
It supports trees with any kind of data (as long it can be turned into a string).
And even supports multilined nodes (as in strings with \n).

# Documentation

I tried to make this as flexible as possible, so in order to support multiple types of trees
you need to explain to the program how to print your tree. The way to accomplish this is by passing 2 lambdas:
1)  get_value: Given a node of your tree type returns that node's value
    for example if your tree implementation is:
    ```
    class Tree:
        def __init__(self, val):
            self.val = val
    ```
    then get_value would be: 
    ```
    lambda node: node.val
    ```
    (if the value of the tree doesn't implement \_\_str\_\_ get_value should turn it into a string)

2)  get_children: Given a node of your tree type returns a list of all its children (from left to right).
    For example if this is your tree implementation:
    ```
    class Tree:
        def __init__(self, val):
            self.val = val
            self.children = []
    ```
    Then get_children would be as simple as: 
    ```
    lambda node: node.children
    ```
    Or if your tree implementation is:
    ```
    class Tree:
        def __init__(self, val):
            self.val = val
            self.child_right = None
            self.child_left = None
    ```
    Then get_children would be: 
    ```
    lambda node: [node.child_left, node.child_right]
    ```


In order to print the tree you first need to make a PrettyPrintTree Object which you pass your lambdas (and other settings) to,
then you can call it whenever you want without needing to pass the lambdas each time.

## Example

```
pt = PrettyPrintTree(lambda x: x.children, lambda x: x.val)
tree = Tree(1)
child1 = tree.add_child(Tree(2))
child2 = tree.add_child(Tree(3))
child1.add_child(Tree(4))
child1.add_child(Tree(5))
child1.add_child(Tree(6))
child2.add_child(Tree(7))
pt(tree)
```
![plot](https://github.com/AharonSambol/PrettyPrintTree/tree/master/ExampleImages/one_to_seven.JPG)

# Other Settings

## Trim:
Say you only want to print the first few characters of each node (in order to keep the tree small for readability),
then you can set trim to a specific amount of characters.

```
pt = PrettyPrintTree(lambda x: x.children, lambda x: x.val, trim=5)
```
![plot](https://github.com/AharonSambol/PrettyPrintTree/tree/master/ExampleImages/trim.JPG)


## Return Instead of Print:
Instead of printing the tree it can return the string instead if you prefer.

```
to_str = PrettyPrintTree(lambda x: x.children, lambda x: x.val, return_instead_of_print=True)
tree_as_str = to_str(tree)
```

## Color:
You can change the bg color of each node, or even just not use color.

```
from colorama import Back

# change color to black:
pt = PrettyPrintTree(lambda x: x.children, lambda x: x.val, color=Back.BLACK)
```
![plot](https://github.com/AharonSambol/PrettyPrintTree/tree/master/ExampleImages/black.JPG)
```
# without any color:
pt = PrettyPrintTree(lambda x: x.children, lambda x: x.val, color=None)
```
![plot](https://github.com/AharonSambol/PrettyPrintTree/tree/master/ExampleImages/no_color.JPG)


## Border:
You can also surround each node with a little border:
```
pt = PrettyPrintTree(lambda x: x.children, lambda x: x.val, border=True)
```
![plot](https://github.com/AharonSambol/PrettyPrintTree/tree/master/ExampleImages/border.JPG)


## Escape NewLines:
You can escape \n sp that each node will be printed on one line.
Note: \\n wil be escaped into \\\\n so that you can tell the difference
```
pt = PrettyPrintTree(lambda x: x.children, lambda x: x.val, show_newline_literal=True)
```
![plot](https://github.com/AharonSambol/PrettyPrintTree/tree/master/ExampleImages/new_line.JPG)


## Start Message:
You can give a lambda that will be given the tree and will return a string which will be printed before the tree.
```
pt = PrettyPrintTree(lambda x: x.children, lambda x: x.val, start_message=lambda node: f'printing tree of type {node.typ}')
```
![plot](https://github.com/AharonSambol/PrettyPrintTree/tree/master/ExampleImages/msg.JPG)


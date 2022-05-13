import re
from colorama import Back, Style
from typing import *


class PrettyPrintTree:
    def __init__(self,
                 get_children: Callable[[object], List],
                 get_val: Callable[[object], object],
                 show_newline_literal: bool = False,
                 return_instead_of_print: bool = False,
                 trim: bool = False,
                 start_message: Callable[[object], str] = None,
                 color: str | None = Back.LIGHTBLACK_EX,
                 border: bool = False
                 ):
        # this is a lambda which returns a list of all the children
        # in order to support trees of different kinds eg:
        #   self.child_right, self.child_left... or
        #   self.children = []... or
        #   self.children = {}... or anything else
        self.get_children = get_children
        self.get_node_val = get_val
        # only display first x chars
        self.trim = trim
        # if true will display \n as \n and not as new lines
        self.show_newline = show_newline_literal
        self.dont_print = return_instead_of_print
        self.start_message = start_message
        self.color = color
        self.border = border

    def __call__(self, node):
        if self.start_message is not None and not self.dont_print:
            print(self.start_message(node))
        res = self.tree_to_str(node)
        is_node = lambda x: (x.startswith('[') or
                             (x.startswith('│') and x != '│') or
                             len(x) > 1 and x[1:-1] == '─' * (len(x)-2) and x[0] + x[-1] in ['┌┐', '└┘'])
        lines = ["".join(self.color_txt(x) if is_node(x) else x for x in line) for line in res]
        if self.dont_print:
            if self.start_message:
                return self.start_message(node) + "\n" + "\n".join(lines)
            return "\n".join(lines)
        print("\n".join(lines))

    def get_val(self, node):
        st_val = str(self.get_node_val(node))
        if self.trim and len(st_val) > self.trim:
            st_val = st_val[:self.trim] + "..."
        if self.show_newline:
            escape_newline = lambda match: '\\n' if match.group(0) == '\n' else '\\\\n'
            st_val = re.sub(r'(\n|\\n)', escape_newline, st_val)
        if '\n' not in st_val:
            return [[st_val]]
        lst_val = st_val.split("\n")
        longest = max(len(x) for x in lst_val)
        return [[f'{x}{" " * (longest - len(x))}'] for x in lst_val]

    def tree_to_str(self, node):
        val = self.get_val(node)
        if len(self.get_children(node)) == 0:
            if len(val) == 1:
                return [['[' + val[0][0] + ']']]
            return self.format_box("", val)
        to_print = [[]]
        spacing = 0
        for child in self.get_children(node):
            child_print = self.tree_to_str(child)
            for l, line in enumerate(child_print):
                if l + 1 >= len(to_print):
                    to_print.append([])
                if l == 0:
                    len_line = len("".join(line))
                    middle_of_child = len_line - sum(divmod(len(line[-1]), 2))
                    len_to_print_0 = len("".join(to_print[0]))
                    to_print[0].append((spacing - len_to_print_0 + middle_of_child) * " " + '┬')
                to_print[l + 1].append(' ' * (spacing - len("".join(to_print[l + 1]))))
                to_print[l + 1].extend(line)
            spacing = max(len("".join(x)) for x in to_print) + 1

        if len(to_print[0]) != 1:
            new_lines = "".join(to_print[0])
            space_before = len(new_lines) - len(new_lines := new_lines.strip())
            new_lines = " " * space_before + '┌' + new_lines[1:-1].replace(' ', '─') + '┐'
            pipe_pos = middle = len(new_lines) - sum(divmod(len(new_lines.strip()), 2))
            new_ch = {'─': '┴', '┬': '┼', '┌': '├', '┐': '┤'}[new_lines[middle]]
            new_lines = new_lines[:middle] + new_ch + new_lines[middle + 1:]
            to_print[0] = [new_lines]
        else:
            to_print[0][0] = to_print[0][0][:-1] + '│'
            pipe_pos = len(to_print[0][0]) - 1
        spacing = " " * (pipe_pos - sum(divmod(len(val[0][0]), 2)))
        if len(val) == 1:
            val = [[spacing, f'[{val[0][0]}]']]
        else:
            val = self.format_box(spacing, val)
        return val + to_print

    def color_txt(self, x):
        spaces = " " * (len(x) - len(x.lstrip()))
        txt = x.lstrip() if self.border else (" " + x.lstrip()[1:-1] + " ")
        txt = self.color + txt + Style.RESET_ALL if self.color else txt
        return spaces + txt

    def format_box(self, spacing, val):
        for r, row in enumerate(val):
            val[r] = [spacing, f'│{row[0]}│']
        if self.border:
            top = [[spacing, '┌' + '─' * (len(val[0][1]) - 2) + '┐']]
            bottom = [[spacing, '└' + '─' * (len(val[0][1]) - 2) + '┘']]
            return top + val + bottom
        return val

# ---------- example: ----------
# class Tree:
#     def __init__(self, val):
#         self.val = val
#         self.children = []
#
#     def add_child(self, child):
#         self.children.append(child)
#         return child
#
#
# class Person:
#     def __init__(self, age, name):
#         self.age = age
#         self.name = name
#
#     def __str__(self):
#         return f"""Person {{
#     age: {self.age},
#     name: {self.name}
# }}"""
#
#
# tree = Tree(0)
# r = tree.add_child(Tree([1, 2, 3]))
# l = tree.add_child(Tree({1: "qo", 24: " 5326"}))
# rl = r.add_child(Tree(43216))
# rr = r.add_child(Tree(Person(17, "Aharon")))
# rr.add_child(Tree(0))
# lr = l.add_child(Tree(5))
# lm = l.add_child(Tree("\n"))
# ll = l.add_child(Tree(6))
# rl.add_child(Tree("!!!!"))
# rlm = rl.add_child(Tree("!!!!\\n!!"))
# rl.add_child(Tree("!!!!!!"))
# rlm.add_child(Tree("looooong"))
# rlm.add_child(Tree("looooong"))
# pt = PrettyPrintTree(lambda x: x.children, lambda x: x.val)
# pt(node=tree)

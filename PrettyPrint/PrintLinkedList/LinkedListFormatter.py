from typing import TypeVar, Callable, Any

from PrettyPrint.Utils.NodeFormatter import NodeFormatter
from PrettyPrint.Utils.Orientation import Orientation
from PrettyPrint.PrintTree.HorizontalTree import add_parent as add_parent_left
from PrettyPrint.PrintTree.TreeFormatter import TreeFormatter
from PrettyPrint.PrintTree.VerticalTree import add_parent as add_parent_top

T = TypeVar("T")


class LinkedListFormatter:
    Vertical = Orientation.Vertical
    Horizontal = Orientation.Horizontal

    def __init__(
            self,
            get_val: Callable[[T], Any],
            get_next: Callable[[T], T],
            get_prev: Callable[[T], T],
            show_newline_literal: bool,
            newline_literal: str,
            trim: int,
            trim_symbol: str,
            start_message: Callable[[T], str],
            color: str,
            border: bool,
            max_depth: int,
            orientation: bool,
    ):
        self.get_node_val = get_val
        self.get_next = get_next
        self.get_prev = get_prev
        self.trim = trim
        self.trim_symbol = trim_symbol
        self.show_newline = show_newline_literal
        self.newline_literal = newline_literal
        self.start_message = start_message
        self.color = color
        self.border = border
        self.max_depth = max_depth
        self.orientation = orientation

    def format(self, node: T) -> str:
        if self.orientation == Orientation.Vertical:
            res = self.linked_list_vertical_join(node)
        else:
            res = self.linked_list_horizontal_join(node)
        res = res.to_str().rstrip()
        if self.start_message:
            return f'{ self.start_message(node) }\n{ res }'
        return res

    def get_arrow(self, prev_node: T, next_node: T) -> str:
        is_next = self.get_next(prev_node) is next_node
        is_prev = self.get_prev(next_node) is prev_node if self.get_prev else False
        if self.orientation == Orientation.Vertical:
            return {
                (True, True): '↕',
                (True, False): '↓',
                (False, True): '↑',
                (False, False): ' ',
            }[(is_next, is_prev)]
        else:
            return {
                (True, True): '↔',
                (True, False): '→',
                (False, True): '←',
                (False, False): ' ',
            }[(is_next, is_prev)]

    def linked_list_vertical_join(self, node: T, depth: int = 0) -> NodeFormatter:
        nxt = self.get_next(node)
        arrow = self.get_arrow(node, nxt) if nxt else ''
        node = self.add_styles(node)
        if nxt and (self.max_depth == -1 or depth < self.max_depth):
            nxt = self.linked_list_vertical_join(nxt, depth + 1)
            nxt.lines.insert(0, ' ' * nxt.get_middle_width() + arrow)
            return add_parent_top(node, nxt)
        return node

    def linked_list_horizontal_join(self, node: T, depth: int = 0) -> NodeFormatter:
        nxt = self.get_next(node)
        arrow = self.get_arrow(node, nxt) if nxt else ''
        node = self.add_styles(node)
        if nxt and (self.max_depth == -1 or depth < self.max_depth):
            nxt = self.linked_list_horizontal_join(nxt, depth + 1)
            middle = nxt.get_middle_height()
            nxt.lines = [
                (arrow if i == middle else ' ') + line
                for i, line in enumerate(nxt.lines)
            ]
            return add_parent_left(node, nxt)
        return node

    def add_styles(self, node: NodeFormatter) -> NodeFormatter:
        return TreeFormatter.add_styles(self, node)



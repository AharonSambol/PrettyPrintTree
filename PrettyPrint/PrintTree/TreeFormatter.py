from typing import Callable, Iterable, Any, TypeVar

from PrettyPrint.PrintTree.HorizontalTree import join_vertically, add_parent as add_parent_left
from PrettyPrint.PrintTree.VerticalTree import join_horizontally, add_parent as add_parent_top
from PrettyPrint.Utils.NodeFormatter import NodeFormatter
from PrettyPrint.Utils.Orientation import Orientation
from PrettyPrint.Utils.StyleAwareUtils import trim_text

T = TypeVar("T")


class TreeFormatter:
    def __init__(
            self,
            get_children: Callable[[T], Iterable[T]],
            get_val: Callable[[T], Any],
            get_label: Callable[[T], Any],
            label_color: str,
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
        self.get_children = get_children 
        self.get_node_val = get_val
        self.get_label = get_label
        self.label_color = label_color
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
            res = self.tree_vertical_join(node)
        else:
            res = self.tree_horizontal_join(node)
        res = res.to_str().rstrip()
        if self.start_message:
            return f'{ self.start_message(node) }\n{ res }'
        return res

    def tree_vertical_join(self, node: T, depth: int = 0) -> NodeFormatter:
        label = self.get_label(node) if self.get_label else None
        children = self.get_children(node)
        node = self.add_styles(node)
        if children and (self.max_depth == -1 or depth < self.max_depth):
            children = [
                self.tree_vertical_join(child, depth + 1)
                for child in children
            ]
            if len(children) == 1:
                children_node = children[0]
                children_node.lines.insert(0, ' ' * children_node.get_middle_width() + '|')
            else:
                children_node = join_horizontally(children)
            node = add_parent_top(node, children_node)
        node = self.add_label(label, node, add_parent_top, '|')
        return node

    def tree_horizontal_join(self, node: T, depth: int = 0) -> NodeFormatter:
        label = self.get_label(node) if self.get_label else None
        children = self.get_children(node)
        node = self.add_styles(node)
        node_padding = ' ' * node.width
        node.lines = node.lines + [node_padding]
        node.height += 1
        if children and (self.max_depth == -1 or depth < self.max_depth):
            children = [
                self.tree_horizontal_join(child, depth + 1)
                for child in children
            ]
            if len(children) == 1:
                children_node = children[0]
                middle = children_node.get_middle_height()
                children_node.lines = [
                    ('─' if i == middle else ' ') + line
                    for i, line in enumerate(children_node.lines)
                ]
            else:
                children_node = join_vertically(children)
            node = add_parent_left(node, children_node)
        node = self.add_label(label, node, add_parent_left, '─')
        return node

    def add_label(
            self,
            label: Any,
            node: NodeFormatter,
            parent_adder: Callable[[NodeFormatter, NodeFormatter], NodeFormatter],
            seperator: str
    ) -> NodeFormatter:
        if label:
            label = NodeFormatter.from_string(str(label))
            if self.label_color:
                label.color_bg(self.label_color, True)
            node = parent_adder(NodeFormatter.from_string(seperator), node)
            node = parent_adder(label, node)
        return node

    def add_styles(self, node: NodeFormatter) -> NodeFormatter:
        contents = str(self.get_node_val(node))
        if self.show_newline:
            contents = contents.replace('\n', self.newline_literal)
        if self.trim != -1:
            contents = trim_text(contents, self.trim, self.trim_symbol)
        node = NodeFormatter.from_string(contents)
        if self.border:
            node.add_border()
        if self.color:
            node.color_bg(self.color, add_space=not self.border)
        return node

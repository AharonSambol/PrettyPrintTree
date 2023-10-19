from typing import Callable, Iterable, Any, TypeVar
from colorama import Back

from PrettyPrint.PrintLinkedList.LinkedListFormatter import LinkedListFormatter
from PrettyPrint.Utils.Orientation import Orientation


T = TypeVar("T")


class PrettyPrintLinkedList:
    Horizontal = Orientation.Horizontal
    Vertical = Orientation.Vertical

    def __init__(
            self,
            get_val: Callable[[T], Any] = None,
            get_next: Callable[[T], Iterable[T]] = None,
            get_prev: Callable[[T], Iterable[T]] = None,
            *,
            show_newline_literal: bool = False,
            newline_literal: str = "\\n",
            return_instead_of_print: bool = False,
            trim: int = -1,
            trim_symbol: str = "...",
            start_message: Callable[[T], str] = None,
            color: str = Back.LIGHTBLACK_EX,
            border: bool = False,
            max_depth: int = -1,
            orientation: bool = Vertical,
    ):
        self.default_get_node_val = get_val or (lambda x: x.value)
        self.default_get_next = get_next or (lambda x: x.next)
        self.default_get_prev = get_prev
        self.default_trim = trim
        self.default_trim_symbol = trim_symbol
        self.default_show_newline = show_newline_literal
        self.default_newline_literal = newline_literal
        self.default_dont_print = return_instead_of_print
        self.default_start_message = start_message
        self.default_color = color
        self.default_border = border
        self.default_max_depth = max_depth
        self.default_orientation = orientation

    def __call__(
            self,
            node: T,
            get_val: Callable[[T], Any] = None,
            get_prev: Callable[[T], T] = None,
            get_next: Callable[[T], T] = None,
            *,
            show_newline_literal: bool = None,
            newline_literal: str = None,
            return_instead_of_print: bool = None,
            trim: int = -1,
            trim_symbol: str = None,
            start_message: Callable[[T], str] = None,
            color: str = None,
            border: bool = None,
            max_depth: int = -1,
            orientation: bool = None,
    ):
        linked_list_formatter = LinkedListFormatter(
            get_val=get_val or self.default_get_node_val,
            get_next=get_next or self.default_get_next,
            get_prev=get_prev or self.default_get_prev,
            show_newline_literal=self.default_show_newline if show_newline_literal is None else show_newline_literal,
            newline_literal=self.default_newline_literal if newline_literal is None else newline_literal,
            trim=self.default_trim if trim == -1 else trim,
            trim_symbol=self.default_trim_symbol if trim_symbol is None else trim_symbol,
            start_message=start_message or self.default_start_message,
            color=self.default_color if color is None else color,
            border=self.default_border if border is None else border,
            max_depth=max_depth if max_depth != -1 else self.default_max_depth,
            orientation=self.default_orientation if orientation is None else orientation,
        )
        res = linked_list_formatter.format(node)
        if return_instead_of_print or (return_instead_of_print is None and self.default_dont_print):
            return res
        print(res)

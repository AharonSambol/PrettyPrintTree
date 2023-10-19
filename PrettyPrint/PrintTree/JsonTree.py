from typing import Iterable


class JsonTree:
    def __init__(self, val, children=None):
        if children is None:
            if isinstance(val, Iterable) and not isinstance(val, str):
                children = val
                val = str(type(val)).removeprefix("<class '").removesuffix("'>").upper()
            else:
                children = []

        self.val = val
        if isinstance(children, dict):
            self.children = [JsonTree(v, c) for v, c in children.items()]
        elif isinstance(children, Iterable) and not isinstance(children, str):
            self.children = [JsonTree(x) for x in children]
        else:
            self.children = [children]

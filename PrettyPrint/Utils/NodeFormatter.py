import colorama.initialise
from PrettyPrint.Utils.StyleAwareUtils import ljust, text_width


class NodeFormatter:
    @classmethod
    def from_string(cls, content: str):
        lines = content.split('\n')
        height = len(lines)
        width = max(text_width(line) for line in lines)
        return cls(lines, height=height, width=width)

    def __init__(
            self,
            lines: list[str], *, height: int, width: int,
            middle_height: int = None, middle_width: int = None
    ):
        self.lines = lines
        self.height = height
        self.width = width
        self.middle_height = middle_height
        self.middle_width = middle_width

    def add_border(self) -> None:
        if self.height == 1:
            self.width += 2
            self.lines[0] = f'[{ self.lines[0] }]'
        else:
            for i, line in enumerate(self.lines):
                self.lines[i] = '│' + ljust(line, self.width) + '│'
            self.lines.insert(0, '┌' + '─' * self.width + '┐')
            self.lines.append('└' + '─' * self.width + '┘')
            self.width += 2
            self.height += 2

    def color_bg(self, color: str, add_space: bool) -> None:
        if add_space:
            self.lines = [f'{ color } { ljust(line, self.width) } { colorama.Style.RESET_ALL }' for line in self.lines]
            self.width += 2
        else:
            self.lines = [f'{ color }{ ljust(line, self.width) }{ colorama.Style.RESET_ALL }' for line in self.lines]

    def to_str(self) -> str:
        return '\n'.join(self.lines)

    def get_middle_width(self) -> int:
        if self.middle_width is None:
            return sum(divmod(self.width, 2)) - 1
        return self.middle_width

    def get_middle_height(self) -> int:
        if self.middle_height is None:
            return sum(divmod(self.height, 2)) - 1
        return self.middle_height




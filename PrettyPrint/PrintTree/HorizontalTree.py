from PrettyPrint.Utils.NodeFormatter import NodeFormatter
from PrettyPrint.Utils.StyleAwareUtils import ljust
from PrettyPrint.Utils.ZipLongest import zip_longest


def join_vertically(boxes: [NodeFormatter]) -> NodeFormatter:
    lines, width, height = join_boxes(boxes)
    middle = add_pipes(boxes, lines)
    width += 1
    return NodeFormatter(lines, height=height, width=width, middle_height=middle)


def join_boxes(boxes: [NodeFormatter]) -> ([str], int, int):
    lines = [line for box in boxes for line in box.lines]
    width = max(box.width for box in boxes)
    height = sum(box.height for box in boxes) + len(boxes) - 1
    return lines, width, height


def add_pipes(boxes: [NodeFormatter], lines: [str]) -> int:
    start = boxes[0].get_middle_height()
    end = boxes[-1].get_middle_height() + sum(box.height for box in boxes[:-1])
    middles = iter(box.get_middle_height() for box in boxes[1:-1])
    heights = iter(box.height for box in boxes)
    middle = next(middles, None)
    box_start = next(heights)
    for i, line in enumerate(lines):
        if i < start or i > end:
            lines[i] = ' ' + line
        elif i == start:
            lines[i] = '┌' + line
        elif i == end:
            lines[i] = '└' + line
        elif middle is not None and i == box_start + middle:
            lines[i] = '├' + line
            box_start += next(heights)
            middle = next(middles, None)
        else:
            lines[i] = '│' + line

    middle_of_pipes = start + sum(divmod(end - start + 1, 2)) - 1
    pipe_dict = {'┌': '┬', '└': '┴', '│': '┤', '├': '┼'}
    middle_line = lines[middle_of_pipes]
    lines[middle_of_pipes] = pipe_dict[middle_line[0]] + middle_line[1:]
    return middle_of_pipes


def add_parent(parent: NodeFormatter, children: NodeFormatter) -> NodeFormatter:
    parent_middle, children_middle = parent.get_middle_height(), children.get_middle_height()
    parent_width, children_width = parent.width, children.width
    parent.lines = [ljust(line, parent.width) for line in parent.lines]

    middle_offset = children_middle - parent_middle
    parent_padding = ' ' * parent.width
    if middle_offset > 0:
        parent.lines = [parent_padding] * middle_offset + parent.lines
    elif middle_offset < 0:
        children.lines = [''] * (-middle_offset) + children.lines

    lines = [
        (parent_padding if parent_line is None else parent_line) + (child_line or '')
        for parent_line, child_line in zip_longest(parent.lines, children.lines, default=None)
    ]
    return NodeFormatter(
        lines,
        height=max(len(parent.lines), len(children.lines)),
        width=parent_width + children_width,
        middle_height=max(children_middle, parent_middle)
    )

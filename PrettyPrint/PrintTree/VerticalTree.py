from PrettyPrint.Utils.NodeFormatter import NodeFormatter
from PrettyPrint.Utils.StyleAwareUtils import ljust
from PrettyPrint.Utils.ZipLongest import zip_longest


def join_horizontally(boxes: [NodeFormatter]) -> NodeFormatter:
    lines, width, height = join_boxes(boxes)
    middle = add_pipes(boxes, lines)
    height += 1
    return NodeFormatter(lines, height=height, width=width, middle_width=middle)


def join_boxes(boxes: [NodeFormatter]) -> ([str], int, int):
    lines = [
        ' '.join(
            ljust(line, boxes[i].width)
            for i, line in enumerate(lines)
        )
        for lines in zip_longest(*(box.lines for box in boxes), default='')
    ]
    width = sum(box.width for box in boxes) + len(boxes) - 1
    height = max(box.height for box in boxes)
    return lines, width, height


def add_pipes(boxes: [NodeFormatter], lines: [str]) -> int:
    padding = ' ' * boxes[0].get_middle_width()
    pipes = '┌'
    for prev, box in zip(boxes, boxes[1:]):
        pipes += '─' * (prev.width - prev.get_middle_width() + box.get_middle_width()) + '┬'
    middle_of_pipes = sum(divmod(len(pipes), 2)) - 1
    pipes = (
            padding +
            pipes[:middle_of_pipes]
            + {"─": "┴", "┬": "┼", "┌": "├", "┐": "┤"}[pipes[middle_of_pipes]]
            + pipes[middle_of_pipes + 1:-1]
            + '┐'
    )
    lines.insert(0, pipes)
    return len(padding) + middle_of_pipes


def add_parent(parent: NodeFormatter, children: NodeFormatter) -> NodeFormatter:
    parent_middle, children_middle = parent.get_middle_width(), children.get_middle_width()
    parent_width, children_width = parent.width, children.width
    if parent_middle == children_middle:
        lines = parent.lines + children.lines
        middle = parent_middle
    elif parent_middle < children_middle:
        padding = ' ' * (children_middle - parent_middle)
        lines = [padding + line for line in parent.lines] + children.lines
        parent_width += children_middle - parent_middle
        middle = children_middle
    else:
        padding = ' ' * (parent_middle - children_middle)
        lines = parent.lines + [padding + line for line in children.lines]
        children_width += parent_middle - children_middle
        middle = parent_middle
    return NodeFormatter(
        lines,
        height=parent.height + children.height,
        width=max(parent_width, children_width),
        middle_width=middle
    )

from cmd2.ansi import style_aware_wcswidth as text_width


def ljust(text: str, amount: int, padding: str = ' ') -> str:
    return text + padding * (amount - text_width(text))


def rjust(text: str, amount: int, padding: str = ' ') -> str:
    return padding * (amount - text_width(text)) + text


def trim_text(text: str, length: int, symbol: str) -> str:
    flat_text = text.replace('\n', 'n')
    contents_width = text_width(flat_text)
    if contents_width <= length:
        return text
    text_slice = flat_text[:length]
    i = 0
    while text_width(text_slice) < length:
        i += 1
        text_slice = flat_text[:length + i]
    return text[:length + i] + symbol

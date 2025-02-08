from .Align import Align
from . import padding


def centered_text(draw, text, font, container_size, pos='centre', border=False):
    # 🌌 calculate space needed for message
    message_size = max(font.getbbox(line)[-2:] for line in text.split('\n'))

    # 📏 where to position the message
    if pos == 'centre':
        message_x, message_y = Align.Centre(container_size, message_size)
    elif pos == 'topright':
        message_x, message_y = Align.TopRight(container_size, message_size)
    elif pos == 'topleft':
        message_x, message_y = Align.TopLeft(container_size, message_size)

    # 🖊️ draw the message at position
    draw.multiline_text(
        (message_x, message_y),
        text,
        fill='black',
        font=font,
        align="left")
    
    # 📏 measure border box
    if border:
        x0, y0 = (message_x - padding, message_y - padding)
        x1 = message_x + message_size[0] + padding
        y1 = message_y + message_size[1] + padding
        # 🖊️ draw box at position
        draw.rectangle([(x0, y0), (x1, y1)], outline='red')

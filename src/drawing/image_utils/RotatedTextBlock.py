from . import transparent
from PIL import Image, ImageDraw


class RotatedTextBlock:
    def __init__(self, text, font):
        self.text = text
        self.font = font

    def size(self):
        return self.font.get_size(self.text)

    def draw_on(self, draw, pos=(0, 0)):
        *_, text_width, text_height = self.font.getbbox(self.text)
        text_image = Image.new('RGBA', (text_width, text_height), transparent)
        text_image_draw = ImageDraw.Draw(text_image)
        text_image_draw.text((0, 0), self.text, 'black', self.font)
        rotated_text = text_image.rotate(270, expand=True)

        display_width, display_height = draw.im.size
        title_bottom_left = display_width - text_height - 2
        vertical_center = int((display_height - text_width) / 2)
        title_paste_pos = (title_bottom_left, vertical_center)
        draw._image.paste(rotated_text, title_paste_pos, rotated_text)
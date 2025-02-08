from .DrawText import DrawText


class TextBlock:
    def __init__(self, texts, align=None):
        self.texts = texts
        self.width = self.longest_line(texts)
        self.height = self.total_height(texts)
        self.align = align

    def total_height(self, texts):
        return sum(map(lambda row: max(map(DrawText.height, row)), texts))

    def longest_line(self, texts):
        return max(map(lambda row: sum(map(DrawText.width, row)), texts))

    def size(self):
        return (self.width, self.height)

    def draw_on(self, draw, pos=(0, 0)):
        pos = self.align(draw.im, self.size()) if self.align else pos
        last_y_pos = pos[1]
        for row in self.texts:
            self.draw_text_row(draw, pos[0], last_y_pos, row)
            last_y_pos += max(map(DrawText.height, row))

    def draw_text_row(self, draw, x_pos, y_pos, row):
        for text in row:
            text.draw_on(draw, (x_pos, y_pos))
            x_pos += DrawText.width(text)
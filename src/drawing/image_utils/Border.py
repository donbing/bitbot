class Border:
    def __init__(self, border_type):
        self.border_type = border_type

    def draw_on(self, draw, pos=(0, 0)):
        if self.border_type != 'none':
            draw.rectangle(Border.border_rect(draw), outline=self.border_type)

    def border_rect(draw):
        return [(0, 0), (draw.im.size[0] - 1, draw.im.size[1] - 1)]
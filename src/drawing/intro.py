from PIL import Image, ImageDraw
import time
from .image_utils.CenteredText import centered_text
from ..configuration.network_utils import wait_for_internet_connection
page1 = '''I'm Bitbot.

I can chart crypto and stock markets.

If you fancy a change,
I can also display pictures and other stuff.

I'll guide you through setup in a moment.'''

page2 = '''First, I need to connect to your WiFi.

From your phone or laptop,
sign-in to the Bitbot WiFi
and follow the instructions on-screen.

Once I have internet access,
I will load the next page...'''

page3 = '''Good job! I'm connected :D

To change my config,
visit 'http://bitbot:8080'
from any device in your network.

In 30 seconds time,
I'll show the Bitcoin chart for you
Have fun!'''

transparent = (255, 0, 0, 0)


def IntroPlayer(display, config):
    intro = Intro(display.size(), display.title_font, config)
    for image in intro.play():
        display.show(image)


class Intro:
    def __init__(self, size, font, config):
        self.display_size = size
        self.font = font
        self.centre = tuple(dim / 2 for dim in self.display_size)
        self.page_duration = 30
        self.intro_background = config.intro_background()

    def get_background(self):
        background = Image.open(self.intro_background)
        background = background.resize(self.display_size)
        return background

    def play(self):
        background = self.get_background()
        img = Image.new("RGBA", self.display_size, transparent)
        draw = ImageDraw.Draw(img)
        centered_text(draw, page1, self.font, img.size, 'topleft')
        background.paste(img, (0, 0), img)
        yield background

        background = self.get_background()
        time.sleep(self.page_duration)
        img = Image.new("RGBA", self.display_size, transparent)
        img.paste(background)
        draw = ImageDraw.Draw(img)
        centered_text(draw, page2, self.font, img.size, 'topleft')
        background.paste(img, (0, 0), img)
        yield background

        background = self.get_background()
        wait_for_internet_connection(self.no_op)
        img = Image.new("RGBA", self.display_size, transparent)
        img.paste(background)
        draw = ImageDraw.Draw(img)
        centered_text(draw, page3, self.font, img.size, 'topleft')
        background.paste(img, (0, 0), img)
        yield background

        time.sleep(self.page_duration)

    def no_op(self):
        pass

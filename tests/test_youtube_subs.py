import unittest
from src.display import title_font
from src.drawing.youtube_stats import subscriber_counter
from os.path import join as pjoin
import pathlib
from src.configuration.bitbot_files import use_config_dir
from src.configuration.bitbot_config import load_config_ini

curdir = pathlib.Path(__file__).parent.resolve()
files = use_config_dir(pjoin(curdir, "../"))
config = load_config_ini(files)

class DisplaySize():
    def __init__(self, size):
        self.size = size

@unittest.skip("needs youtube api key")
class YouTubeSubsTests(unittest.TestCase):
    display_size = DisplaySize((400, 300))

    def test_showing_youtube_subscriber_count(self):
        aubscriber_count_display = subscriber_counter.YouTubeSubscriberCount(self.display_size, title_font, config)
        image = aubscriber_count_display.play()
        image.save(f'tests/images/youtube_subs_count.png')

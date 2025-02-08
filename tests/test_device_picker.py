import unittest
from src.display.picker import picker, disk, inky, waveshare
from os.path import join as pjoin
import pathlib
from PIL import Image
from src.configuration.bitbot_files import use_config_dir
from src.configuration.bitbot_config import load_config_ini

curdir = pathlib.Path(__file__).parent.resolve()
files = use_config_dir(pjoin(curdir, "../"))
config = load_config_ini(files)


def get_device(display_output_name):
    config.set('display', 'output', display_output_name)
    return picker(config)


class TestDevicePicker(unittest.TestCase):
    def test_can_create_disker(self):
        device = get_device('disk')
        assert type(device) is disk.Disker, "should pick disk output"

    @unittest.skip("inky device must be connected")
    def test_can_create_inky(self):
        device = get_device('inky')
        assert type(device) is inky.Inker, "should pick inky output"

    @unittest.skip("waveshare device must be connected")
    def test_can_create_waveshare(self):
        device = get_device('waveshare.epd2in7b_V2')
        assert type(device) is waveshare.Waver, "should pick waveshare output"

    @unittest.skip("waveshare device must be connected")
    def test_draw_image_to_waveshare(self):
        device = get_device('waveshare.epd2in7b_V2')

        image = Image.open('tests/images/APPLE 1mo defaults.png')
        image = image.resize(device.size())
        image = image.convert('P', palette=Image.ADAPTIVE, colors=3)
        device.show(image)

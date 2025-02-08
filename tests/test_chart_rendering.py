import io
from PIL import Image, ImageChops
import pandas as pd
from src.configuration.bitbot_files import use_config_dir
from src.configuration.bitbot_config import load_config_ini
import os
import pathlib
import unittest

from src.drawing.market_charts.mpf_plotted_chart import MplFinanceChart
from src.exchanges.CandleData import CandleData

exchange_name = "coinbase"

# basic config
config_defaults = {
    'display': {
        'expanded_chart': 'false',
        'show_volume': 'false',
    }
}

class TestDisplay():
    def __init__(self, size, dpi):
        self.size1 = size
        self.dpi1 = dpi

    def size(self):
        return self.size1
    
    def dpi(self):
        return self.dpi1

test_data_path = "tests/data"
test_images_path = "tests/images"

class TestRenderingMeta(type):
    def __new__(mcs, name, bases, dict, chart_size):
        chart = configure_chart(chart_size)

        def gen_test(generatedTestName, data_file_name, this_tests_images_path):
            def test(self):
                test_image_file_path = f"{this_tests_images_path}/{generatedTestName}.png"
                chart_data = get_chart_data(data_file_name)

                previous_image = Image.open(test_image_file_path) if os.path.exists(test_image_file_path) else None

                with io.BytesIO() as file_stream:
                    chart.write_to_stream(file_stream, chart_data)
                    new_image = Image.open(file_stream)

                    assert_image_matches_size(new_image, chart_size)

                    changes = image_changes(previous_image, new_image, test_image_file_path)
                    new_image.save(test_image_file_path)
                    if changes:
                        # os.system("code '" + test_image_file_path + "'")
                        assert False, f"Image diff check: '{changes}'"

            return test

        for file_name in os.listdir(test_data_path):
            test_name = f"test_{file_name}".replace(".pkl","")
            this_tests_images_path=os.path.join(test_images_path, chart_size)
            os.makedirs(this_tests_images_path, exist_ok=True)
            dict[test_name] = gen_test(test_name, file_name, this_tests_images_path)

        return type.__new__(mcs, name, bases, dict)

def configure_chart(chart_size):
    curdir = pathlib.Path(__file__).parent.resolve()
    files = use_config_dir(os.path.join(curdir, "../"))
    config = load_config_ini(files)
    config.read_dict(config_defaults)
    config.config["display"]["resolution"] = chart_size
    chart = MplFinanceChart(config, TestDisplay(tuple(map(int, chart_size.split("x"))), 100), files)
    return chart


def get_chart_data(test_data_file_name):
    # yes, maybe pkl metadata somehow?
    source, dest, candle_width = test_data_file_name.replace(".pkl", "").split("_")
    price_history = pd.read_pickle(f"{test_data_path}/{test_data_file_name}")

    return CandleData(f"{source}/{dest}", candle_width, price_history)


def assert_image_matches_size(new_image, expected_res):
    actual_res = f"{new_image.width}x{new_image.height}"
    assert expected_res == actual_res, f"expected {expected_res}, was {actual_res}"


def image_changes(previous_image, new_image, file_name):
    if previous_image is None:
        return new_image
    
    diff = ImageChops.difference(new_image.convert('RGB'), previous_image.convert('RGB'))

    differenceImageBounds = diff.getbbox()
    if differenceImageBounds:
        dir, name, = os.path.split(file_name)
        fails_folder = os.path.join(dir, 'fail')
        os.makedirs(fails_folder, exist_ok=True)
        diff_file_path = os.path.join(fails_folder, name)

        threshold = 128
        diff = diff.point(lambda x: 0 if x < threshold else 255)
        diff.save(diff_file_path)

        return diff, diff_file_path


class SmallChartRenderingTests(unittest.TestCase, chart_size="264x176", metaclass=TestRenderingMeta):
    __metaclass__ = TestRenderingMeta


class MediumChartRenderingTests(unittest.TestCase, chart_size="400x300", metaclass=TestRenderingMeta):
    __metaclass__ = TestRenderingMeta


class LargeChartRenderingTests(unittest.TestCase, chart_size="640x448", metaclass=TestRenderingMeta):
    __metaclass__ = TestRenderingMeta


class ExtraLargeChartRenderingTests(unittest.TestCase, chart_size="800x480", metaclass=TestRenderingMeta):
    __metaclass__ = TestRenderingMeta

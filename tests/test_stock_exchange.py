import unittest
from src.configuration import bitbot_config, bitbot_files
from src.configuration.bitbot_files import use_config_dir
from src.configuration.bitbot_config import load_config_ini
from src.exchanges.stock_exchanges import Exchange, candle_configs
import os
import pathlib


# 🪳 ''1h',' <- fails on weekends due to short chart duration
test_params = ['1m', '5m', '30m', '1h', '1d', '1wk', '1mo', '3mo']

curdir = pathlib.Path(__file__).parent.resolve()
files = use_config_dir(os.path.join(curdir, ".."))
config_ini = load_config_ini(files)

class TestStockExchange(unittest.TestCase):
    def test_fetching_history(self):
        for candle_spec in test_params:
            with self.subTest(msg=candle_spec):
                self.run_test(candle_spec)

    def run_test(self, candle_width):
        stock = "TSLA"
        mock_config = {
                    "currency": {
                        "stock_symbol": stock
                    },
                    "display": {
                        "candle_width": candle_width,
                        "disk_file_name": "pictures/last_display.png"
                    }
                }
        exchange = Exchange()

        config = bitbot_config.BitBotConfig(mock_config, {})
        data = exchange.fetch_history(config)
        num_candles = len(data.candle_data)

        we_got_candles = num_candles > 0
        self.assertTrue(we_got_candles, msg=f'got {num_candles} candles for {stock}')

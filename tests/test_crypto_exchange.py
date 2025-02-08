import datetime
import os
import unittest

from src.exchanges import crypto_exchanges


os.makedirs('tests/data/', exist_ok=True)


# 📄 grabs data for the other tests to use
class TestFetcingPriceHistory(unittest.TestCase):
    
    # 🐌 ccxt does rate-limiting per-exchange
    coinbase = crypto_exchanges.Exchange("coinbase")
    cryptocom = crypto_exchanges.Exchange("cryptocom")
        
    def test_coinbase_btc(self):
        for candle_spec in self.coinbase.exchange.timeframes:
            with self.subTest(msg=candle_spec):
                check_price_history(candle_spec, self.coinbase, "BTC/USD")

    def test_coinbase_eth(self):
        for candle_spec in self.coinbase.exchange.timeframes:
            with self.subTest(msg=candle_spec):
                check_price_history(candle_spec, self.coinbase, "ETH/USD")
    
    def test_cryptocom_cro(self):
        for candle_spec in self.cryptocom.exchange.timeframes:
            with self.subTest(msg=candle_spec):
                check_price_history(candle_spec, self.cryptocom, "CRO/BTC")
    
    # dont write randomised data files to disk, the rendering tests get confused
    def test_random_timeframe(self):
        with self.subTest(msg="random"):
            check_price_history("random", self.cryptocom, "CRO/BTC")


def check_price_history(candle_width, exchange, instrument, store_candle_data=False):
    # ⬇️ fetch data from selected exchange
    expected_candle_count = 40
    start_time = datetime.datetime.strptime('2023-11-10T00:00', '%Y-%m-%dT%H:%M')
    data = exchange.fetch_history(
        candle_width, 
        instrument, 
        start_time,
        max_candles=expected_candle_count)
    
    # 💾 save the data for other tests
    if store_candle_data:
        instrument_name = instrument.replace("/", "_")
        data.candle_data.to_pickle(f"tests/data/{instrument_name}_{candle_width}.pkl")

    # 💪 assert we got the default number of candles
    num_candles = len(data.candle_data)
    we_got_candles = num_candles > 0 # we get < max candles for some larger timeframes
    assert we_got_candles, f'got {num_candles} candles for {instrument}, expected {expected_candle_count}'

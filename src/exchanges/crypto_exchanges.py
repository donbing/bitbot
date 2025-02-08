import ccxt
import random
import pandas as pd
import logging
from src.configuration.log_decorator import info_log
from ccxt.base.errors import BadSymbol
from src.exchanges.CandleData import CandleData

# 🪙 CCXT based crypto exchange client
class Exchange():
    def __init__(self, exchange_name):
        self.exchange = load_exchange(exchange_name)
        
    def fetch_history(self, candle_width, instrument, chart_since=None, max_candles=40):
        if(candle_width == "random"):
            random_index = random.randrange(len(self.exchange.timeframes))
            candle_width = list(self.exchange.timeframes.keys())[random_index]

        dirty_price_data = fetch_market_data(
            self.exchange,
            instrument,
            candle_width,
            max_candles,
            chart_since)
        
        candle_data = parse_to_dataframe(dirty_price_data)

        return CandleData(instrument, candle_width, candle_data)

    def __repr__(self):
        return '<ccxt crypto exchange>'


def parse_to_dataframe(candle_data):
    data_frame = pd.DataFrame(candle_data)
    data_frame.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    data_frame.index = pd.DatetimeIndex(data_frame['Date'], dtype="datetime64[ms]")
    return data_frame


@info_log
def fetch_market_data(exchange, instrument, candle_width, num_candles, since):
    try:
        return exchange.fetchOHLCV(
            instrument,
            candle_width,
            limit=num_candles,
            since=since and exchange.parse8601(since.strftime('%Y-%m-%dT%H:%M:%S.%f%z')))
    except BadSymbol:
        logging.warning(f'"{instrument}" is not available')
        return []


@info_log
def load_exchange(exchange_name):
    exchange = getattr(ccxt, exchange_name)({
        # 'apiKey': '<YOUR API KEY HERE>',
        # 'secret': '<YOUR API SECRET HERE>',
        'enableRateLimit': True,
    })
    exchange.loadMarkets()
    return exchange

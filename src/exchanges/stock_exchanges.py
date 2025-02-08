import yfinance
import collections
import random
from datetime import datetime, timedelta, timezone
from src.configuration.log_decorator import info_log
from src.exchanges.CandleData import CandleData


CandleConfig = collections.namedtuple('CandleConfig', 'width duration fat_duration')

candle_configs = [
    CandleConfig('1mo', timedelta(weeks=4*24), None),
    CandleConfig('1wk', timedelta(weeks=60), None),
    CandleConfig('3mo', timedelta(weeks=12*24), None),
    CandleConfig('1m', timedelta(minutes=60), timedelta(days=4)),
    CandleConfig('2m', timedelta(minutes=60), timedelta(days=4)),
    CandleConfig('5m', timedelta(minutes=60), timedelta(days=4)),
    CandleConfig('15m', timedelta(minutes=15*60), timedelta(days=4)),
    CandleConfig('30m', timedelta(minutes=30*40), timedelta(days=4)),
    CandleConfig('1h', timedelta(hours=40), timedelta(days=3)),
    CandleConfig('1d', timedelta(days=40), timedelta(days=3)),
]

# 🏦 yFinance based stocks api client
class Exchange():

    def __init__(self):
        self.name = 'yahoo finance'

    def fetch_history(self, config):
        instrument = config.stock_symbol()
        ticker = yfinance.Ticker(instrument)
        candle_config = self.select_candle_config(config)
        candle_width = candle_config.width
        chart_duration = candle_config.fat_duration or candle_config.duration

        start_date = config.chart_since() 
        if start_date is None or (start_date + chart_duration) > datetime.now(timezone.utc):
            start_date = datetime.utcnow() - chart_duration

        end_date = start_date + chart_duration

        history = self.get_stock_history(
            ticker,
            candle_width,
            start_date,
            end_date)
        instrument = ticker.info.setdefault('shortName', ticker.ticker)
        
        return CandleData(instrument, candle_width, self.parse_to_dataframe(history.tail(40)))

    def parse_to_dataframe(self, candle_data):
        candle_data = candle_data.drop(["Dividends", "Stock Splits"], axis=1)
        return candle_data

    @info_log
    def get_stock_history(self, ticker, candle_width, start_date, end_date):
        return ticker.history(
            interval=candle_width,
            start=start_date,
            end=end_date)

    def select_candle_config(self, config):
        candle_width = config.candle_width()
        if(candle_width == "random"):
            return self.get_random_candle_config()
        else:
            candle_config = self.get_candle_config_matching(candle_width)
            return candle_config

    def get_candle_config_matching(self, configred_candle_width):
        if configred_candle_width not in candle_configs:
            candle_config, = (
                    conf for conf in candle_configs
                    if conf.width == configred_candle_width
                )
            return candle_config

    def get_random_candle_config(self):
        randomised_index = random.randrange(len(candle_configs))
        new_var = candle_configs[randomised_index]
        return new_var

    def __repr__(self):
        return '<yfinance stock Exchange>'


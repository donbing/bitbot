class CandleData():
    def __init__(self, instrument, candle_width, candle_data):
        self.instrument = instrument
        self.candle_width = candle_width
        self.candle_data = candle_data

    def percentage_change(self):
        current_price = self.last_close()
        start_price = self.start_price()
        return ((current_price - start_price) / current_price) * 100 if start_price is not None else 0

    def last_close(self):
        lastClose = self.candle_data.at[self.candle_data.index[-1], 'Close']
        return lastClose

    def start_price(self):
        firstClose = self.candle_data.at[self.candle_data.index[0], 'Close']
        return float(firstClose)
    
    def price_change(self):
        return abs(self.start_price() - self.last_close())

    def __repr__(self):
        return f'<{self.instrument} {self.candle_width} candle data>'
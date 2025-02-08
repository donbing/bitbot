
from datetime import datetime
from PIL import ImageDraw
from src.configuration.log_decorator import info_log
from src.drawing.image_utils.DrawText import DrawText
from src.drawing.image_utils.TextBlock import TextBlock
from src.drawing.image_utils.Align import Align
from src.drawing.image_utils.RotatedTextBlock import RotatedTextBlock
from src.drawing.image_utils.Border import Border
from src.configuration.network_utils import get_ip
from src.drawing.market_charts.price_humaniser import human_format


class ChartOverlay():
    def __init__(self, config, display, chart_data):
        self.config = config
        self.display = display
        self.chart_data = chart_data
        self.title_font = self.display.title_font
        self.price_font = self.display.price_font
        self.medium_font = self.display.medium_font
        self.tiny_font = self.display.tiny_font

    @info_log
    def draw_on(self, chart_image):
        # 🖊️ handles drawing on top of our chart image
        draw_plot_image = ImageDraw.Draw(chart_image)
        # 🖊️ draw each of the configured display elements
        for elem in self.display_elements():
            elem.draw_on(draw_plot_image)

    def display_elements(self):
        # 🕒 add the time if configured
        if self.config.show_timestamp() == 'true':
            yield DrawText(self.format_time(), self.tiny_font, align=Align.BottomRight)
            
        # 📡 add the ip address if configured
        if self.config.show_ip() == 'true':
            yield DrawText(get_ip(), self.tiny_font, align=Align.BottomLeft)

        # 🔲 add a border if configured
        yield Border(self.config.border_type())

        # 🖊️ add configured overlay
        if self.config.overlay_type() == "2":
            for element in self.overlay2(self.chart_data):
                yield element
        if self.config.overlay_type() == "1":
            for element in self.overlay1(self.chart_data):
                yield element

    def overlay1(self, chartdata):
        portfolio_value = self.value_held(chartdata)
        portfolio_entry_value = self.entry_value()
        portfolio_pnl = self.profit(chartdata)
        yield TextBlock([
            [
                # 🎹 draw instrument name and candle width text
                DrawText(f'{chartdata.instrument} ({chartdata.candle_width}) ', self.title_font),
                # ➗ draw coloured change percentage
                DrawText.percentage(chartdata.percentage_change(), self.title_font),
            ],
            # 🐘 large font price text
            [DrawText.draw_string(human_format(chartdata.last_close(), ndigits=3), self.price_font)],
            # 💬 draw holdings or comment
            [
                DrawText.number(portfolio_pnl, self.title_font)
                if portfolio_value
                else DrawText.random_from_bool(self.ai_comments(), self.price_increasing(chartdata), self.title_font),

                DrawText.pip_calc(self.entry_price(), chartdata.last_close(), self.title_font, prefix=" ")
                if portfolio_entry_value != 0
                else DrawText.empty(self.title_font)
            ]
        ], align=Align.LeastIntrusive)

    def overlay2(self, chartdata):
        portfolio_value = self.value_held(chartdata)
        portfolio_entry_value = self.entry_value()
        portfolio_delta = self.profit(chartdata)
        # 🎹 draw instrument name
        yield RotatedTextBlock(chartdata.instrument, self.medium_font)
        # 🕎 candle width
        yield DrawText(chartdata.candle_width, self.medium_font, colour='red', align=Align.TopRight)
        # 🏳️ title block
        yield TextBlock([
            # ➗ draw coloured change percentage
            [DrawText.percentage(chartdata.percentage_change(), self.title_font)],
            # 🐘 large font price text
            [DrawText.draw_string(human_format(chartdata.last_close(), ndigits=3), self.price_font)],
            # 💬 draw holdings or comment
            [
                DrawText.draw_string(human_format(portfolio_value), self.title_font)
                if portfolio_value
                else DrawText.random_from_bool(self.ai_comments(), self.price_increasing(chartdata), self.title_font),

                DrawText.draw_string(human_format(portfolio_delta), self.title_font)
                if portfolio_entry_value != 0
                else DrawText.empty(self.title_font)
            ]
        ], align=Align.LeastIntrusive)

    def price_increasing(self, chartdata):
        return chartdata.start_price() < chartdata.last_close()

    def format_time(self):
        return datetime.now().strftime("%-H:%M%b%-d")

    def ai_comments(self):
        return self.config.get_price_action_comments()

    def value_held(self, market):
        return self.portfolio_size() * market.last_close()

    def portfolio_size(self):
        return self.config.portfolio_size()

    def entry_price(self):
        return self.config.entry_price()

    def entry_value(self):
        return self.entry_price() * self.portfolio_size()

    def profit(self, market):
        return self.value_held(market) - self.entry_value()

    def __repr__(self):
        return f'<Overlay: {self.config.overlay_type()}>'

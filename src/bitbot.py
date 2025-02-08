from PIL import Image, ImageDraw
from os.path import exists
import io

from matplotlib import font_manager
from src.drawing.market_charts.mpf_plotted_chart import MplFinanceChart
from src.exchanges import crypto_exchanges, stock_exchanges
from src.configuration.log_decorator import info_log
from src.configuration.network_utils import wait_for_internet_connection
from src.display.picker import picker as display_picker
from src.drawing.market_charts.chart_overlay import ChartOverlay
from src.drawing.youtube_stats.subscriber_counter import YouTubeSubscriberCount
from src.drawing.tide_times.tidal_graph import render_tide_chart
from src.drawing.image_utils.CenteredText import centered_text


class BitBot():
    def __init__(self, config, files):
        self.config = config
        self.files = files
        self.display = display_picker(config)
        self.chart = MplFinanceChart(self.config, self.display, self.files)

    # 🏛️ stock or crypto exchange
    def market_exchange(self):
        exchange_factory = stock_exchanges if self.config.stock_symbol() else crypto_exchanges
        return exchange_factory.Exchange(self.config.exchange_name())

    @info_log
    def display_chart(self):
        # 📡 await internet connection
        wait_for_internet_connection(self.display_connection_error)
        # 📈 fetch chart data
        market_exchange = self.market_exchange()
        chart_data = market_exchange.fetch_history(
            self.config.candle_width(),
            self.config.instrument_name(),
            self.config.chart_since())
        
        if(chart_data.candle_data.empty is False):
            # 🖊️ draw the chart on the display
            with io.BytesIO() as file_stream:
                # 🖊️ draw chart plot to image
                self.chart.write_to_stream(file_stream, chart_data)
                chart_image = Image.open(file_stream)
                # 🖊️ draw overlay on image
                overlay = ChartOverlay(self.config, self.display, chart_data)
                overlay.draw_on(chart_image)
                # 📺 display the image
                self.display.show(chart_image)
                return chart_image
        else:
            return self.display_message(f'{chart_data.instrument} ({chart_data.candle_width}) was not found on {market_exchange.name}')

    @info_log
    def display_message(self, message):  
        img = Image.new("P", self.display.size())
        draw = ImageDraw.Draw(img)
        centered_text(draw, message, self.display.title_font, self.display.size(), border=True)
        self.display.show(img)
        return img

    @info_log
    def cycle_chart(self):  
        self.config.cycle_instrument()
        self.display_chart()

    @info_log
    def display_photo(self):
        image_path = self.config.photo_image_file()
        if(exists(image_path)):
            self.display.show(Image.open(image_path))

    @info_log
    def display_youtube_subs(self):
        subscriber_display = YouTubeSubscriberCount(self.display.size(), self.display.title_font, self.config)
        subscriber_display.play()
        
    @info_log
    def display_tide_times(self):
        with io.BytesIO() as img_buf:
            img = render_tide_chart(self.config.tide_location_id(), img_buf)
            self.display.show(img)

    @info_log
    def display_connection_error(self):
        self.display_message("""
        NO INTERNET CONNECTION
        ----------------------------
        Please check your WIFI
        ----------------------------
        To configure WiFi access,
        connect to 'bitbot-<nnn>' WiFi AP
        and follow the instructions""")

    def __repr__(self):
        return f'<BitBot output: {str(self.config.output_device_name())}>'

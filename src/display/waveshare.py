import threading

from src.configuration.log_decorator import info_log
from . import DisplayBase
import time


# 🌊 supports waveshare EPDs
class Waver(DisplayBase):
    def __init__(self, device_name, config):
        device_class = self.load_device_class(device_name)
        self.display = device_class()
        self.device_name = device_name
        self.lock = threading.Lock()
        self.config = config
        self.set_fonts()

    def load_device_class(self, device_name):
        waveshare_module = __import__('waveshare_epd.' + device_name)
        device_class = getattr(waveshare_module, device_name).EPD
        return device_class

    def _size(self):
        return (self.display.width, self.display.height)

    # 📺 show the image
    @info_log
    def show(self, image):
        image = self.apply_rotation(image)
        image = image.convert('P')
        image = self.resize_image(image)

        # create a bw image from our source
        black_image = image.copy()
        black_image.putpalette((255, 255, 255, 0, 0, 0))

        # create an image for the red colour channel
        color_image = image.copy()
        color_image.putpalette((255, 255, 255, 255, 255, 255, 0, 0, 0) + (255, 255, 255)*253)

        
        self.lock.acquire()
        
        epd = self.display
        try:
            epd.init()
            epd.Clear()
            time.sleep(1)
            epd.display(epd.getbuffer(black_image), epd.getbuffer(color_image))
            epd.sleep()
        finally:
            self.lock.release()
        
    def __repr__(self):
        return f'<{self.device_name}: @{self.size()}>'

from . import quantise_image, white_black_red, DisplayBase
import threading
from ..configuration.log_decorator import info_log
from inky.auto import auto


# 🦑 supports Pimoroni Inky EPDs
class Inker(DisplayBase):
    def __init__(self, device_name, config):
        self.device_name = device_name
        self.lock = threading.Lock()
        self.config = config
        self.display = auto()
        self.set_fonts()

    def _size(self):
        return self.display.resolution
    
    @info_log
    def show(self, image):
        if self.config.display_border_colour():
            match self.config.display_border_colour():
                case "white":              
                    self.display.set_border(self.display.WHITE)  
                case "black":      
                    self.display.set_border(self.display.BLACK)
            
        # 🌀 rotate/resize the image
        image = self.apply_rotation(image)
        image = self.resize_image(image)

        # 🎨 apply colour palette
        if self.display.colour in ["yellow", "red", 'black']:
            image = quantise_image(image, white_black_red)

        self.lock.acquire()
        # 📺 show the image
        self.display.set_image(image)
        try:
            self.display.show()
        finally:
            self.lock.release()
            
        image.save(self.config.output_file_name())

    def __repr__(self):
        return f'<Inky {self.display.colour}: @{self.size()}>'

from PIL import Image, ImageDraw
from ..image_utils.CenteredText import centered_text
from ...configuration.network_utils import wait_for_internet_connection
import json
import requests

transparent = (255, 0, 0, 0)

class YouTubeSubscriberCount:
    def __init__(self, size, font, config):
        self.config = config
        self.display_size = size
        self.font = font
        self.centre = tuple(dim / 2 for dim in self.display_size.size)

    def play(self):
        channel_id=self.config.youtube_channelid()
        your_key=self.config.youtube_key()
        url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={your_key}"
        http_response = requests.get(url)
        response_json = json.loads(http_response.text)
        subscriber_count = response_json['items'][0]['statistics']['subscriberCount']
        text_to_draw = f"{subscriber_count} Subscribers"
        img = Image.new("RGBA", self.display_size.size, transparent)
        draw = ImageDraw.Draw(img)
        centered_text(draw, text_to_draw, self.font, self.display_size, 'centre')
        return img
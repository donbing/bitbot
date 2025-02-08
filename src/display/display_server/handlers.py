from inky.auto import auto
from http.server import BaseHTTPRequestHandler
from PIL import Image
import io
import cgi
import json


# 🎨 create a limited pallete image for converting our chart image
def quantise_inky(display_image):
    palette_img = Image.new("P", (1, 1))
    white_black_red = (255, 255, 255, 0, 0, 0, 255, 0, 0)
    palette_img.putpalette(white_black_red + (0, 0, 0) * 252)
    return display_image.convert('RGB').quantize(palette=palette_img)


def unsupported_media_type(handler, content_type_header):
    handler.wfile.write(bytes(content_type_header, "utf8"))
    handler.send_response(415)
    handler.end_headers()


# 🤔 gets json describing the currently connected display
def get_json(handler):
    inky_display = auto()
    handler.send_response(200)
    handler.send_header('Content-Type', 'application/json')
    handler.end_headers()
    json_str = json.dumps({
        "type": inky_display.colour,
        "width": inky_display.WIDTH,
        "height": inky_display.height,
        "uploadLink": handler.path,
    })
    handler.wfile.write(json_str.encode(encoding='utf_8'))

# 🖼️ gets an html form to upload images for display
def get_html(handler):
    html = '''
        <form method='post' enctype='multipart/form-data'>
            <input type='file' name='image_file'/>
            <input type='submit'>
        </form>'''

    handler.send_response(200)
    handler.send_header("Content-type", "text/html; charset=utf-8")
    handler.send_header("Content-Length", str(len(html)))
    handler.end_headers()
    handler.wfile.write(bytes(html, "utf8"))

# 📺 Shows the uploaded image on whatever display is being used
def display_uploaded_image(handler):
    content_type, pdict = cgi.parse_header(handler.headers['content-type'])

    # boundary data needs to be encoded in a binary format
    pdict['boundary'] = bytes(pdict['boundary'], "utf-8")

    if(content_type == 'multipart/form-data'):
        inky_display = auto()
        fields = cgi.parse_multipart(handler.rfile, pdict)
        image = Image.open(io.BytesIO(fields['image_file'][0]), mode='r')
        image = image.resize((inky_display.WIDTH, inky_display.HEIGHT))
        inky_display.set_image(quantise_inky(image))
        inky_display.show()
        handler.send_response(200)
    else:
        unsupported_media_type(handler)


class InkyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        content_type_header = self.headers.get('accept')
        if('application/json' in content_type_header):
            get_json(self)
        elif('text/html' in content_type_header):
            get_html(self)
        else:
            unsupported_media_type(self, content_type_header)

    def do_POST(self):
        display_uploaded_image(self)

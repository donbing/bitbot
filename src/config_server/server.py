import io
import mimetypes
import os
import pathlib
import time
import uuid
from src.configuration.bitbot_files import BitBotFiles
from src.configuration.bitbot_config import load_config_ini
from flask import Flask, jsonify, render_template, request, redirect, send_from_directory, url_for
from PIL import Image
import ccxt

app = Flask(__name__)

# 🗂️ load up app config
base_dir = os.path.join(pathlib.Path(__file__).parent.resolve(), '../../')
files_config = BitBotFiles(base_dir)
app_config = load_config_ini(files_config)

# 🗂️ list style and config files
style_files = files_config.files_ending_with("mplstyle")
ini_files = files_config.files_ending_with("ini")


# ⚙️ config index page
@app.route('/')
def index():
    return render_template(
        'index.html',
        style_files=style_files,
        ini_files=ini_files,
        config=app_config)

@app.route('/pictures/<filename>', methods=['GET'])
def last_image(filename):
    return send_from_directory(os.path.join(base_dir, 'pictures'), filename, mimetype="imagee/png")

# ⚙️ user-friendly config.ini editor
@app.route('/configure', methods=['POST', 'GET'])
def configure():
    if request.method == 'GET':
        exchange = create_exchange(app_config.exchange_name())
        exchanges = ccxt.exchanges
        return render_template(
            'config.html',
            config=app_config,
            exchanges=exchanges,
            markets=exchange.load_markets()
        )
    else:
        app_config.set_currency(request.form)
        app_config.set_display(request.form)
        return '200 OK'


# 📝 read/write to config files
@app.route('/file/<file>', methods=['POST', 'GET'])
def file(file):
    if request.method == 'POST':
        file_path = files_config.all_files.get(file)
        with open(file_path, 'w') as fh:
            fh.write(request.form['file'])
        return redirect(request.url)
    else:
        file_path = files_config.all_files.get(file)
        with open(file_path) as fh:
            return render_template('file.html', file=fh.read(), file_name=file)


# 🖼️ confiure picture frame mode settings
@app.route('/modes/picture', methods=['POST'])
def picture_mode():
    photo_mode_state = request.form.get('enable_picture_mode') or 'false'
    cycle_pictures = request.form.get('cycle_pictures') or 'false'
    app_config.toggle_photo_mode(photo_mode_state, cycle_pictures)
    image_file = request.files['image_file']
    if(photo_mode_state == 'true' and image_file):
        picture = Image.open(io.BytesIO(image_file.read()), mode='r')
        picture_file = app_config.set_photo_image_file(uuid.uuid4().hex)
        picture.save(picture_file, format="png")
    app_config.save()
    return redirect(url_for('index'))


# 🌳 stream log file output
@app.route('/logs')
def logs():
    def generate():
        with open(files_config.log_file_path, 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    time.sleep(1)
                    continue

                yield line

    return app.response_class(generate(), mimetype='text/plain')


def create_exchange(exchange_name):
    exchange = getattr(ccxt, exchange_name)()
    exchange.loadMarkets()
    return exchange


def get_market(exchange_name, market_id):
    exchange = create_exchange(exchange_name)
    markets = {
        key: value
        for (key, value) in exchange.markets.items()
        if market_id in key.lower() and value['active']
    }
    print(markets)
    return exchange, markets


# 🏛️ search for crypto exchange by name
@app.route('/exchanges/search')
def exchange_search():
    filtered = filter(lambda e: request.args['q'] in e.lower(), ccxt.exchanges)
    return jsonify(list(filtered)), '200 OK'


# 🎺 search exchanges instruments
@app.route('/exchanges/<exchange>/markets')
def instrument_search(exchange):
    exchange, instruments = get_market(exchange, request.args['q'])
    return jsonify(list(instruments.keys())), '200 OK'

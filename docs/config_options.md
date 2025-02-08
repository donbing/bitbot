# ⚙️ Configuration file options
Config options can be found in [config/config.ini](config/config.ini), there are 5 headings in the file.

## `[currency]`
 - `exchange`: the exchange to read prices from, see [CCXT](https://github.com/ccxt/ccxt/wiki/Exchange-Markets).
 - `instrument`: name of the market to track.
 - `stock_symbol`: overrides the instrument and tracks stock symbols instead.
 - `holdings`: track the total value of your investment be entering how much you own.
 - `currencies`: comma separated list of currencies to cycle between
 
## `[display]`
 - `rotation`: rotate the display (had bugs on inky).
 - `refresh_time_minutes`: wait time between display updates.
 - `output`: the display to output to, supports `disk`, `inky` and [`waveshare.{drivername}`](https://github.com/waveshare/e-Paper/tree/master/RaspberryPi_JetsonNano/python/lib/waveshare_epd).
 - `disk_file_name`: where to write files to if 'disk' is selected as output.
 - `overlay_layout`: select from the 2 available overlay layouts, supports `1` or `2` as value.
 - `expanded_chart`: tries to make use of the full screen by expanding the axis lines to the edge of the display.
 - `border`: adds a small timestamp to the bottom right corner, handy.
 - `show_volume`: adds trading volume cars to the bottom of the chart.
 - `candle_width`: manually specify the chanrt timeframe, supports `random`, `5m`, `15m`, `1h`, `4h` etc.
 - `show_ip`: shows small ip address in the bottom left.
 - `dpi`: dpi of the display
 
## `[picture_frame_mode]`
 - `enabled`: enable or disable picture mode.
 
## `[youtube_subs]`
 - `enabled`: enable or disable youtube subscriber count mode.
 - `account_id`: account Id
 - `key`: google developers API key with TY enabled

## `[tide_times_mode]`
 - `enabled`: enable or disable tide times mode.
 - `location_id`: id of the location to be trackes

## `[comments]`
 - `up`: comma separated list of `up` comments, will be chosen from randomly.
 - `down`: comma separated list of `down` comments, will be chosen from randomly.

## `[first_run]`
 - `enabled`: tracks displaying the intro pages the first time that Bitbot runs.
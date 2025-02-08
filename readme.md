# 🤖 **BitBot**
> A Raspberry Pi powered e-ink price chart and photo display
<div>
    <img height="100" src="docs/images/last_display.png">
    <img height="100" src="docs/images/kilobitbot-v2.jpg">
</div>

![lint and test](https://github.com/donbing/bitbot/actions/workflows/lint-and-test-python.yml/badge.svg)
![docker image](https://github.com/donbing/bitbot/actions/workflows/build-and-push-image.yaml/badge.svg)

# ✨ Features
 - ⚙️ `Config webserver` running on port **8080** allows easy configuration
 - 🏦 Capable of charting `stocks` and `crypto-currency` from **many different exchanges**
 - 🖼️ `Picture-frame` mode allows any image to be easily ***uploaded for display.***
 - 🆘 A `friendly intro` sequence will guide you through **setup**
 - 💲 Large `current price` header (**avoids chart overlap**) 
 - 🎲 Randomly selected `time frames`, or configured to **your preference**
 - 💰 Tracks the total `value of your holdings` 
 - 📈 Shows instrument details (e,g, ```(XBT/USD, +12%)```)
 - 📊 Optional `volume chart`
 - 💬 Displays configurable `AI commentry` depending on **price action**
 - 📡 `Warns` on **connection errors**
 - ♻️ Display `refreshes` **after config changes** 
 - 👶 Support `2.7"` displays
 - 📺 Support `waveshare` displays
 - 👆 **Inky Impression** `buttons` (cycle currency, change view, show volume, toggle photo-mode)
 
# 💡 Queued Features
 - 💸 Display **Transaction fees**
 - 👆 `Configurable` and/or `state based` **button actions**

# 📝 Docs
 - [🔗 Device **Assembly**](docs/device_assembly.md)
 - [💻 How To **Install**](docs/app_install.md)
 - [⚙️ Device **Setup**](docs/device_setup.md)
 - [💾 **Config** Options](docs/config_options.md)
 - [📒 Dev **Notes**](docs/development.md)
 - [📈 Chart examples](/tests/images/)

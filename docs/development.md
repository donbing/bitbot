# Development
> Bitbot is somewhat cobbled together, but is fairly carefully commented and has been factored with ease of change in mind.  

## ✔️ Tests 
[python unit tests](/tests) with the default test framework  
`python3 -m unittest discover tests -v`

## ✉️ Env vars 
`BITBOT_TESTRUN` loads one chart and then exits  
`BITBOT_SHOWIMAGE` [opens the image in vscode](/run.py) after loading the chart  
`BITBOT_OUTPUT` may be set to `disk` to write to disk rather than the e-ink display  
`export BITBOT_TESTRUN=true BITBOT_OUTPUT=disk BITBOT_SHOWIMAGE=true`

## 📻 Easy WiFi config 
[`comitup`](https://github.com/davesteele/comitup) is used for the ***disk image***, it creates a **config hotspot** on the Pi if it **cant connect** to any wifi itself.  
The config file is located at `/etc/comitup.conf`
```sh
# show comitup info
sudo comitup -i
# open cli (easy to delete connections here)
sudo comitup-cli
```

## 🌳Logging 
BitBot will log to the `config web-ui` `syslog`, `StdOut` and a rolling `logs/debug.log` file, configured in [📁logging.ini](/logging.ini)  
Log level is **defaulted to `INFO`**, but there is some ***limited debug level logging*** if you wish to get more info.  
Cron jobs were configured to output to syslog. 😞
```sh
# roling file log
tail ~/bitbot/debug.log
# follow syslog
tail -f /var/log/syslog | grep 'Bitbot:'
```

## 🎁 Packages 
UML diagram of broad [package interactions](http://www.plantuml.com/plantuml/svg/3Oon3KCX30NxFqMo0EvJ_LN0M7mhO11-LjOFrUckkDkHDsBqwwt6FQh4xgy7MFuXslcNckA94YwRfq4CYUUWEgseDIgACa4Zgvt6JcT5A_CtD_6qZbstM3ty0m00)  

 - [Pimoroni](pimoroni.com) [`inky`](https://github.com/pimoroni/inky) does the **e-ink display**, 
 - [`CCXT`](https://github.com/ccxt/ccxt) talks to **crypto exchanges**
 - [`MPL-Finance`](https://github.com/matplotlib/mpl-finance) **draws the graphs** (and could do with updating to [`mplfinance`](https://github.com/matplotlib/mplfinance))
 - [`Pillow`](https://github.com/python-pillow/Pillow) draws **drawing overlay** text onto the graph

## 🐳 Docker 
**Github actions** builds and tests and publishes a **container image** on each commit to `main` and `release`  

🐳 `x86` faster than the Pi.
```sh
# use an arm emulator to set platform for testing
docker run -e --privileged --rm -it --platform linux/arm/v7 --env BITBOT_TESTRUN=true --env BITBOT_OUTPUT=disk bitbot
# remove the `--platform` args if building on a pi 
docker buildx build --platform linux/arm/v7 . -t bitbot -f bitbot.dockerfile
```
🐳 Run **Priviledged access** is needed for `GPIO`, this looks to be fixable thru bind mounts.
```sh
docker run --privileged --platform linux/arm/v7 bitbot
```
🎼 Docker compose 
```sh
docker compose up -d --build
```
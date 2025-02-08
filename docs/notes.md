todo:
 - ## formatters
  y axis eng formatter precision needs to be calculated (fixed 2dp atm)


 - ## layout 
   * fix expanded mode 
   - fit candle count to screen size
   - keep an eye on the overlay least intrusive position algo, seems to be flaky
    - is flaky, whitespace check needs to be improved

 - ## multi-currency support
   - button to toggle between curencies
   - multi-plot display 
   - overlapping coloured multi-coin charts

 - ## impression:
    - better button actions!
     - make these state-based, so photo mode behaves different to chart mode
    - larger intro font
    - larger label fonts
    - config candle colours
    - config volume colours

 - ## config server
    - allow selecting style in config

 - ## general
    - on-screen assembly instructions
    - moving averages
    - indicators
    - multi instrument graphs

# Docker
Build arm6 on x86
```bash
# install QEMU and register the executable types on the host
docker run --privileged --rm tonistiigi/binfmt --install all
# Build arm7 on x86
docker run -e QEMU_CPU=arm1176 --privileged --rm -it --platform linux/arm/v7 balenalib/raspberry-pi:buster bash
# build container arm6
docker buildx build --platform linux/arm64 . -t bitbot --progress string
# run it, have to specify which chip QEMU should emulate
docker run -e QEMU_CPU=arm1176 --privileged --rm -t --platform linux/arm/v navikey/raspbian-buster:latest bash

docker buildx build --platform linux/arm/v7 . -t bitbot -f scripts/docker/dockerfile --progress string
docker run -e QEMU_CPU=arm1176 --privileged --rm -it --platform linux/arm/v7 bitbot
```

# Hackery
```bash
# remove all containers
docker container rm $(docker container ls -q -a)
#' which cpus to use for the build 
# --cpuset-cpus=0-3'

# error: failed to solve: failed to solve with frontend dockerfile.v0: failed to create LLB definition: rpc error: code = Unknown desc = error getting credentials - err: exit status 255, out: ``
= In ~/.docker/config.json `change credsStore to credStore`

# error exec "--env" "executable file not found in $PATH: unknown"
= badly ordered docker args, envs must come before image name
```

# Testing
```bash
# test run 
docker run --rm --env BITBOT_TESTRUN=true --env BITBOT_OUTPUT=disk --env BITBOT_SHOWIMAGE=false  bb

# run tests
docker run --rm \
--name bitbot_tests \
--env BITBOT_TESTRUN=true --env BITBOT_OUTPUT=disk --env BITBOT_SHOWIMAGE=false \
--mount type=bind,source="$(pwd)",target=/code/tests/images \
bb \
python3 -m unittest discover
```

# PiOS
```sh
# Get linux os version
cat /etc/os-release
# Enable vnc raspiconfig
sudo raspi-config nonint do_vnc 0
# Check cpu arch 
dpkg --print-architecture
```

# Git
Setup my git
```sh
# setup user
git config --global user.email ccbing@gmail.com
git config --global user.name donbing
# tell git to cache creds after first auth
git config --global credential.helper store
# remove creds
git config --global --unset user.password
# aliases
 git config --global alias.co checkout
 git config --global alias.br branch
 git config --global alias.ci commit
 git config --global alias.st status
```

# Fonts
- place in `~/.fonts` or `/usr/local/share/fonts` for system wide access  
- `mkdir ~/.fonts && cp ~/bitbot/src/resources/04B_03__.TTF ~/.fonts/04B_03__.TTF`
- manually rebuild the font cache with `fc-cache -f -v`
- list fonts with `fc-list`

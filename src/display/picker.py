from . import disk, inky, waveshare


# ✒️ selects EPD display or file output
def picker(config):
    # todo: name classes to match config values
    typeMap = {
            'disk': disk.Disker,
            'inky': inky.Inker,
            'waveshare': waveshare.Waver
        }
    output_device = config.output_device_name()
    manufacturer, device_name, *_ = output_device.split('.') + [None]
    return typeMap[manufacturer](device_name, config)

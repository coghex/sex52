import evdev
from x52_driver import X52Driver

device = evdev.InputDevice('/dev/input/event25')
dev    = X52Driver.find_supported_devices()[0]

#print(device.capabilities(verbose=True))
#print(device.input_props(verbose=True))

for event in device.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        try:
            print(event.code)
        except KeyError:
            print("keyerror")

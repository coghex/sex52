import evdev

device = evdev.InputDevice('/dev/input/event6')

#print(device.capabilities(verbose=True))
#print(device.input_props(verbose=True))

for event in device.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        try:
            print(evdev.categorize(event))
        except KeyError:
            print("keyerror")

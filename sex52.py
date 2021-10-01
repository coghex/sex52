import evdev
from x52_driver import X52Driver, X52ProEvdevKeyMapping, X52MfdLine, X52ColoredLedStatus

device = evdev.InputDevice('/dev/input/by-id/usb-Logitech_X52_Professional_H.O.T.A.S.-event-joystick')
dev    = X52Driver.find_supported_devices()[0]

#print(device.capabilities(verbose=True))
#print(device.input_props(verbose=True))

for event in device.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        if (event.code == X52ProEvdevKeyMapping.FIRE_C):
            if (event.value == evdev.events.KeyEvent.key_down):
                dev.set_mfd_text(X52MfdLine.LINE2,"blop blop")
        if (event.code == X52ProEvdevKeyMapping.FIRE_A):
            if (event.value == evdev.events.KeyEvent.key_down):
                dev.set_led_a(X52ColoredLedStatus.RED)
            if (event.value == evdev.events.KeyEvent.key_up):
                dev.set_led_a(X52ColoredLedStatus.GREEN)
#        try:
#            print(event.code)
#        except KeyError:
#            print("keyerror")

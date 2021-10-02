import evdev
from x52_driver import X52Driver, X52ProEvdevKeyMapping, X52MfdLine, X52ColoredLedStatus

def eventLEDButton(dev, code, val):
    if (val == evdev.events.KeyEvent.key_down):
        if (code == X52ProEvdevKeyMapping.TOGGLE_2) or (code == X52ProEvdevKeyMapping.TOGGLE_4) or (code == X52ProEvdevKeyMapping.TOGGLE_6):
            dev.set_led(code,X52ColoredLedStatus.GREEN)
        else:
            dev.set_led(code,X52ColoredLedStatus.RED)
    if (val == evdev.events.KeyEvent.key_up):
        if (code == X52ProEvdevKeyMapping.TOGGLE_1) or (code == X52ProEvdevKeyMapping.TOGGLE_2) or (code == X52ProEvdevKeyMapping.TOGGLE_3) or (code == X52ProEvdevKeyMapping.TOGGLE_4) or (code == X52ProEvdevKeyMapping.TOGGLE_5) or (code == X52ProEvdevKeyMapping.TOGGLE_6):
            dev.set_led(code,X52ColoredLedStatus.AMBER)
        else:
            dev.set_led(code,X52ColoredLedStatus.GREEN)

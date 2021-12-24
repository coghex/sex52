import os
import evdev
import signal
import json
import time
import cargo
import nav
import inp
import journal
from x52_driver import X52Driver, X52ProEvdevKeyMapping, X52MfdLine, X52ColoredLedStatus
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def main():
    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            inp.eventLEDButton(dev, event.code, event.value)

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
        elif event.event_type == 'modified':
            path = event.src_path
            fn   = os.path.basename(path)
            if (fn == "Cargo.json"):
                cargo.handleCargo(path,dev)
            elif (fn == "NavRoute.json"):
                nav.handleNav(path,dev)
            else:
                journ = journal.getCurrentJournal(os.path.dirname(path))
                if (fn == (journ + ".01.log")):
                    journal.handleJournal(path,dev)

def init(dev):
    dev.set_mfd_brightness(32)
    line1 = "----sex52.py----"
    line2 = "   loaded...:   "
    line3 = ">elite dangerous"
    dev.set_mfd_text(X52MfdLine.LINE1,line1)
    dev.set_mfd_text(X52MfdLine.LINE2,line2)
    dev.set_mfd_text(X52MfdLine.LINE3,line3)
    dev.set_led(X52ProEvdevKeyMapping.FIRE_A,X52ColoredLedStatus.GREEN)
    dev.set_led(X52ProEvdevKeyMapping.FIRE_B,X52ColoredLedStatus.GREEN)
    dev.set_led(X52ProEvdevKeyMapping.FIRE_D,X52ColoredLedStatus.GREEN)
    dev.set_led(X52ProEvdevKeyMapping.FIRE_E,X52ColoredLedStatus.GREEN)
    dev.set_led(X52ProEvdevKeyMapping.FIRE_I,X52ColoredLedStatus.GREEN)
    dev.set_led(X52ProEvdevKeyMapping.POV_2_UP,X52ColoredLedStatus.GREEN)
    dev.set_led(X52ProEvdevKeyMapping.TOGGLE_1,X52ColoredLedStatus.AMBER)
    dev.set_led(X52ProEvdevKeyMapping.TOGGLE_2,X52ColoredLedStatus.AMBER)
    dev.set_led(X52ProEvdevKeyMapping.TOGGLE_3,X52ColoredLedStatus.AMBER)
    print("init")

def sigInt(sig_in,frame):
    fin()

def fin():
    print("bye...")
    observer.stop()
    device.close()
    exit(0)

if __name__ == "__main__":
    try:
        device = evdev.InputDevice('/dev/input/by-id/usb-Logitech_X52_Professional_H.O.T.A.S.-event-joystick')
        dev    = X52Driver.find_supported_devices()[0]
    except:
        print("no controller detected...")
        exit(0)
    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, "/home/" + os.getlogin() + "/.steam/steam/steamapps/compatdata/359320/pfx/drive_c/users/steamuser/Saved Games/Frontier Developments/Elite Dangerous/", recursive=True)
    observer.start()
    signal.signal(signal.SIGINT, sigInt)
    init(dev)
    while True:
        main()
    observer.join()

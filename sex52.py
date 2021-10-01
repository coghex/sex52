import evdev
import signal
import json
from x52_driver import X52Driver, X52ProEvdevKeyMapping, X52MfdLine, X52ColoredLedStatus
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def main():
        for event in device.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                if (event.code == X52ProEvdevKeyMapping.FIRE_C):
                    if (event.value == evdev.events.KeyEvent.key_down):
                        dev.set_mfd_text(X52MfdLine.LINE2,"blop blop")
                eventLEDButton(dev, event.code, event.value)
#                try:
#                    print(event.code)
#                except KeyError:
#                    print("keyerror")

def eventLEDButton(dev, code, val):
    if (val == evdev.events.KeyEvent.key_down):
        dev.set_led(code,X52ColoredLedStatus.RED)
    if (val == evdev.events.KeyEvent.key_up):
        dev.set_led(code,X52ColoredLedStatus.GREEN)

device = evdev.InputDevice('/dev/input/by-id/usb-Logitech_X52_Professional_H.O.T.A.S.-event-joystick')
dev    = X52Driver.find_supported_devices()[0]
#print(device.capabilities(verbose=True))
#print(device.input_props(verbose=True))

def sigInt(sig_in,frame):
    print("bye...")
    observer.stop()
    device.close()
    exit(0)

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
        elif event.event_type == 'modified':
            f = open(event.src_path,)
            data = json.load(f)
            f.close()
            print("cargo: ")
            for n,item in enumerate(data["Inventory"]):
                print(item["Name"], ": ", item["Count"])
           
if __name__ == "__main__":
    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, "/home/coghex/.steam/steam/steamapps/compatdata/359320/pfx/drive_c/users/steamuser/Saved Games/Frontier Developments/Elite Dangerous/Cargo.json", recursive=True)
    observer.start()
    signal.signal(signal.SIGINT, sigInt)
    try:
        main()
    except:
        print("error")
        observer.stop()
        device.close()
        exit(0)
    observer.join()

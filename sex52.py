import evdev
import signal
import json
from x52_driver import X52Driver, X52ProEvdevKeyMapping, X52MfdLine, X52ColoredLedStatus
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def main():
        for event in device.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                #if (event.code == X52ProEvdevKeyMapping.FIRE_C):
                #    if (event.value == evdev.events.KeyEvent.key_down):
                #        dev.set_mfd_text(X52MfdLine.LINE2,"blop blop")
                eventLEDButton(dev, event.code, event.value)
#                try:
#                    print(event.code)
#                except KeyError:
#                    print("keyerror")

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

device = evdev.InputDevice('/dev/input/by-id/usb-Logitech_X52_Professional_H.O.T.A.S.-event-joystick')
dev    = X52Driver.find_supported_devices()[0]
#print(device.capabilities(verbose=True))
#print(device.input_props(verbose=True))

def sigInt(sig_in,frame):
    print("bye...")
    observer.stop()
    device.close()
    exit(0)

def extract_count(json):
    try:
        return int(json["Count"])
    except KeyError:
        return 0

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
        elif event.event_type == 'modified':
            f = open(event.src_path,)
            try:
                data = json.load(f)
                f.close()
            except:
                f.close()
                return()
            #for n,item in enumerate(data["Inventory"]):
            #    print(item["Name"], ": ", item["Count"])
            if (len(data["Inventory"]) == 0):
                line1 = "no cargo"
                line2 = " "
                line3 = " "
                dev.set_mfd_text(X52MfdLine.LINE1,line1)
                dev.set_mfd_text(X52MfdLine.LINE2,line2)
                dev.set_mfd_text(X52MfdLine.LINE3,line3)
                return ()
            print("cargo: ")
            data["Inventory"].sort(key=extract_count,reverse=True)
            name1 = data["Inventory"][0]["Name"]
            count1 = str(data["Inventory"][0]["Count"])
            if len(name1) > (14 - len(count1)):
                name1 = name1[0:(14 - len(count1))]
            elif (len(data["Inventory"]) == 1):
                line1 = "cargo:"
                line2 = name1 + ": " + count1
                line3 = " "
                dev.set_mfd_text(X52MfdLine.LINE1,line1)
                dev.set_mfd_text(X52MfdLine.LINE2,line2)
                dev.set_mfd_text(X52MfdLine.LINE3,line3)
                return ()
            name2 = data["Inventory"][1]["Name"]
            count2 = str(data["Inventory"][1]["Count"])
            if len(name2) > (14 - len(count2)):
                name2 = name2[0:(14 - len(count2))]
            elif (len(data["Inventory"]) == 2):
                line1 = "cargo:"
                line2 = name1 + ": " + count1
                line3 = name2 + ": " + count2
                dev.set_mfd_text(X52MfdLine.LINE1,line1)
                dev.set_mfd_text(X52MfdLine.LINE2,line2)
                dev.set_mfd_text(X52MfdLine.LINE3,line3)
                return ()
            name3 = data["Inventory"][2]["Name"]
            count3 = str(data["Inventory"][2]["Count"])
            if len(name3) > (14 - len(count3)):
                name3 = name3[0:(14 - len(count3))]
            else:
                line1 = name1 + ": " + count1
                line2 = name2 + ": " + count2
                line3 = name3 + ": " + count3
                dev.set_mfd_text(X52MfdLine.LINE1,line1)
                dev.set_mfd_text(X52MfdLine.LINE2,line2)
                dev.set_mfd_text(X52MfdLine.LINE3,line3)
                return ()

def init():
    dev.set_mfd_brightness(32)
    line1 = "    sex52.py    "
    line2 = "    --------    "
    line3 = ">loaded: elite d"
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
           
if __name__ == "__main__":
    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, "/home/coghex/.steam/steam/steamapps/compatdata/359320/pfx/drive_c/users/steamuser/Saved Games/Frontier Developments/Elite Dangerous/Cargo.json", recursive=True)
    observer.start()
    signal.signal(signal.SIGINT, sigInt)
    init()
    try:
        main()
    except:
        print("error")
        observer.stop()
        device.close()
        exit(0)
    observer.join()

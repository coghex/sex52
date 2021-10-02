import json
from x52_driver import X52Driver, X52ProEvdevKeyMapping, X52MfdLine, X52ColoredLedStatus

def handleNav(path,dev):
    f = open(path,'r')
    try:
        data = json.load(f)
    except Exception as ex:
        print("exception: ", ex)
    f.close()
    if (len(data["Route"]) == 0):
        line1 = "no route"
        line2 = " "
        line3 = " "
        dev.set_mfd_text(X52MfdLine.LINE1,line1)
        dev.set_mfd_text(X52MfdLine.LINE2,line2)
        dev.set_mfd_text(X52MfdLine.LINE3,line3)
        return None
    print("updating nav...")
    dest = data["Route"][0]["StarSystem"]
    if (len(data["Route"]) == 1):
        line1 = "final jump:"
        line2 = dest
        line3 = " "
        dev.set_mfd_text(X52MfdLine.LINE1,line1)
        dev.set_mfd_text(X52MfdLine.LINE2,line2)
        dev.set_mfd_text(X52MfdLine.LINE3,line3)
        return None
    system = data["Route"][-1]["StarSystem"]
    if (len(data["Route"]) > 1):
        line1 = "route:"
        line2 = "> " + dest
        line3 = "> " + system
        dev.set_mfd_text(X52MfdLine.LINE1,line1)
        dev.set_mfd_text(X52MfdLine.LINE2,line2)
        dev.set_mfd_text(X52MfdLine.LINE3,line3)


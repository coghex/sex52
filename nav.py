import os
import json
import journal
from x52_driver import X52Driver, X52ProEvdevKeyMapping, X52MfdLine, X52ColoredLedStatus

def handleNav(path,dev):
    f = open(path,'r')
    pathbase = os.path.dirname(path)
    f2 = open ((pathbase + "/" + (journal.getCurrentJournal(pathbase)) + ".01.log"))
    try:
        data = json.load(f)
    except Exception as ex:
        print("exception: ", ex)
    try:
        data1 = f2.read()
        data2 = data1.replace('}\n{','},{')
        data3 = json.loads(f'[{data2}]')
    except Exception as ex:
        data3 = ["unknown"]
        print("exception: ", ex)
        return None
    f.close()
    f2.close()
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
    loc = [x for x in data3 if x["event"] == "Location"]
    if (len(data["Route"]) == 1):
        if (len(loc[-1]["StarSystem"]) > 11):
            line1 = "loc: " + (loc[-1]["StarSystem"][0:11])
        elif (len(loc[-1]["StarSystem"]) > 6):
            line1 = "loc: " + (loc[-1]["StarSystem"])
        else:
            line1 = "location: " + (loc[-1]["StarSystem"])
        line2 = "destination: "
        line3 = dest
        dev.set_mfd_text(X52MfdLine.LINE1,line1)
        dev.set_mfd_text(X52MfdLine.LINE2,line2)
        dev.set_mfd_text(X52MfdLine.LINE3,line3)
        return None
    system = data["Route"][-1]["StarSystem"]
    if (len(data["Route"]) == 2):
        if (len(system) > 11):
            line1 = "loc: " + (system[0:11])
        elif (len(system) > 6):
            line1 = "loc: " + system
        else:
            line1 = "location: " + system
        if (len(dest) > 10):
            line2 = "dest: " + (dest[0:10])
        else:
            line2 = "dest: " + dest
        line3 = " "
        dev.set_mfd_text(X52MfdLine.LINE1,line1)
        dev.set_mfd_text(X52MfdLine.LINE2,line2)
        dev.set_mfd_text(X52MfdLine.LINE3,line3)
        return None
    nex = data["Route"][-2]["StarSystem"]
    if (len(data["Route"]) > 2):
        if (len(system) > 11):
            line1 = "loc: " + (system[0:11])
        elif (len(system) > 6):
            line1 = "loc: " + system
        else:
            line1 = "location: " + system
        if (len(nex) > 10):
            line2 = "next: " + (nex[0:10])
        else:
            line2 = "next: " + nex
        if (len(dest) > 10):
            line3 = "dest: " + (dest[0:10])
        else:
            line3 = "dest: " + dest
        dev.set_mfd_text(X52MfdLine.LINE1,line1)
        dev.set_mfd_text(X52MfdLine.LINE2,line2)
        dev.set_mfd_text(X52MfdLine.LINE3,line3)
        return None

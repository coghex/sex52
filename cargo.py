import json
from x52_driver import X52Driver, X52ProEvdevKeyMapping, X52MfdLine, X52ColoredLedStatus

def handleCargo(path,dev):
    f = open(path,'r')
    try:
        data = json.load(f)
    except Exception as ex:
        print("exception: ", ex)
    f.close()
    if (len(data["Inventory"]) == 0):
        line1 = "no cargo"
        line2 = " "
        line3 = " "
        dev.set_mfd_text(X52MfdLine.LINE1,line1)
        dev.set_mfd_text(X52MfdLine.LINE2,line2)
        dev.set_mfd_text(X52MfdLine.LINE3,line3)
        return None
    print("updating cargo...")
    data["Inventory"].sort(key=extract_count,reverse=True)
    name1 = data["Inventory"][0]["Name"]
    count1 = str(data["Inventory"][0]["Count"])
    if len(name1) > (14 - len(count1)):
        name1 = name1[0:(14 - len(count1))]
    if (len(data["Inventory"]) == 1):
        line1 = "cargo:"
        line2 = name1 + ": " + count1
        line3 = " "
        dev.set_mfd_text(X52MfdLine.LINE1,line1)
        dev.set_mfd_text(X52MfdLine.LINE2,line2)
        dev.set_mfd_text(X52MfdLine.LINE3,line3)
        return None
    name2 = data["Inventory"][1]["Name"]
    count2 = str(data["Inventory"][1]["Count"])
    if len(name2) > (14 - len(count2)):
        name2 = name2[0:(14 - len(count2))]
    if (len(data["Inventory"]) == 2):
        line1 = "cargo:"
        line2 = name1 + ": " + count1
        line3 = name2 + ": " + count2
        dev.set_mfd_text(X52MfdLine.LINE1,line1)
        dev.set_mfd_text(X52MfdLine.LINE2,line2)
        dev.set_mfd_text(X52MfdLine.LINE3,line3)
        return None
    name3 = data["Inventory"][2]["Name"]
    count3 = str(data["Inventory"][2]["Count"])
    if len(name3) > (14 - len(count3)):
        name3 = name3[0:(14 - len(count3))]
    line1 = name1 + ": " + count1
    line2 = name2 + ": " + count2
    line3 = name3 + ": " + count3
    dev.set_mfd_text(X52MfdLine.LINE1,line1)
    dev.set_mfd_text(X52MfdLine.LINE2,line2)
    dev.set_mfd_text(X52MfdLine.LINE3,line3)
    return None


def extract_count(json):
    try:
        return int(json["Count"])
    except KeyError:
        return 0


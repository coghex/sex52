import os
from datetime import datetime

def isJournal(files):
    ret = []
    for f in files:
        fn = os.path.basename(f)
        if (fn[0:8] == "Journal."):
            ret = ret + [fn[0:20]]
    ret.sort(key = lambda date: datetime.strptime(date, "Journal.%y%m%d%H%M%S"))
    return ret

def getCurrentJournal(path):
    files = os.listdir(path)
    journals = isJournal(files)
    return journals[-1]

def handleJournal(path,dev):
    print("Journal")

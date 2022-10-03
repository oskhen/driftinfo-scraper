#!/usr/bin/env python3

from datetime import datetime, timedelta
import glob, os, json

def isCached(group):
    files = glob.glob(f"./cache/{group}/*")
    latest = max(files, key=os.path.getctime)
    stamp = latest.split("\\")[1].split(".data")[0]
    if datetime.strptime(stamp, "%Y-%m-%d-%H-%M") < ( datetime.now() - timedelta(minutes=30) ):
        return False
    return True

def saveData(driftData, group):

    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M')
    filename = f"{timestamp}.data"
    filepath = f"cache/{group}/{filename}"
    with open(filepath, "w") as f:
        json.dump(driftData, f)

def loadData(group):
    files = glob.glob(f"./cache/{group}/*")
    latest = max(files, key=os.path.getctime)
    with open(latest, "r") as f:
        cache = json.load(f)
    return cache


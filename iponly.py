#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import re
from datetime import datetime, timedelta
import json
import glob, os
import Handler
import time


def getDriftInfo():

    if Handler.isCached("iponly"):
        return Handler.loadData("iponly")

    url = "https://cms.ip-only.se/feed/driftinfo"

    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    items = soup.find_all("item")

    driftinfo = ([item.find("content:encoded").contents[0] for item in items])

    extractedDataList = []

    for drift in driftinfo:
        driftdict = {}
        x = re.sub('<[^>]+>', "", drift)
        for line in x.split("\n"):
            if not line:
                continue
            a = line.split(": ", 1)
            if len(a) != 2:
                continue
            head, tail = a
            driftdict[head] = tail
        extractedDataList.append(driftdict)
    
    data = [ [driftinfo[i], extractedDataList[i] ] for i in range(len(driftinfo)) ]

    Handler.saveData(data, "iponly")

    return data

def getDriftInfobyStatus():

    driftinfo, driftlist = getDriftInfo()

    statusDict = {}
    for i, item in enumerate(driftlist):
        if "Status" in item:
            status = item["Status"]
            if status not in statusDict:
                statusDict[status] = [driftinfo[i]]
            else:
                statusDict[status].append(driftinfo[i])

    return statusDict

def getOngoingDriftInfo():

    data = getDriftInfo()

    lst = []

    for item in data:
        try:
            if item[1]["Status"] == "ONGOING" and datetime.strptime(item[1]["Occured"], "%d/%m/%Y %H:%M %Z") > ( datetime.now() - timedelta(weeks=2) ):
                lst.append(item[0])
        except:
            continue

    return lst

def getOverview():

    relevance = ["Location", "Occured", "Estimated Time of Repair"]
    data = getDriftInfo()
    lst = []

    for item in data:
        try:
            if item[1]["Status"] == "ONGOING" and datetime.strptime(item[1]["Occured"], "%d/%m/%Y %H:%M %Z") > ( datetime.now() - timedelta(weeks=2) ):
                x = [item[1][y] for y in relevance]
                age = int(time.time() - datetime.strptime(item[1]["Occured"], "%d/%m/%Y %H:%M %Z").timestamp())
                x.append(Handler.getColorbyAge(age))
                lst.append(x)
        except:
            continue

    return lst

if __name__ == "__main__":
    
    print(getOverview())
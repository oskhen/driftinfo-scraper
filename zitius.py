#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import Handler
import time

def getDriftInfo():

    if Handler.isCached("zitius"):
        return Handler.loadData("zitius")
    
    url = "https://zmarket.se/privat/driftinformation"

    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    divs = soup.find_all(class_="driftinfo-item")

    drifted = divs[0]
    planned = divs[1]

    delim = "<h3>"

    rawed = [x.decode_contents().split(delim) for x in divs]
    
    for i in range(len(rawed)):
        rawed[i] = [(delim + x.strip()) for x in rawed[i] if x.strip()]

    Handler.saveData(rawed, "zitius")

    return rawed

def getOngoingDriftInfo():

    data = getDriftInfo()[0]

    ongoing = list()

    for item in data:
        if "Påverkade områden" in item:
            timestamp = ""
            for line in item.split("\n"):
                if "<h3>" in line:
                    timestamp = ' '.join(re.sub('<[^>]+>', "", line).split(" ")[0:2])
            if timestamp:
                x = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                if x > ( datetime.now() - timedelta(weeks=2) ):
                    ongoing.append(item)

    return ongoing

def getOverview():

    data = getDriftInfo()[0]

    lst = []

    for item in data:
        if "Påverkade områden" in item:
            occurred = ""
            ETA = ""
            for line in item.split("\n"):
                if "<h3>" in line:
                    occurred = ' '.join(re.sub('<[^>]+>', "", line).split(" ")[0:2])
                if "åtgärdat: " in line:
                    ETA = line.split("åtgärdat: ")[1].removesuffix("</p>")
            
            areas = ', '.join([x.removesuffix("</li>") for x in item.split("<ul>")[1].split("</ul>")[0].strip("\n").split("<li>")[2:]])

            age = int(time.time() - datetime.strptime(occurred, "%Y-%m-%d %H:%M:%S").timestamp())
            x = [areas, occurred, ETA, Handler.getColorbyAge(age)]

            lst.append(x)
    
    return lst

if __name__ == "__main__":

    print(getOverview())

 
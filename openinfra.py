#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import Handler

fakeAgent = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}

def getDriftLinks():

    url = "https://openinfra.com/status/"
    soup = BeautifulSoup(requests.get(url, headers=fakeAgent).content, "html.parser")

    divs = soup.find_all(class_="card link blog-item")
    linklist = []

    for div in divs:

        driftType = div.decode_contents().split("<span>")[1].split("</span>")[0]
        if driftType == "Driftstopp" or driftType == "Driftstörning":
            href = div.decode_contents().split("href=\"")[1].split("\">")[0]
            linklist.append(href)
    
    return linklist

def getOngoingDriftInfo():

    if Handler.isCached("openinfra"):
        return Handler.loadData("openinfra")

    links = getDriftLinks()
    
    issues = []

    for link in links:

        url = link
        soup = BeautifulSoup(requests.get(url, headers=fakeAgent).content, "html.parser")
        # <div class="single-block">

        driftinfo = soup.find_all(class_="status-wrap")

        data = driftinfo[0].decode_contents()
        issues.append(data)

    Handler.saveData(issues, "openinfra")
    return issues

def getOverview():

    driftinfo = getOngoingDriftInfo()

    lst = []

    for item in driftinfo:
        location = item.split("Driftstörning ")[1].split("</h4>")[0]
        occurred = ' '.join(item.split("<strong>")[1].split("</strong>")[0].split())
        ETA = "?"
        lst.append([location, occurred, ETA])

    return lst

if __name__ == "__main__":
    
    print(getOverview())

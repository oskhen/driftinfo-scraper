#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import cacheHandler

chrDriver = "C:\\Users\\oh962419\\Chromedriver\\chromedriver"

def getSubPortals():

    url = "https://www.itux.se/driftinformation/"

    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    links = [x.lstrip("=\"//").split("\"")[0] for x in soup.find_all(class_="small-block-grid-2 medium-block-grid-4 large-block-grid-6")[0].decode_contents().split("href")[1:]]
    return links

def getDatafromLink(link, driver):

    link = link.removeprefix("http://")

    url = f"https://{link}/driftinformation/"

    #soup = BeautifulSoup(requests.get(url).content, "html.parser")
    #drift = soup.find_all(class_="large-12 columns large-centered")

    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")


    drift = [("<h4>" + x.replace("</dl></article><article>", "")) for x in soup.find_all(class_="large-12 columns large-centered")[0].decode_contents().split("<h4>")[1:]]

    try:
        drift[-1] = drift[-1].split("<dl class=\"accordion\"")[0]
    except:
        pass

    drift = [x for x in drift if "planerat" not in x and "Planerat" not in x and "ingen driftinformation" not in x]

    return drift

def getDriver():
    service = Service(ChromeDriverManager().install())
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def getOngoingDriftInfo():

    if cacheHandler.isCached("itux"):
        return cacheHandler.loadData("itux")

    driver = getDriver()
    links = getSubPortals()
    driftData = []

    for link in links:
        domain = link.split(".")[0]
        if "://" in domain:
            domain = domain.split("://")[1]
        
        data = getDatafromLink(link, driver)
        if data:
            driftData.append([domain, data])
        else:
            continue
    
    cacheHandler.saveData(driftData, "itux")

    return driftData

def getOverview():

    drift = getOngoingDriftInfo()
    lst = []

    for site in drift:
        items = site[1]
        for item in items:
            try:
                occurred = item.split("Skapad: ")[1].split(")")[0]
                ETA = "?"
                location = item.split("drabbar kunder i")[1].split("\n")[0]
                lst.append([location, occurred, ETA])
            except:
                continue
    
    return lst

if __name__ == "__main__":
    #print(getDatafromLink("goteborg.itux.se"))
    print(getOverview())

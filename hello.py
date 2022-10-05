#!/usr/bin/env python3

from flask import Flask, render_template
import zitius
import iponly
import openinfra
import itux

app = Flask(__name__)

### | TODO

## Coloring
# red = 1h
# yellow = 12h
# default = >12h
# green = solved

## Standardize timestamps

def loadZitiusInfo():
    
    data = zitius.getDriftInfo()
    return '<br>'.join(data[0])

def loadIPOnlyInfo():

    data = iponly.getOngoingDriftInfo()
    return '---<br>'.join(data)

@app.route("/")
def dashboard():
    return render_template('cards2-basic.jinja',
    iponly=iponly.getOngoingDriftInfo(),
    zitius=zitius.getOngoingDriftInfo(),
    openinfra=openinfra.getOngoingDriftInfo(),
    itux=itux.getOngoingDriftInfo())

@app.route("/wallboard")
def wallboard():
    return render_template("wallboard.jinja",
    iponly=iponly.getOverview(),
    zitius=zitius.getOverview(),
    itux=itux.getOverview(),
    openinfra=openinfra.getOverview())

@app.route("/iponly")
def routeIPOnly():
    return loadIPOnlyInfo()

@app.route("/zitius")
def routeZitius():
    return loadZitiusInfo()

@app.route("/testing")
def testing():
    return render_template("cards2.jinja")
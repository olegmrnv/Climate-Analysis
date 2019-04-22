from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
import datetime as dt
from flask import Flask, jsonify
from datetime import date, timedelta

engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False})
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)


app=Flask(__name__)


@app.route("/")
def home():
    return (
        f"------------------------------------------------------------------------------------<br/>"
        f"You are at the home page, please use one of the following addresses:<br/>"
        f"------------------------------------------------------------------------------------<br/><br/>"
        f"/api/precipitation<br/>"
        f"/api/stations<br/>"
        f"/api/temperature<br/>"
        f"/api/&#60start&#62<br/>"
        f"/api/&#60start&#62/&#60end&#62"

    )

@app.route("/api/precipitation")
def precipitation():
    prcp = session.query(Measurement.date, Measurement.prcp).all()
    prcp = dict(prcp)
    return (
        jsonify(prcp)
    )

@app.route("/api/stations")
def stations():
    stn = session.query(Station.station).all()
    stn = list(np.ravel(stn))
    return (
        jsonify(stn)
    )

@app.route("/api/temperature")
def temperature():
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    latest_date = dt.datetime.strptime(latest_date, '%Y-%m-%d').date()
    year_ago = latest_date - dt.timedelta(days = 365)
    date_tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= year_ago).all()
    date_tobs = dict(date_tobs)
    return jsonify(date_tobs)

@app.route("/api/<start>")
def from_start(start):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    temps = session.query(*sel).filter(Measurement.date >= start).all()[0]    
    return jsonify(temps)

@app.route("/api/<start>/<end>")
def strt_end(start, end):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    temps = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()[0]
    return jsonify(temps)


if __name__ == "__main__":
    app.run(debug=True)

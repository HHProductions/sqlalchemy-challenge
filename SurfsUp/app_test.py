import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations"
        f"/api/v1.0/stations/api/v1.0/tobs"
        f"/api/v1.0/stations/api/v1.0/<start>"
        f"/api/v1.0/stations/api/v1.0/<start>/<end>"
    )
##############

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation detail"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()
    # Create a dictionary from the row data and append to a list of precipitation data
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    # Convert list of tuples into normal list
   # all_prcp = list(np.ravel(results))

    return jsonify(all_prcp)

##############

@app.route("/api/v1.0/stations")
def station_name():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list stations"""
    # Query all stations
    results = session.query(Station.station, Station.name).all()

    session.close()

    # Create a dictionary from the row data and append to a list of stations
    all_stations = []
    for station, name in results:
        stations_dict = {}
        stations_dict["station"] = station
        stations_dict["name"] = name
        all_stations.append(stations_dict)

    return jsonify(all_stations)

##############

@app.route("/api/v1.0/tobs")
def temperature():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list temperatures"""
    # Query all temperatures for station USC00519281
    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= year_ago).\
        filter(Measurement.station == "USC00519281").all()

    session.close()
    # Create a dictionary from the row data and append to a list of temperature data
    all_temperature = []
    for date, tobs in results:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["tobs"] = tobs
        all_temperature.append(temp_dict)

    return jsonify(all_temperature)



##############

@app.route("/api/v1.0/2016-8-23")
def temp_stats():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a stats on temperatures"""
    # Query all temperatures for station USC00519281

    min_temp = session.query(Measurement.date, func.min(Measurement.tobs)).\
            filter(Measurement.station == "USC00519281").all()
    # max_temp = session.query(func.max(Measurement.tobs)).\
    #     filter(Measurement.station == "USC00519281").all()
    # avg_temp = session.query(func.avg(Measurement.tobs)).\
    #     filter(Measurement.station == "USC00519281").all()
        # filter(Measurement.date>="2016-08-23").\


    session.close()
    # # Create a dictionary from the row data and append to a list of temperature data
    # min_max_avg = []
    # temp_stat = {}
    # for date, tobs in min_temp:
    #     temp_stat["date"] = date
    #     temp_stat["temp"] = min_temp
    #     min_max_avg.append(temp_stat)
    # temp_stat["temp"] = max_temp
    # min_max_avg.append(temp_stat)
    # temp_stat["temp"] = avg_temp
    # min_max_avg.append(temp_stat)

    return jsonify(min_temp)



if __name__ == '__main__':
    app.run(debug=True)

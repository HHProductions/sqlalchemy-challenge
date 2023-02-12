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
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/stations/api/v1.0/tobs<br/>"
        f"/api/v1.0/stations/api/v1.0/start<br/>"
        f"/api/v1.0/stations/api/v1.0/start&end<br/>"
        f"<br/>"
        f"For start and end please use yyyy-mm-dd format and ensure they are separated by &."

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

@app.route("/api/v1.0/<start>")
def temp_stats(start):
    # Create our session (link) from Python to the DB

    session = Session(engine)

    """Return a stats on temperatures"""
    # Query all temperatures for station USC00519281
    # define list and dictionaries for data capture
    temp_stat = []
    min_dict = {}
    max_dict = {}
    avg_dict = {}
    session = Session(engine)
    

#     """Return a list temperatures"""
#     # Query all temperatures for station USC00519281
    
    results1 = session.query(Measurement.date, func.min(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.station == "USC00519281").all()
    results2 = session.query(Measurement.date, func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.station == "USC00519281").all()
    results3 = session.query(Measurement.date, func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.station == "USC00519281").all()
# filter(Measurement.date >= year_ago).\
#         filter(Measurement.station == "USC00519281").all()
    session.close()
     # Create a dictionary from the row data and append to a list of temperature data
    
    for date, tobs in results1:
        min_dict["TMIN"] = tobs
        temp_stat.append(min_dict)
    for date, tobs in results2:
        max_dict["TMAX"] = tobs
        temp_stat.append(max_dict)
    for date, tobs in results3:
        avg_dict["TAVG"] = tobs
        temp_stat.append(avg_dict)

    return jsonify(temp_stat)

@app.route("/api/v1.0/<start>&<end>")
def temp_stats1(start,end):
    # Create our session (link) from Python to the DB

    session = Session(engine)

    """Return a stats on temperatures"""
    # Query all temperatures for station USC00519281
    # define list and dictionaries for data capture
    temp_stat1 = []
    min_dict1 = {}
    max_dict1 = {}
    avg_dict1 = {}
    session = Session(engine)
    

#     """Return a list temperatures"""
#     # Query all temperatures for station USC00519281
    
    results1 = session.query(Measurement.date, func.min(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).\
    filter(Measurement.station == "USC00519281").all()
    results2 = session.query(Measurement.date, func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).\
    filter(Measurement.station == "USC00519281").all()
    results3 = session.query(Measurement.date, func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).\
    filter(Measurement.station == "USC00519281").all()
# filter(Measurement.date >= year_ago).\
#         filter(Measurement.station == "USC00519281").all()
    session.close()
     # Create a dictionary from the row data and append to a list of temperature data
    
    for date, tobs in results1:
        min_dict1["TMIN"] = tobs
        temp_stat1.append(min_dict1)
    for date, tobs in results2:
        max_dict1["TMAX"] = tobs
        temp_stat1.append(max_dict1)
    for date, tobs in results3:
        avg_dict1["TAVG"] = tobs
        temp_stat1.append(avg_dict1)

    return jsonify(temp_stat1)






if __name__ == '__main__':
    app.run(debug=True)

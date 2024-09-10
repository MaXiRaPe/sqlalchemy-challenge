# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, text, inspect

from flask import Flask, jsonify

## Function definition to transform dates


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
# Base.classes.keys()
# Save references to each table
Msmt = Base.classes.measurement
Stn = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# Home route
@app.route("/")
def welcome():
  
    """List all available api routes."""
    return (
        f"This app provides Precipitation and observed Temperatures from different stations in Hawaii. <br/>"
        f"Copy route into browser to access. <br/>"
        f"<br/>Available Routes:<br/>"
        f"<br/>Precipitation for the last year:<br/>" 
        f"/api/v1.0/precipitation<br/>"
        f"<br/>List of Stations:<br/>" 
        f"/api/v1.0/stations<br/>"
        f"<br/>Temperatures observed in the last year by the most active station: <br/>" 
        f"/api/v1.0/tobs<br/>"
        f"<br/>Search for Temperature Stats from a start date:<br/>" 
        f"/api/v1.0/date/'2017-08-23'<br/>"
        f"<br/>Search for Temperature Stats between two dates:<br/>" 
        f"/api/v1.0/date_range/'2016-08-23/2017-08-23'<br/>"
    )

# precipitation route
## Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
@app.route("/api/v1.0/precipitation")
def precipitation():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Create and List a JSON representation of a dictionary with precipitation data."""
    
    recent_date = session.query(Msmt.date).\
        order_by(Msmt.date.desc()).first()
    
    recent_date2 = pd.to_datetime(recent_date[0])
    yy = recent_date2.year
    mm = recent_date2.month
    dd = recent_date2.day
    query_date = dt.date(yy, mm, dd) - dt.timedelta(days=365)
    
    results = session.query(Msmt.date, Msmt.prcp).\
        filter(Msmt.date >= query_date).\
        order_by(Msmt.date.desc()).all()

    session.close()

    precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation.append(precipitation_dict)

    return jsonify(precipitation)


# # stations route
# ## Return a JSON list of stations from the dataset
@app.route("/api/v1.0/stations")
def stations():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Create a JSON list of stations from the dataset."""
    
    sel = [Stn.station, Stn.name]
    stations_qry = session.query(*sel).\
    filter(Stn.station == Msmt.station).\
    group_by(Msmt.station).\
    order_by((Stn.name).desc()).all()
    
    session.close()

    stations = []
    for station, name in stations_qry:
        stations_dict = {}
        stations_dict["station"] = station
        stations_dict["name"] = name
        stations.append(stations_dict)

    return jsonify(stations)


# # temperatures route
# ## Query the dates and temperature observations of the most-active station for the previous year of data.
@app.route("/api/v1.0/tobs")
def tobs():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of temperature observations for the previous year."""
    
    sel = [Msmt.station, func.count(Msmt.date)]
    totals = session.query(*sel).\
        group_by(Msmt.station).\
        order_by(func.count(Msmt.date).desc()).all()
    active_station = totals[0][0]
    
    stn_date1 = session.query(Msmt.date).\
        filter(Msmt.station == totals[0][0]).\
        order_by(Msmt.date.desc()).first()

    stn_date2 = pd.to_datetime(stn_date1[0])
    yys = stn_date2.year
    mms = stn_date2.month
    dds = stn_date2.day
    query_date2 = dt.date(yys, mms, dds) - dt.timedelta(days=365)

    tobs_qry = session.query(Msmt.date, Msmt.tobs).\
        filter(Msmt.station == active_station).\
        filter(Msmt.date >= query_date2).\
        order_by(Msmt.date.desc()).all()

    session.close()

    tobs_ls = []
    for date, tobs in tobs_qry:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_ls.append(tobs_dict)

    return jsonify(tobs_ls)


# start date route
## For a specified start, calculate TMIN,TAVG, and TMAX for all the dates greater than or equal to the start date.

@app.route("/api/v1.0/date/<start>")
def start_date(start):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date."""
    
    sel = [func.min(Msmt.tobs),
       func.max(Msmt.tobs),
       func.avg(Msmt.tobs)]
    temp_stats = session.query(*sel).\
    filter(Msmt.date >= start).all()

    session.close()

    stats_ls = [{"TMIN":temp_stats[0][0],"TMAX": temp_stats[0][1], "TAVG":temp_stats[0][2]}]         
        
    
    return jsonify(stats_ls)

    
# start and end date route
## For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.

@app.route("/api/v1.0/date_range/<start>/<end>")
def range_date(start, end):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive."""
    
    if  start > end:
        max_date = start
        min_date = end
    else:
        max_date = end
        min_date = start
   
    sel = [func.min(Msmt.tobs),
       func.max(Msmt.tobs),
       func.avg(Msmt.tobs)]
    temp_stats = session.query(*sel).\
       filter(Msmt.date >= min_date, Msmt.date <= max_date).all()
 
    session.close()

    stats_ls = [{"TMIN":temp_stats[0][0],"TMAX": temp_stats[0][1], "TAVG":temp_stats[0][2]}]         
     
    return jsonify(stats_ls)

if __name__ == '__main__':
    app.run(debug=True)
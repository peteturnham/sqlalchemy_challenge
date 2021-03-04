##############################################
##############################################
#####Package for Flask Web Deployment
##############################################


##############################################
# Importing Required Packages and Dependencies 
##############################################
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import pandas as pd
from flask import Flask, jsonify, request, render_template
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement= Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
api_version = "v1.0"

def base_url():
    return "api/" + api_version

#################################################
# Flask Routes
#################################################

@app.route("/")
@app.route("/index")
def welcome_page():

    base_p = f'{request.base_url}api/{api_version}/'
    api_p = f'/api/{api_version}/'
    return f'''
<!DOCTYPE html>
<html>
<body>
<h1>Welcome to the Flask API for the Hawaii Climate</h1>
<p>This app is version {api_version}. Please use the path {request.base_url}api/{api_version} to get to the endpoints.</p>
<h2>Headings</h2>
<ul>
  <li><a href="{request.base_url}">home</a></li>
  <li><a href="{base_p}precipitation">precipitation - {api_p}precipitation</a></li>
  <li><a href="{base_p}stations">stations - {api_p}stations</a></li>
  <li><a href="{base_p}tobs">tobs - {api_p}tobs</a></li>
  <li>start - {api_p}[start]</li>
  <li>start and end - {api_p}[start]/[end]</li>
</ul>
</body>
</html>'''



#################################################
#   Path to Precipitation Measurement Data 
#################################################

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all recorded temperatures in Hawaii"""
    # Query all passengers
    results = session.query(measurement.date, measurement.prcp).all()
    

    session.close()

    # Convert list of tuples into normal list
    all_data = list(np.ravel(results))

    return jsonify(all_data)
#################################################
#   Path to Station Data
#################################################

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations and their related data"""
    #query for stations in the dataset
    results = session.query(station.station, station.name).all()
    # Convert list of tuples into normal list
    all_data = list(np.ravel(results))

    session.close()



    return jsonify(all_data)
#################################################
#   Temperature observations
#################################################
@app.route("/api/v1.0/tobs")
def tobs():
    #creating a session link to our database
    session = Session(engine)
    twelve_months = dt.date(2017,8,23)- dt.timedelta(days=365)
    data = session.query(measurement.station, measurement.tobs).filter(measurement.date>=twelve_months).\
        filter_by(station = 'USC00519281')
    all_tobs = []
    for station, tobs in data:
        temp_dict = {}
        temp_dict["station"]= station
        temp_dict["temperature observation"]= tobs
        all_tobs.append(temp_dict)




    
    
    return jsonify(all_tobs)


if __name__ == '__main__':
    app.run(debug=True)

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
  <li><a href="{base_p}start">start - {api_p}start</a></li>
  <li>start - {api_p}start date(Y-M-D)</li>
  <li>start and end - {api_p}start date(Y-M-D)/end date(Y-M-D)</li>
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
    rain = []
    for date, prcp in results:
        rain_dict = {}
        rain_dict["date"] = date
        rain_dict["precipitation"] = prcp
        rain.append(rain_dict)
    return jsonify(rain)
    session.close()

    


#################################################
#   Path to Station Data
#################################################

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    station = Base.classes.station
    """Return a list of stations and their related data"""
    #query for stations in the dataset
    results = session.query(station.name, station.station).all()
    # Convert list of tuples into normal list
    session.close()
   
    
    station_info = []
    for name, station in results:
        stations= {}
        stations["Station Location "]= name
        stations["Station"] = station
        station_info.append(stations)

     # close out the query session
   
    
    
    return jsonify(station_info)
    
#################################################
#   Path to Temperature Observations
#################################################
@app.route("/api/v1.0/tobs")
def tobs():
    #creating a session link to our database
    session = Session(engine)
    twelve_months = dt.date(2017,8,23)- dt.timedelta(days=365)
    data = session.query(measurement.station, measurement.tobs, measurement.date).filter(measurement.date>=twelve_months).\
        filter_by(station = 'USC00519281')
    all_tobs = []
    for station, tobs, date in data:
        temp_dict = {}
        temp_dict["station"]= station
        temp_dict["temperature observation(fahrenheit)"]= tobs
        temp_dict["date recorded"]= date
        all_tobs.append(temp_dict)

    # close out the query session
    session.close()
    info= "Temperature Recordings from 2016-08-23 to 2017-08-18"
    the_goods=jsonify (all_tobs)
    return (the_goods)

@app.route("/api/v1.0/start")
def display():
    return(f"To use this page, type in your desired query date in the format of 'Year-Month-Day'" )

#################################################
#   Path for start date input
#################################################
@app.route("/api/v1.0/<start>")

# defineing a function that takes in a variable
def temp_search(start):
    #start session
    session = Session(engine)
    #convert object to string, then string to integer
    converted_date= dt.datetime.strptime(start, "%Y-%m-%d").date()
    #method to return data back to user
    temps = [func.min(measurement.tobs),
            func.avg(measurement.tobs),
            func.max(measurement.tobs)]
    #query to supply user input date
    temp = session.query(*temps).\
                filter(func.strftime('%Y-%m-%d', measurement.date) >= converted_date).all()
    return jsonify(
    f'The minimum temperature(fareinheit) is: {temp[0][0]}'
    f' The average temperature(fareinheit) is: {temp[0][1]}'
    f' The maximum temperature(fareinheit) is: {temp[0][2]}'
    )

#################################################
#   Path for start/end date input
#################################################
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    #start session
    session = Session(engine)
    #user defined start input
    converted_date= dt.datetime.strptime(start, "%Y-%m-%d").date()
    end_converted_date =  dt.datetime.strptime(end, "%Y-%m-%d").date()
    #method to return data back to user
    temps = [func.min(measurement.tobs),
            func.avg(measurement.tobs),
            func.max(measurement.tobs)]
    #query to supply user input date
    temp = session.query(*temps).\
                filter(func.strftime('%Y-%m-%d', measurement.date) >= converted_date).\
                    filter(func.strftime('%Y-%m-%d', measurement.date) >= end_converted_date).all()
    return jsonify(f'The minimum temperature(fareinheit) is: {temp[0][0]}'
    f' The average temperature(fareinheit) is: {temp[0][1]}'
    f' The maximum temperature(fareinheit) is: {temp[0][2]}'
    )

    

if __name__ == '__main__':
    app.run(debug=True)

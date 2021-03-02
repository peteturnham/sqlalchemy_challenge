from flask import Flask, jsonify, request
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
#############################
# Flask set up
#############################

app = Flask(__name__)
#app version
api_version = "v1.0"

#############################
# Database Setup
engine = create_engine("sqlite:///resources/hawaii.sqlite")
# Reflect an existing database into a new model
Base = automap_base()
# Reflect the tables from the database
Base.prepare(engine, reflect= True)

# Save reference to table
data = Base.classes.hawaii


#############################
# 

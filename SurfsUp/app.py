# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurements = Base.classes.measurement
stations = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/age_range/lower_age/upper_age<br/>"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    """Return the last 12 months of precipitation data"""

    prcp = session.query(measurements.date, measurements.prcp).filter(measurements.date>="2016-08-23").all()

    #Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary 
    # using date as the key and prcp as the value.
    prcp_dict = {}

    for result in prcp:
    
        date = result.date
        prcps = result.prcp
        prcp_dict[date] = prcps

    #Return the JSON representation of your dictionary.
    
    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():

    """Return all stations in the dataset"""
    
    #Return a JSON list of stations from the dataset.
    sttn = session.query(measurements.station, func.count(measurements.station)).group_by(measurements.station).order_by(func.count(measurements.station).desc()).all()
    
    sttn_dict = list(np.ravel(sttn))
    
    return jsonify(sttn_dict)

session.close()

if __name__ == '__main__':
    app.run(debug=True)
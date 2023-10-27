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
        f"/api/v1.0/<start><br/>"
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
    sttn = session.query(measurements.station, func.count(measurements.station)
                         ).group_by(measurements.station
                                    ).order_by(func.count(measurements.station).desc()).all()
    
    sttn_dict = list(np.ravel(sttn))
    
    return jsonify(sttn_dict)

@app.route("/api/v1.0/tobs")
def tobs(): 

    """Return temperatures for the last year of data for the most-active station"""
    
    #Query the dates and temperature observations of the most-active station for the previous year of data.

    temp = session.query(measurements.date, measurements.tobs).filter(
                        measurements.station == 'USC00519281',
                        measurements.date >= "2016-08-23").all()
    
    temp_dict = list(np.ravel(temp))
    #Return a JSON list of temperature observations for the previous year.
    return jsonify(temp_dict)

@app.route(f"/api/v1.0/<start>")
def get_temp(start):

    """Return the min, avg, and max temps after a date"""
    temp_range = session.query(measurements.tobs, func.min(measurements.tobs), 
                               func.max(measurements.tobs), func.avg(measurements.tobs)).filter(measurements.date >= start).all()

    temp_range_dict = list(np.ravel(temp_range))

    return jsonify(temp_range_dict)

@app.route("/api/v1.0/<start>/<end>")
def get_range(start, end):
        
        """Return the min, avg, and max temps for a date range"""
        range = session.query(measurements.date, func.min(measurements.tobs), func.avg(measurements.tobs), func.max(measurements.tobs)
                              ).filter(measurements.date >= start, measurements.date <= end).group_by(measurements.date).all()
        
        range_list = list(np.ravel(range))
        
        return jsonify(range_list)

session.close()

if __name__ == '__main__':
    app.run(debug=True)
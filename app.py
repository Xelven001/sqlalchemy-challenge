# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import text
from datetime import datetime, timedelta
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(autoload_with=engine)
# reflect the tables

Base.classes.keys()

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)




app = Flask(__name__)

# Define route for the homepage
@app.route('/')
def home():
    return (
        f"Welcome to Climate App!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

# Define route for precipitation data
@app.route('/api/v1.0/precipitation')
def precipitation():
    # Construct the SQL query to retrieve precipitation data for the last 12 months
    start_date = datetime.strptime("2017-08-23", "%Y-%m-%d") - timedelta(days=365)

    query = text('SELECT date, prcp FROM measurement WHERE date >= :start_date ORDER BY date DESC')
    results = session.execute(query, {"start_date": start_date})
    
    # Convert query results into a dictionary
    precipitation_data = {}
    for row in results:
        precipitation_data[row[0]] = row[1]
    
    return jsonify(precipitation_data)

# Define route for stations
@app.route('/api/v1.0/stations')
def stations():
    # Construct the SQL query to retrieve stations
    query = text('SELECT DISTINCT station FROM station')
    results = session.execute(query)
    
    # Convert query results into a list
    station_list = [row[0] for row in results]
    
    return jsonify(station_list)

#Define route for temperature observations
@app.route('/api/v1.0/tobs')
def tobs():
    start_date = datetime.strptime("2017-08-23", "%Y-%m-%d") - timedelta(days=365)
    query = text('SELECT station,date, tobs FROM measurement WHERE station = "USC00519281" AND date >= :start_date ORDER BY date DESC')
    results = session.execute(query, {"start_date": start_date})
    
    tobs_data = [{"station": row[0],"date": row[1], "temperature": row[2]} for row in results]
    
    return jsonify(tobs_data)
# # Define route for temperature statistics
def temperature_stats_start(start):
    query = text('SELECT MIN(tobs), AVG(tobs), MAX(tobs) FROM measurement WHERE date >= :start_date')
    results = session.execute(query, {"start_date": start})
    temperature_stats = list(results.fetchone())
    
    temperature_stats_dict = {
        "TMIN": temperature_stats[0],
        "TAVG": temperature_stats[1],
        "TMAX": temperature_stats[2]
    }

    return jsonify(temperature_stats_dict)



@app.route('/api/v1.0/<start>/<end>')
def temperature_stats_start_end(start, end):
    query = text('SELECT MIN(tobs), AVG(tobs), MAX(tobs) FROM measurement WHERE date BETWEEN :start_date AND :end_date')
    results = session.execute(query, {"start_date": start, "end_date": end})
    temperature_stats = list(results.fetchone())
    
    temperature_stats_dict = {
        "TMIN": temperature_stats[0],
        "TAVG": temperature_stats[1],
        "TMAX": temperature_stats[2]
    }

    return jsonify(temperature_stats_dict)



if __name__ == '__main__':
    app.run(debug=True)

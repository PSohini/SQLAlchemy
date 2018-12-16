# 12 months
last_year = dt.date(2017,8,23)-dt.timedelta(days=365)

@app.route(“/”)
def welcome():
   “”"List all available api routes.“”"
   return (
       f”Hawaii Weather<br/>”
       f”/api/v1.0/precipitation<br/>”
       f”/api/v1.0/stations<br/>”
       f”/api/v1.0/tobs<br/>”
       f”/api/v1.0/<start><br/>”
       f”/api/v1.0/<start>/<end>”
   )


@app.route(“/api/v1.0/precipitation”)
def precipitation():
   “”"convert query results using date as the key and prcp as the value”“”
   prcp_results = session.query(Measurement.date, Measurement.prcp).\
   filter(Measurement.date >= last_year).group_by(Measurement.date).all()

   return jsonify(prcp_results)

@app.route(“/api/v1.0/stations”)
def stations():
   “”"Return a list of stations”“”
   station = session.query(Station.station, Station.name).all()

   return jsonify(station)

@app.route(“/api/v1.0/tobs”)
def tobs():
   “”"Return a list of dates and temperature observations from last 12 months”“”
   temperature = session.query(Measurement.date, func.avg(Measurement.tobs)).\
   filter(Measurement.date >= last_year).all()

   return jsonify(temperature)

@app.route(“/api/v1.0/<start>“)
def startdate(start):
   “”"Return a list of min temp, avg temp, max temp for start or start-end range”“”
   “”"<start> only: TMIN, TAVG, TMAX for all dates >= start date”“”
   s_temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
   filter(Measurement.date >= start).all()

   return jsonify(s_temps)

@app.route(“/api/v1.0/<start>/<end>“)
def startenddate(start, end):
   “”"Return a list of min temp, avg temp, max temp for start or start-end range”“”
   “”"<start> and <start>/<end>: TMIN, TAVG, TMAX for dates in between”“”
   se_temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
   filter(Measurement.date >= start).filter(Measurement.date <= end).all()

   return jsonify(se_temps)

if __name__ == ‘__main__‘:
   app.run(debug=True)
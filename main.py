import os
import time
import inverter
import energydb
import threading
from datetime import datetime, date
from flask import Flask, request, render_template

# Global data base object
db = None
app = Flask(__name__)

# Huawei OpenAPI username
USER_NAME = 'TODO'
# Huawei OpenAPI password
USER_PASS = 'TODO'
# Device id
DEV_ID = 'TODO'
# Device type
DEV_TYPE = 'TODO'

###############################################################################
#
# COLLECT&PROCESS Thread
#
def collect_process_data():
    """
        1) Connect to Huawei Fusion Solar OpenAPI.

        2) Dump station and devices list.

        3) Extract custom device data.

        4) Save device data to database.

        5) Sleep for 5 minutes (required by Huawei Fusion Solar documentation).
    """

    # Intialize Huawei Fusion Solar
    inv = inverter.Inverter(USER_NAME, USER_PASS)
    inv.login()

    # Print stations and devices
    stations_list = inv.get_stations_list()
    for station in stations_list:
        print("Station:")
        print("  Code   : %s" % (station.get('stationCode')))
        print("  Name   : %s" % (station.get('stationName')))
        print("  Address: %s" % (station.get('stationAddr')))

        devices_list = inv.get_station_devices_list(station.get('stationCode'))
        for device in devices_list:
            print("    Device:")
            print("     Id  : %s" % (device.get('id')))
            print("     Name: %s" % (device.get('devName')))
            print("     Type: %s" % (device.get('devTypeId')))

    # Extract data and save to database
    while True:
        print("==================== collect data ====================")
        inverter_data = inv.get_device_data(DEV_ID, DEV_TYPE)
        db.insert_inverter_data(inverter_data)
        time.sleep(300)

###############################################################################
#
# Flask
# Allow querry by datetime (URL/?date=...). Based on specified datetime, querry
# sqlite data base and return the records to be displayed as a graph.
#

@app.route("/")
def index():
    # Validate that parameter is specified
    req_date = request.args.get('date')
    if req_date == None:
        return "No date selected"

    # Validate parameter value
    try:
        date_obj = datetime.strptime(req_date, '%d-%m-%Y')
        datetime_min_obj = datetime.combine(date_obj, datetime.min.time())
        datetime_max_obj = datetime.combine(date_obj, datetime.max.time())
    except:
        return "Invalid date format"

    # Querry data base
    data = db.get_inverter_data_by_date(datetime_min_obj, datetime_max_obj)
    if len(data) == 0:
        return "No records for date " + req_date

    timestamp = []
    active_power = []
    for i in data:
        timestamp.append(i[1])
        active_power.append(i[0])

    # Return data to be displayed as graph
    return render_template("index.html", labels=timestamp,
                                         data=active_power,
                                         user=USER_NAME)

if __name__ == "__main__":
    # Initialize data base (global)
    db = energydb.EnergyDB()

    # Start Inverter and DB thread
    collect_process_thread = threading.Thread(target=collect_process_data)
    collect_process_thread.start()

    # Flask APP (main thread)
    app.run(debug=False)

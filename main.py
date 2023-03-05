import time
import inverter
import energydb
import threading
from flask import Flask

"""
TODO
"""
app = Flask(__name__)

# Data base global
db = None

###############################################################################
#
# Collect and process thread
#
def collect_process_data():
    # Intialize Huawei Fusion Solar
    inv = inverter.Inverter('TODO','TODO')
    inv.login()
    inv.get_stations_list()
    inv.get_devices_list('NE=34087202')

    while True:
        print("==================== collect data ====================")
        inverter_data = inv.get_device_data('1000000034087203', '38')

        # Insert data to data base
        db.insert_data(inverter_data)

        print("========================================================")
        time.sleep(300)

###############################################################################
#
# Flask
#
@app.route("/")
def index():
    data = collect_data()
    return str(data)

def collect_data():
    return db.get_data()

###############################################################################

if __name__ == "__main__":
    # Initialize data base (global)
    db = energydb.EnergyDB()

    # Start Inverter and DB thread
    collect_process_thread = threading.Thread(target=collect_process_data)
    collect_process_thread.start()

    # Flask APP (main thread)
    app.run(debug=False)

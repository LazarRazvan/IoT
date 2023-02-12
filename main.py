import inverter
import energydb
"""
TODO
"""

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    # Create database
    db = energydb.EnergyDB()
    db.create_table()

    # Huawei Fusion Solar Connect
    inv = inverter.Inverter('','')
    inv.login()
    inv.get_stations_list()
    inverter_data = inv.get_plant_data("")

    print(inverter_data)

    # Insert data to data base
    db.insert_data(inverter_data)

    # Print data base
    records = db.get_data()

    return render_template("index.html", records=records)

if __name__ == "__main__":
    # Run application
    app.run()

import time
import inverter
import energydb

"""
TODO
"""

if __name__ == "__main__":
    # Create database
    db = energydb.EnergyDB()
    db.create_table()

    # Huawei Fusion Solar Connect
    inverter = inverter.Inverter('TODO','TODO')
    inverter.login()
    inverter.get_stations_list()
    inverter.get_devices_list('NE=34087202')

    while True:
        print("==================== collect data ====================")
        inverter_data = inverter.get_device_data('1000000034087203', '38')

        # TODO: Debug
        print(inverter_data)

        # Insert data to data base
        db.insert_data(inverter_data)

        # Print data base
        records = db.get_data()

        print("========================================================")
        time.sleep(300)

import json
import sqlite3

"""
Data base to store the value of energy produced by the solar panels.
"""
class EnergyDB(object):
    """ Database location"""
    DB_NAME = "energy.db"

    def __init__(self):
        """ Connect to data base """
        self.connection = sqlite3.connect(EnergyDB.DB_NAME)
        self.cursor = self.connection.cursor()

    def close(self):
        """ Close data base connection """
        self.connection.close()

    def create_table(self):
        """ Create table to track invertor energy """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS InverterEnergy (
            active_power REAL,
            reactive_power REAL,
            temperature REAL,
            input_voltage REAL,
            input_current REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)

    def insert_data(self, data_tuple):
        """ Insert inverter records to data base """
        self.cursor.execute("""
            INSERT INTO InverterEnergy (active_power, reactive_power, temperature, input_voltage, input_current)
            VALUES (?, ?, ?, ?, ?)
            """, (data_tuple[0], data_tuple[1], data_tuple[2], data_tuple[3], data_tuple[4]),
        )

    def get_data(self):
        """ Print data base InverterEnergy records """
        print("InverterEnergy:")
        records = self.cursor.execute("SELECT * FROM InverterEnergy").fetchall()
        print(records)

        return records

    def commit(self):
        """ Commit changes to database """
        self.connection.commit()

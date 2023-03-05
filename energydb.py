import json
import sqlite3
from datetime import datetime
from threading import Lock

"""
Singleton data base to store the value of energy produced by the solar panels.
"""
class EnergyDB(object):
    """ Database location"""
    DB_NAME = "energy.db"
    __singleton = None
    __lock = Lock()

    @staticmethod
    def get_instance(self):
        """ Get DB instance """
        if EnergyDB.__singleton == None:
            EnergyDB()

        return EnergyDB.__singleton

    def __init__(self):
        """ Connect to data base and create table """
        # Singleton
        if EnergyDB.__singleton != None:
            raise Exception("Singleton error!")

        # Connect to DB
        self.connection = sqlite3.connect(EnergyDB.DB_NAME, check_same_thread=False)
        self.cursor = self.connection.cursor()

        # Create table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS InverterEnergy (
            active_power REAL,
            reactive_power REAL,
            temperature REAL,
            input_voltage REAL,
            input_current REAL,
            timestamp DATETIME
        )
        """)

        EnergyDB.__singleton = self

    def close(self):
        """ Close data base connection """
        self.connection.close()

    def insert_data(self, data_tuple):
        """ Insert inverter records to data base """
        self.__lock.acquire()

        self.cursor.execute("""
            INSERT INTO InverterEnergy (active_power, reactive_power, temperature, input_voltage, input_current, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (data_tuple[0], data_tuple[1], data_tuple[2], data_tuple[3], data_tuple[4], datetime.now())
        )
        self.connection.commit()

        self.__lock.release()

    def get_data(self):
        """ Print data base InverterEnergy records """
        self.__lock.acquire()

        records = self.cursor.execute("SELECT * FROM InverterEnergy").fetchall()

        self.__lock.release()
        return records

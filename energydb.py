import json
import sqlite3
from threading import Lock
from datetime import datetime, date

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
        """ Connect to data base and create table for inverter """
        # Singleton
        if EnergyDB.__singleton != None:
            raise Exception("Singleton error!")

        # Connect to DB
        self.connection = sqlite3.connect(EnergyDB.DB_NAME, check_same_thread=False)
        self.cursor = self.connection.cursor()

        # Create table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS InverterPower (
            active_power REAL,
            timestamp DATETIME
        )
        """)

        EnergyDB.__singleton = self

    def close(self):
        """ Close data base connection """
        self.connection.close()

    def insert_inverter_data(self, data_dict):
        """ Insert inverter record to data base and set timestamp """
        self.__lock.acquire()

        record_datetime = datetime.now().replace(microsecond=0)
        self.cursor.execute("""
            INSERT INTO InverterPower (active_power, timestamp)
            VALUES (?, ?)
            """, (data_dict['active_power'], record_datetime)
        )
        self.__lock.release()

        self.connection.commit()


    def get_inverter_data_by_date(self, datetime_min, datetime_max):
        """ Print data base InverterPower records filtered by date"""
        self.__lock.acquire()

        current_date = date.today()
        records = self.cursor.execute(
                        "SELECT * FROM InverterPower WHERE timestamp BETWEEN ? AND ?",
                        (datetime_min,datetime_max)
                    ).fetchall()

        self.__lock.release()

        return records


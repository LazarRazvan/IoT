import sys
import json
import requests
from datetime import datetime

"""
Read data from inverter.
"""
class Inverter(object):
    """ Specific Huawei Fusion Solar request URLS """
    login_url = 'https://eu5.fusionsolar.huawei.com/thirdData/login'
    logout_url = 'https://eu5.fusionsolar.huawei.com/thirdData/logout'
    station_list_url = 'https://eu5.fusionsolar.huawei.com/thirdData/getStationList'
    station_rtime_url = 'https://eu5.fusionsolar.huawei.com/thirdData/getStationRealKpi'
    device_list_url = 'https://eu5.fusionsolar.huawei.com/thirdData/getDevList'
    device_rtime_url = 'https://eu5.fusionsolar.huawei.com/thirdData/getDevRealKpi'

    def __init__(self, username, password):
        """ Initialize connection data """

        # Login request object
        self.login_obj = {
            "userName" : username,
            "systemCode" : password
        }

        # Connection token (filled up in login step)
        self.xsrf_token = None

    def login(self):
        """ Login to Huawei OpenApi """

        # Send login request
        response = requests.post(
                                self.login_url,
                                json = self.login_obj,
                                cookies = {"web-auth" : "true", "Cookie_1" : "value"},
                                timeout = 3600
                                )

        # Inspect repsone
        json_status = json.loads(response.content)
        if json_status['success'] == False:
            raise ValueError("Inverter login error!")

        # Get session cookie (xsrf-token)
        cookies_dict = response.cookies.get_dict()
        if "XSRF-TOKEN" not in cookies_dict:
            raise ValueError("Inverter login token error!")

        self.xsrf_token = cookies_dict.get("XSRF-TOKEN")

    def get_stations_list(self):
        """ Get statations list for current user """
        plant_obj = {}

        # Send get station list request
        response = requests.post(
                                self.station_list_url,
                                json = plant_obj,
                                cookies = {"XSRF-TOKEN" : self.xsrf_token, "web-auth" : "true"},
                                headers = {"XSRF-TOKEN": self.xsrf_token},
                                timeout = 3600
        )

        # Inspect response
        json_plant = json.loads(response.content)
        if json_plant['success'] == False:
            raise ValueError("Inverter get stations list error!")

        return json_plant['data']

    def get_station_devices_list(self, station_code):
        """ Get devices list for a given station for user """
        rtime_obj = { "stationCodes" : station_code }

        # Send get station list request
        response = requests.post(
                                self.device_list_url,
                                json = rtime_obj,
                                cookies = {"XSRF-TOKEN" : self.xsrf_token, "web-auth" : "true"},
                                headers = {"XSRF-TOKEN": self.xsrf_token},
                                timeout = 3600
        )

        # Inspect response
        json_devices = json.loads(response.content)
        if json_devices['success'] == False:
            raise ValueError("Inverter get devices list error!")

        return json_devices['data']

    def get_station_data(self, station_code):
        """ Get station dictionary data for a user """
        rtime_obj = { "stationCodes" : station_code }

        # Send real time data request
        response = requests.post(
                                self.station_rtime_url,
                                json = rtime_obj,
                                cookies = {"XSRF-TOKEN" : self.xsrf_token, "web-auth" : "true"},
                                headers = {"XSRF-TOKEN": self.xsrf_token},
                                timeout = 3600
        )

        # Inspect response
        json_rtime = json.loads(response.content)
        if json_rtime['success'] == False:
            raise ValueError("Plant real time data error!")

        # Print values
        data_map = json_rtime['data'][0].get('dataItemMap')
        dict_data = {
            "day_power" : data_map.get('day_power'),
            "month_power" : data_map.get('month_power'),
            "total_power" : data_map.get('total_power'),
        }

        return dict_data

    def get_device_data(self, dev_id, dev_type):
        """ Get device dictionary data for a user (only active power) """
        rtime_obj = { "devIds" : dev_id, "devTypeId" : dev_type }

        # Send real time data request
        response = requests.post(
                                self.device_rtime_url,
                                json = rtime_obj,
                                cookies = {"XSRF-TOKEN" : self.xsrf_token, "web-auth" : "true"},
                                headers = {"XSRF-TOKEN": self.xsrf_token},
                                timeout = 3600
        )

        json_rtime = json.loads(response.content)
        if json_rtime['success'] == False:
            raise ValueError("Device real time data error!")

        data_map = json_rtime['data'][0].get('dataItemMap')
        dict_data = {
            "active_power" : data_map.get('active_power'),
        }

        return dict_data

import sys
import json
import requests

"""
Read data from inverter.
"""
class Inverter(object):
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
        self.xsrf_token = "unset"

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

        print("Plants number: %d\n" % (len(json_plant['data'])))
        for station in json_plant['data']:
            print(station)
            print("\n")

    def get_devices_list(self, station_code):
        """
        TODO: Read station list for current user.
        """
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


        print("Devices number: %d\n" % (len(json_devices['data'])))
        for dev in json_devices['data']:
            print(dev)
            print("\n")

    def get_plant_data(self, plant_code):
        """ TODO: Return """
        rtime_obj = { "stationCodes" : plant_code }

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
        print(json_rtime['data'])
        for data_obj in json_rtime['data']:
            map_obj = data_obj.get('dataItemMap')
            print ("Day power : %s" % map_obj.get('day_power'))
            print ("Month power : %s" % map_obj.get('month_power'))
            print ("Total power : %s" % map_obj.get('total_power'))
            print ("Health State : %s" % map_obj.get('real_health_state'))

        return (map_obj.get('day_power'), map_obj.get('month_power'), map_obj.get('total_power'))

    def get_device_data(self, dev_id, dev_type):
        """ TODO """
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

        print (json_rtime['data'])
        for data_obj in json_rtime['data']:
            map_obj = data_obj.get('dataItemMap')
            print ("Active power : %s" % map_obj.get('active_power'))
            print ("Reactive power : %s" % map_obj.get('reactive_power'))
            print ("Temperature : %s" % map_obj.get('temperature'))
            print ("Input Voltage : %s" % map_obj.get('pv1_u'))
            print ("Input Current : %s" % map_obj.get('pv1_i'))

        return (map_obj.get('active_power'), map_obj.get('reactive_power'), map_obj.get('temperature'), map_obj.get('pv1_u'), map_obj.get('pv1_i'))
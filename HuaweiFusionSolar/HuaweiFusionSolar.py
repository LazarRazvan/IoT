import json
import requests

"""
Northbound Interface Reference-V6 (SmartPVMS)

REST API Interface communication with Huawei Smart PV Management System of
Huawei Fusion Solar application.

Documentation:
https://support.huawei.com/enterprise/en/energy-common/imaster-neteco-pid-251993099
"""

class HuaweiFusionSolar(object):
    def __init__(self, client_name=None, client_pass=None, client_domain=None):
        """
        Connect to Huawei SmartPVMS

        Parameters:
            client_name     : Client username for SmartPVMS access.
            client_pass     : Client password for SmartPVMS access.
            client_domain   : Client domain name of the SmartPVMS system.
        """

        self.xsrf_token = None
        self.client_name = client_name
        self.client_pass = client_pass
        self.endpoint = f'https://{client_domain}'

        # Perform login to get xsrf-token
        self.login()

    def login(self):
        """
        Login and extract XSRF-TOKEN for next requests.

        Request URL: https://<domain>/thirdData/login
        Request Method: POST
        Request Parameters:
            - userName
                Username. String. Mandatory
            - systemCode
                Password. String. Mandatory
        """
        # Request URL
        COMMAND_URL = f'{self.endpoint}/thirdData/login'

        # Request parameters
        data = {
            "userName" : self.client_name,
            "systemCode" : self.client_pass
        }

        # Send request
        response = requests.post(COMMAND_URL, json=data)
        json_response = json.loads(response.content)
        if json_response['success'] == False:
            raise ValueError("Login error (%s: %s)" % (json_response['failCode'], json_response['message']))

        # Set the xsrf-token
        self.xsrf_token = response.headers['xsrf-token']


    def logout(self):
        """
        Force the XSRF-TOKEN to expire immediately.

        Request URL: https://<domain>/thirdData/logout
        Request Method: POST
        Request Parameters:
            - xsrfToken
                Token from login respons header. String. Mandatory
        """
        # Request URL
        COMMAND_URL = f'{self.endpoint}/thirdData/logout'

        # Request parameters
        data = {
            "xsrfToken" : self.xsrf_token
        }

        # Send request
        response = requests.post(COMMAND_URL, json=data)
        json_response = json.loads(response.content)
        if json_response['success'] == False:
            raise ValueError("Logout error (%s: %s)" % (json_response['failCode'], json_response['message']))


    def plant_list(self, pageNo, startTime=None, endTime=None):
        """
        Get the plant list. Maximum API calls per day:
        Roundup(nr_plants/100) x 10 + 25

        Request URL: https://<domain>/thirdData/stations
        Request Mode: POST
        Request Parameters:
            - pageNo
                Page numbers for the results. Integer. Mandatroy
            - gridConnectedStartTime
                Time in miliseconds. Long. Optional
            - gridConnectedEndTime
                Time in miliseconds. Long. Optional

        On success, method return all 'data' returned by request.
        """
        # Request URL
        COMMAND_URL = f'{self.endpoint}/thirdData/stations'

        # Request parameters
        data = { "pageNo" : pageNo }

        if startTime is not None:
            data['gridConnectedStartTime'] = startTime
        if endTime is not None:
            data['gridConnectedEndTime'] = endTime

        # Request headers
        header = { "XSRF-TOKEN" : self.xsrf_token }

        # Send request
        response = requests.post(COMMAND_URL, headers=header, json=data)
        json_response = json.loads(response.content)
        if json_response['success'] == False:
            raise ValueError("Plant list interfaceerror (%s: %s)" %
                        (json_response['failCode'], json_response['message']))

        return json_response['data']


    def plant_real_time_data(self, stationCodes):
        """
        Get real time data for one or multiple plants. Maximum API calls per
        user every 5 minutes:
        Roundup (Number of plants/100)

        Request URL: https://<domain>/thirdData/getStationRealKpi
        Request Mode: POST
        Request Parameters:
            - stationCodes
                Plants ids seppareted by comma. String. Mandatory

        On success, method return all 'data' returned by request.
        """
        # Request URL
        COMMAND_URL = f'{self.endpoint}/thirdData/getStationRealKpi'

        # Request parameters
        data = { "stationCodes" : stationCodes }

        # Request headers
        header = { "XSRF-TOKEN" : self.xsrf_token }

        # Send request
        response = requests.post(COMMAND_URL, headers=header, json=data)
        json_response = json.loads(response.content)
        if json_response['success'] == False:
            raise ValueError("Plant real-time data interface error (%s: %s)" %
                        (json_response['failCode'], json_response['message']))

        return json_response['data']


    def plant_hourly_data(self, stationCodes, collectTime):
        """
        Get hourly data for one or multiple plants. Maximum API calls day:
        Roundup (Number of plants/100) + 24

        Request URL: https://<domain>/thirdData/getKpiStationHour
        Request Mode: POST
        Request Parameters:
            - stationCodes
                Plants ids seppareted by comma. String. Mandatory
            - collectTime
                Time in miliseconds. Long. Mandatory

        On success, method return all 'data' returned by request.
        """
        # Request URL
        COMMAND_URL = f'{self.endpoint}/thirdData/getKpiStationHour'

        # Request parameters
        data = { "stationCodes" : stationCodes, "collectTime" : collectTime }

        # Request headers
        header = { "XSRF-TOKEN" : self.xsrf_token }

        # Send request
        response = requests.post(COMMAND_URL, headers=header, json=data)
        json_response = json.loads(response.content)
        if json_response['success'] == False:
            raise ValueError("Plant hourly data interface error (%s: %s)" %
                        (json_response['failCode'], json_response['message']))

        return json_response['data']


    def plant_daily_data(self, stationCodes, collectTime):
        """
        Get daily data for one or multiple plants. Maximum API calls day:
        Roundup (Number of plants/100) + 24

        Request URL: https://<domain>/thirdData/getKpiStationDay
        Request Mode: POST

        Request Parameters:
            - stationCodes
                Plants ids seppareted by comma. String. Mandatory
            - collectTime
                Time in miliseconds. Long. Mandatory

        On success, method return all 'data' returned by request.
        """
        # Request URL
        COMMAND_URL = f'{self.endpoint}/thirdData/getKpiStationDay'

        # Request parameters
        data = { "stationCodes" : stationCodes, "collectTime" : collectTime }

        # Request headers
        header = { "XSRF-TOKEN" : self.xsrf_token }

        # Send request
        response = requests.post(COMMAND_URL, headers=header, json=data)
        json_response = json.loads(response.content)
        if json_response['success'] == False:
            raise ValueError("Plant daily data interface error (%s: %s)" %
                        (json_response['failCode'], json_response['message']))

        return json_response['data']


    def plant_monthly_data(self, stationCodes, collectTime):
        """
        Get monthly data for one or multiple plants. Maximum API calls day:
        Roundup (Number of plants/100) + 24

        Request URL: https://<domain>/thirdData/getKpiStationMonth
        Request Mode: POST

        Request Parameters:
            - stationCodes
                Plants ids seppareted by comma. String. Mandatory
            - collectTime
                Time in miliseconds. Long. Mandatory

        On success, method return all 'data' returned by request.
        """
        # Request URL
        COMMAND_URL = f'{self.endpoint}/thirdData/getKpiStationMonth'

        # Request parameters
        data = { "stationCodes" : stationCodes, "collectTime" : collectTime }

        # Request headers
        header = { "XSRF-TOKEN" : self.xsrf_token }

        # Send request
        response = requests.post(COMMAND_URL, headers=header, json=data)
        json_response = json.loads(response.content)
        if json_response['success'] == False:
            raise ValueError("Plant monthly data interface error (%s: %s)" %
                        (json_response['failCode'], json_response['message']))

        return json_response['data']


    def plant_yearly_data(self, stationCodes, collectTime):
        """
        Get yearly data for one or multiple plants. Maximum API calls day:
        Roundup (Number of plants/100) + 24

        Request URL: https://<domain>/thirdData/getKpiStationYear
        Request Mode: POST

        Request Parameters:
            - stationCodes
                Plants ids seppareted by comma. String. Mandatory
            - collectTime
                Time in miliseconds. Long. Mandatory

        On success, method return all 'data' returned by request.
        """
        # Request URL
        COMMAND_URL = f'{self.endpoint}/thirdData/getKpiStationYear'

        # Request parameters
        data = { "stationCodes" : stationCodes, "collectTime" : collectTime }

        # Request headers
        header = { "XSRF-TOKEN" : self.xsrf_token }

        # Send request
        response = requests.post(COMMAND_URL, headers=header, json=data)
        json_response = json.loads(response.content)
        if json_response['success'] == False:
            raise ValueError("Plant yearly data interface error (%s: %s)" %
                        (json_response['failCode'], json_response['message']))

        return json_response['data']


    def device_list(self, stationCodes):
        """
        Get devices information associated with a given plant. Maximum API calls
        per day:
        Roundup (Number of plants/100) + 24

        Request URL: https://<domain>/thirdData/getDevList
        Request Mode: POST
        Request Parameters:
            - stationCodes
                Plants ids seppareted by comma. String. Mandatory

        On success, method return all 'data' returned by request.
        """
        # Request URL
        COMMAND_URL = f'{self.endpoint}/thirdData/getDevList'

        # Request parameters
        data = { "stationCodes" : stationCodes }

        # Request headers
        header = { "XSRF-TOKEN" : self.xsrf_token }

        # Send request
        response = requests.post(COMMAND_URL, headers=header, json=data)
        json_response = json.loads(response.content)
        if json_response['success'] == False:
            raise ValueError("Plant daily data interface error (%s: %s)" %
                        (json_response['failCode'], json_response['message']))

        return json_response['data']


    def device_real_time_data(self, devTypeId, devIds=None, sns=None):
        """
        Get real time data for one or multiple devices of the same type.
        Maximum API calls per user every 5 minutes:
        Sum (Roundup (No. devices of same type/100) )

        Request URL: https://<domain>/thirdData/getDevRealKpi
        Request Mode: POST
        Request Parameters:
            - devIds
                Device ids of the same type sepparated by comma. String. Optional
            - sns
                Device sns of the same type sepparated by comma. String. Optional
            - devTypeId
                Device type. Integer. Mandatory

        On success, method return all 'data' returned by request.
        """
        # Request URL
        COMMAND_URL = f'{self.endpoint}/thirdData/getDevRealKpi'

        # Either sns or devIds must be set
        if devIds is None and sns is None:
            return

        # Request parameters
        data = { "devTypeId" : devTypeId }
        if devIds is not None:
            data['devIds'] = devIds
        if sns is not None:
            data['sns'] = sns

        # Request headers
        header = { "XSRF-TOKEN" : self.xsrf_token }

        # Send request
        response = requests.post(COMMAND_URL, headers=header, json=data)
        json_response = json.loads(response.content)
        if json_response['success'] == False:
            raise ValueError("Device real-time data interface error (%s: %s)" %
                        (json_response['failCode'], json_response['message']))

        return json_response['data']


    def device_history_data(self, devTypeId, startTime, endTime, devIds=None, sns=None):
        """
        Get history data for one or multiple devices of the same type.
        Maximum API calls per user per day:
        Sum (Roundup (No. devices of same type/100) ) + 24

        Request URL: https://<domain>/thirdData/getDevHistoryKpi
        Request Mode: POST
        Request Parameters:
            - devIds
                Device ids of the same type sepparated by comma. String. Optional
            - sns
                Device sns of the same type sepparated by comma. String. Optional
            - devTypeId
                Device type. Integer. Mandatory
            - startTime
                Time in miliseconds. Long. Mandatory
            - endTime
                Time in miliseconds. Long. Mandatory

        On success, method return all 'data' returned by request.
        """
        # Request URL
        COMMAND_URL = f'{self.endpoint}/thirdData/getDevHistoryKpi'

        # Either sns or devIds must be set
        if devIds is None and sns is None:
            return

        # Request parameters
        data = { "devTypeId" : devTypeId, "startTime" : startTime, "endTime" : endTime }
        if devIds is not None:
            data['devIds'] = devIds
        if sns is not None:
            data['sns'] = sns

        # Request headers
        header = { "XSRF-TOKEN" : self.xsrf_token }

        # Send request
        response = requests.post(COMMAND_URL, headers=header, json=data)
        json_response = json.loads(response.content)
        if json_response['success'] == False:
            raise ValueError("Device history data interface error (%s: %s)" %
                        (json_response['failCode'], json_response['message']))

        return json_response['data']


    def device_daily_data(self, devTypeId, collectTime, devIds=None, sns=None):
        """
        Get daily data for one or multiple devices of the same type.
        Maximum API calls per user per day:
        Sum (Roundup (No. devices of same type/100) ) + 24

        Request URL: https://<domain>/thirdData/getDevKpiDay
        Request Mode: POST
        Request Parameters:
            - devIds
                Device ids of the same type sepparated by comma. String. Optional
            - sns
                Device sns of the same type sepparated by comma. String. Optional
            - devTypeId
                Device type. Integer. Mandatory
            - collectTime
                Time in miliseconds. Long. Mandatory

        On success, method return all 'data' returned by request.
        """
        # Request URL
        COMMAND_URL = f'{self.endpoint}/thirdData/getDevKpiDay'

        # Either sns or devIds must be set
        if devIds is None and sns is None:
            return

        # Request parameters
        data = { "devTypeId" : devTypeId, "collectTime" : collectTime }
        if devIds is not None:
            data['devIds'] = devIds
        if sns is not None:
            data['sns'] = sns

        # Request headers
        header = { "XSRF-TOKEN" : self.xsrf_token }

        # Send request
        response = requests.post(COMMAND_URL, headers=header, json=data)
        json_response = json.loads(response.content)
        if json_response['success'] == False:
            raise ValueError("Device real-time data interface error (%s: %s)" %
                        (json_response['failCode'], json_response['message']))

        return json_response['data']


    def device_monthly_data(self, devTypeId, collectTime, devIds=None, sns=None):
        """
        Get monthly data for one or multiple devices of the same type.
        Maximum API calls per user per day:
        Sum (Roundup (No. devices of same type/100) ) + 24

        Request URL: https://<domain>/thirdData/getDevKpiMonth
        Request Mode: POST
        Request Parameters:
            - devIds
                Device ids of the same type sepparated by comma. String. Optional
            - sns
                Device sns of the same type sepparated by comma. String. Optional
            - devTypeId
                Device type. Integer. Mandatory
            - collectTime
                Time in miliseconds. Long. Mandatory

        On success, method return all 'data' returned by request.
        """
        # Request URL
        COMMAND_URL = f'{self.endpoint}/thirdData/getDevKpiMonth'

        # Either sns or devIds must be set
        if devIds is None and sns is None:
            return

        # Request parameters
        data = { "devTypeId" : devTypeId, "collectTime" : collectTime }
        if devIds is not None:
            data['devIds'] = devIds
        if sns is not None:
            data['sns'] = sns

        # Create request headers
        header = { "XSRF-TOKEN" : self.xsrf_token }

        # Send request
        response = requests.post(COMMAND_URL, headers=header, json=data)
        json_response = json.loads(response.content)
        if json_response['success'] == False:
            raise ValueError("Device monthly data interface error (%s: %s)" %
                        (json_response['failCode'], json_response['message']))

        return json_response['data']


    def device_yearly_data(self, devTypeId, collectTime, devIds=None, sns=None):
        """
        Get yearly data for one or multiple devices of the same type.
        Maximum API calls per user per day:
        Sum (Roundup (No. devices of same type/100) ) + 24

        Request URL: https://<domain>/thirdData/getDevKpiYear
        Request Mode: POST
        Request Parameters:
            - devIds
                Device ids of the same type sepparated by comma. String. Optional
            - sns
                Device sns of the same type sepparated by comma. String. Optional
            - devTypeId
                Device type. Integer. Mandatory
            - collectTime
                Time in miliseconds. Long. Mandatory

        On success, method return all 'data' returned by request.
        """
        # Request URL
        COMMAND_URL = f'{self.endpoint}/thirdData/getDevKpiYear'

        # Either sns or devIds must be set
        if devIds is None and sns is None:
            return

        # Request parameters
        data = { "devTypeId" : devTypeId, "collectTime" : collectTime }
        if devIds is not None:
            data['devIds'] = devIds
        if sns is not None:
            data['sns'] = sns

        # Request headers
        header = { "XSRF-TOKEN" : self.xsrf_token }

        # Send request
        response = requests.post(COMMAND_URL, headers=header, json=data)
        json_response = json.loads(response.content)
        if json_response['success'] == False:
            raise ValueError("Device real-time data interface error (%s: %s)" %
                        (json_response['failCode'], json_response['message']))

        return json_response['data']

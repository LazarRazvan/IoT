import json
import uuid
import hmac
import time
import hashlib
import requests

"""
TuyaCloud is designed as a main class for specific Tuya compatible devices
(ex: TuyaSwitch) implementing the main methods for each device.

Class main methods are built to connect with Tuya IoT Cloud Platform
https://iot.tuya.com/

1) init
    Set the API endpoint (TUYA_ENDPOINTS) based on user selected region and get
    the access token to be used for communication (note that this expires and
    has to be refreshed)

2) __create_signature (dunder method)
    Create the signature for each request perform by a Tuya Device.

3) __create_string_to_sign (dunder method)
    Create the stringToSign required in signature computation

4) __create_request_headers (dunder method)
    Create the headers for a given request.

5) command
    Send a custom command to a Tuya device using POST request

6) get_devices
    Return a list with all devices associated with current user.

7) get_device_status
    Return device status as json.

7) print_devices
    Print the list returned by get_devices method
"""

################################################################################
# Tuya Enpoints
# https://developer.tuya.com/en/docs/iot/api-request?id=Ka4a8uuo1j4t4)
################################################################################
TUYA_ENDPOINTS = {
    "cn" : "https://openapi.tuyacn.com",
    "w-us" : "https://openapi.tuyaus.com",
    "e-us" : "https://openapi-ueaz.tuyaus.com",
    "eu" : "https://openapi.tuyaeu.com",
    "w-eu" : "https://openapi-weaz.tuyaeu.com",
    "in" : "https://openapi.tuyain.com"
}

################################################################################
# Empty request body encryption
# https://developer.tuya.com/en/docs/iot/api-request?id=Ka4a8uuo1j4t4)
################################################################################
EMPTY_BODY_ENCRYPTION = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

################################################################################
# Token expired error code
# https://developer.tuya.com/en/docs/iot/error-code?id=K989ruxx88swc
#
# When this error code is returned by a request, the access token has to be
# refreshed.
################################################################################
INVALID_TOKEN = 1010

class TuyaCloud(object):
    def __init__(self, client_region=None, client_id=None, client_secret=None, device_id=None):
        """
        Connect to Tuya Iot Cloud

        Parameters:
            client_region   : Region (cn|w-us|e-us|eu|w-eu|in)
            client_id       : Client id (Cloud > "Project" > Authorization Ket > Access ID/Client ID)
            client_secret   : Client id (Cloud > "Project" > Authorization Ket > Access Secret/Client Secret)
            device_id       : Tuya device id (set by particular classes that inherit this class)
        """

        self.device_id = device_id
        self.client_id = client_id
        self.access_token = None
        self.client_secret = client_secret
        self.client_region = client_region

        # Region validation
        if self.client_region not in TUYA_ENDPOINTS:
            raise ValueError("Invalid value for client region")

        self.endpoint = TUYA_ENDPOINTS[self.client_region]

        # Get access token
        self.refresh_access_token()


    def __create_signature(self, t, stringToSign, refresh_token=False):
        """
        Build the request signature.
        https://developer.tuya.com/en/docs/iot/new-singnature?id=Kbw0q34cs2e5g

        Token management API:
            str = client_id + t + stringToSign
            sign = HMAC-SHA256(str, secret).toUpperCase()

        General business API:
            str = client_id + access_token + t + stringToSign
            sign = HMAC-SHA256(str, secret).toUpperCase()
        """

        if refresh_token:
            data = self.client_id + t + stringToSign
        else:
            data = self.client_id + self.access_token + t + stringToSign

        return hmac.new(
                        self.client_secret.encode('UTF-8'),
                        data.encode('UTF-8'),
                        hashlib.sha256
                    ).hexdigest().upper()


    def __create_string_to_sign(self, method, content, headers, url):
        """
        Build the stringToSign for request signature.
        https://developer.tuya.com/en/docs/iot/new-singnature?id=Kbw0q34cs2e5g

        String stringToSign=
            HTTPMethod + "\n" +
            Content-SHA256 + "\n" +
            Headers + "\n" +
            URL
        """
        content_sha256 = None
        header_sorted = None

        # Create content
        if content is None:
            content_sha256 = EMPTY_BODY_ENCRYPTION
        else:
            content_sha256 = hashlib.sha256(content.encode('UTF-8')).hexdigest()

        # Create headers (all request headers involved in signature calculation)
        headers_sorted = ''.join([f'{key}:{headers[key]}\n'
                            for key in sorted(headers.keys())])

        return f'{method}\n{content_sha256}\n{headers_sorted}\n{url}'


    def __create_request_headers(self, signature, t):
        """
        Create the headers for a given request.
        https://developer.tuya.com/en/docs/iot/api-request?id=Ka4a8uuo1j4t4
        """
        return {
            "client_id" : self.client_id,
            "secret" : self.client_secret,
            "sign" : signature,
            "t" : t,
            "access_token" : self.access_token,
            "sign_method" : "HMAC-SHA256",
            "Signature-Headers" : "area_id:call_id",
            "area_id" : self.area_id,
            "call_id" : self.call_id
        }

    def command(self, content=None):
        """
        Send a command to a Tuya device.
        https://developer.tuya.com/en/docs/cloud/e2512fb901?id=Kag2yag3tiqn5
        """
        _URL = f'/v1.0/iot-03/devices/{self.device_id}/commands'
        time_now = str(int(time.time() * 1000))
        COMMAND_URL = f'{self.endpoint}{_URL}'

        # Create signature (use body encryption)
        signature_headers = {
            "area_id" : self.area_id,
            "call_id" : self.call_id
        }
        stringToSign = self.__create_string_to_sign(
                                        method  = "POST",
                                        content = content,
                                        headers = signature_headers,
                                        url     = _URL
                                    )

        signature = self.__create_signature(t=time_now, stringToSign=stringToSign)

        # Create request headers
        headers = self.__create_request_headers(signature, time_now)

        # Send request
        response = requests.post(COMMAND_URL, headers = headers, data = content)
        json_response = json.loads(response.content)
        if json_response['success'] == False:
            # If token has expired, refresh it
            errcode = int(json_response['code'])
            if errcode == INVALID_TOKEN:
                print("Access token expired! Refresh it!")
                self.refresh_access_token()
                return self.command(content=content)
            else:
                raise ValueError("Unable to send command (%s: %s)" %
                                (json_response['code'], json_response['msg']))


    def refresh_access_token(self):
        """
        Get Tuya IoT access token (a signature to verify the identity)
        https://developer.tuya.com/en/docs/iot/new-singnature?id=Kbw0q34cs2e5g
        """
        _URL = "/v1.0/token?grant_type=1"
        time_now = str(int(time.time() * 1000))
        ACCESS_TOKEN_URL = f'{self.endpoint}{_URL}'

        # Set area id and call id (used for signature calculation)
        self.area_id = time_now
        self.call_id = str(uuid.uuid4())

        # Create signature (use encryption for empty body)
        signature_headers = {
            "area_id" : self.area_id,
            "call_id" : self.call_id
        }
        stringToSign = self.__create_string_to_sign(
                                        method  = "GET",
                                        content = None,
                                        headers = signature_headers,
                                        url     = _URL
                                    )
        signature = self.__create_signature(t=time_now,stringToSign=stringToSign,refresh_token=True)

        # Create request headers
        headers = self.__create_request_headers(signature, time_now)

        # Send request
        response = requests.get(ACCESS_TOKEN_URL, headers = headers)
        json_response = json.loads(response.content)
        if json_response['success'] == False:
            raise ValueError("Access token refresh error (%s: %s)" % (json_response['code'], json_response['msg']))

        # Get access token
        self.access_token = json_response['result']['access_token']


    def get_devices(self):
        """
        Get Tuya devices for current user.
        """
        _URL = "/v1.0/iot-01/associated-users/devices"
        time_now = str(int(time.time() * 1000))
        DEVICES_URL = f'{self.endpoint}{_URL}'

        # Create signature (use encryption for empty body)
        signature_headers = {
            "area_id" : self.area_id,
            "call_id" : self.call_id
        }
        stringToSign = self.__create_string_to_sign(
                                        method  = "GET",
                                        content = None,
                                        headers = signature_headers,
                                        url     = _URL
                                    )

        signature = self.__create_signature(t=time_now, stringToSign=stringToSign)

        # Create request headers
        headers = self.__create_request_headers(signature, time_now)

        # Send request
        response = requests.get(DEVICES_URL, headers = headers)
        json_response = json.loads(response.content)
        if json_response['success'] == False:
            # If token has expired, refresh it
            errcode = int(json_response['code'])
            if errcode == INVALID_TOKEN:
                print("Access token expired! Refresh it!")
                self.refresh_access_token()
                return self.get_devices()
            else:
                raise ValueError("Unable to get devices list (%s: %s)" %
                                (json_response['code'], json_response['msg']))

        return json_response['result']['devices']


    def get_device_status(self):
        """
        Get single device status.
        https://developer.tuya.com/en/docs/cloud/f76865b055?id=Kag2ycn1lvwpt
        """
        _URL = f'/v1.0/iot-03/devices/{self.device_id}/status'
        time_now = str(int(time.time() * 1000))
        DEVICE_STATUS_URL = f'{self.endpoint}{_URL}'

        # Create signature (use encryption for empty body)
        signature_headers = {
            "area_id" : self.area_id,
            "call_id" : self.call_id
        }
        stringToSign = self.__create_string_to_sign(
                                        method  = "GET",
                                        content = None,
                                        headers = signature_headers,
                                        url     = _URL
                                    )

        signature = self.__create_signature(t=time_now, stringToSign=stringToSign)

        # Create request headers
        headers = self.__create_request_headers(signature, time_now)

        # Send request
        response = requests.get(DEVICE_STATUS_URL, headers = headers)
        json_response = json.loads(response.content)
        if json_response['success'] == False:
            # If token has expired, refresh it
            errcode = int(json_response['code'])
            if errcode == INVALID_TOKEN:
                print("Access token expired! Refresh it!")
                self.refresh_access_token()
                return self.get_devices()
            else:
                raise ValueError("Unable to get device status (%s: %s)" %
                                (json_response['code'], json_response['msg']))

        return json_response['result']


    def print_devices(self):
        """
        Print all devices for current user (get_devices)
        """
        device_idx = 1
        json_devices = self.get_devices()

        print("Devices list:")
        for device in json_devices:
            print("\tDevice %d:" % (device_idx))
            print(device)
            device_idx += 1


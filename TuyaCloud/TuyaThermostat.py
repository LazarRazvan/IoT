import json
import time
import hmac
import hashlib
import requests
from TuyaCloud import TuyaCloud

"""
TuyaThermostat is designed to control temperature for thermostats compatible
with Tuya App.

Class has the following methods:

    1) turn_on
        Turn the thermostat on.

    2) turn_off
        Turn the thermostat off.

    3) window_check_on
        Turn on open window detection.

    4) window_check_off
        Turn off open window detection.

    5) frost_on
        Turn on frost protection.

    6) frost_off
        Turn off frost protection.

    7) get_room_temperature
        Get room temperature.

    8) get_trigger_temperature
        Get trigger temperature.

    9) set_trigger_temperature
        Set trigger temperature.
"""

class TuyaThermostat(TuyaCloud):
    def __init__(self, client_region=None, client_id=None, client_secret=None, device_id=None, log_file=None):
        # Call constructor for TuyaCloud (to ensure API communication)
        super().__init__(client_region, client_id, client_secret, device_id, log_file)

    def turn_on(self):
        """
        Turn on thermostat.

        Ex:
            obj.turn_on()
        """

        # Create request body
        body = {'commands':{'code': 'switch', 'value': True}}
        try:
            super().command(content=json.dumps(body))
        except ValueError as e:
            print(f'Error: {e}')
            return

    def turn_off(self):
        """
        Turn on thermostat.

        Ex:
            obj.turn_off()
        """

        # Create request body
        body = {'commands':{'code': 'switch', 'value': False}}
        try:
            super().command(content=json.dumps(body))
        except ValueError as e:
            print(f'Error: {e}')
            return

    def window_check_on(self):
        """
        Turn on open window detection.

        Ex:
            obj.window_check()
        """

        # Create request body
        body = {'commands':{'code': 'window_check', 'value': True}}
        try:
            super().command(content=json.dumps(body))
        except ValueError as e:
            print(f'Error: {e}')
            return

    def window_check_off(self):
        """
        Turn off open window detection.

        Ex:
            obj.window_check_off()
        """

        # Create request body
        body = {'commands':{'code': 'window_check', 'value': False}}
        try:
            super().command(content=json.dumps(body))
        except ValueError as e:
            print(f'Error: {e}')
            return

    def frost_on(self):
        """
        Turn on frost protection.

        Ex:
            obj.frost()
        """

        # Create request body
        body = {'commands':{'code': 'frost', 'value': True}}
        try:
            super().command(content=json.dumps(body))
        except ValueError as e:
            print(f'Error: {e}')
            return

    def frost_off(self):
        """
        Turn off frost protection.

        Ex:
            obj.frost_off()
        """

        # Create request body
        body = {'commands':{'code': 'frost', 'value': False}}
        try:
            super().command(content=json.dumps(body))
        except ValueError as e:
            print(f'Error: {e}')
            return

    def get_room_temperature(self):
        """
        Get room temperature.

        Ex:
            obj.get_room_temperature()
        """

        # Get status
        status = self.get_status()

        # Parse 'temp_current'
        return status.get('temp_current', -1)

    def get_trigger_temperature(self):
        """
        Get trigger temperature.

        Ex:
            obj.get_trigger_temperature()
        """

        # Get status
        status = self.get_status()

        # Parse 'temp_set'
        return status.get('temp_set', -1)

    def set_trigger_temperature(self, temp):
        """
        Set trigger temperature.

        Ex:
            obj.set_trigger_temperature(240)
        """

        # Create request body
        body = {'commands':{'code': 'temp_set', 'value': temp}}
        try:
            super().command(content=json.dumps(body))
        except ValueError as e:
            print(f'Error: {e}')
            return

    def get_status(self):
        """
        Get status of switch(es).

        Ex:
            obj.get_status()
        """

        # Get status
        device_status_dict = super().get_device_status()

        # Create return
        result_status = {}
        for d in device_status_dict:
            result_status[d['code']] = d['value']

        return result_status

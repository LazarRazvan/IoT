import json
import time
import hmac
import hashlib
import requests
from TuyaCloud import TuyaCloud

"""
TuyaSwitch is designed to control multi-button smart switches compatible with
Tuya App.

Class has the following methods:

    1) turn_on
        Allow turning on multiple switches specified by name in the switch_list
        input parameter.

    2) turn_off
        Allow turning off multiple switches specified by name in the switch_list
        input parameter.

    3) turn_cusom
        Allow custom actions at once for multiple switches specified by name and
        vale (action) in the switch_dict input parameter.

    4) get_status
        Get switch device status.
"""

class TuyaSwitch(TuyaCloud):
    def __init__(self, client_region=None, client_id=None, client_secret=None, device_id=None):
        # Call constructor for TuyaCloud (to ensure API communication)
        super().__init__(client_region, client_id, client_secret, device_id)

    def turn_on(self, switch_list=None):
        """
        Turn on switch(es).

        Parameters:
            switch_list  : List with switches names to be turned on.

        Ex:
            obj.turn_on(['switch_1','switch_2'])
        """

        if switch_list is None:
            return

        # Create request body
        switch_body = {'commands':[{'code': key, 'value': True} for key in switch_list]}
        super().command(content=json.dumps(switch_body))

    def turn_off(self, switch_list=None):
        """
        Turn on switch(es).

        Parameters:
            switch_list  : List with switches names to be turned off.

        Ex:
            obj.turn_off(['switch_1','switch_2'])
        """

        if switch_list is None:
            return

        # Create request body
        switch_body = {'commands':[{'code': key, 'value': False} for key in switch_list]}
        super().command(content=json.dumps(switch_body))

    def turn_custom(self, switch_dict=None):
        """
        Turn custom switch.

        Parameters:
            switch_dict : Dictionary with switch name as key and the action
                          (True/False) as value.
        """

        if switch_dict is None:
            return

        # Create request body
        switch_body = {'commands':[{'code': key, 'value': value} for key,value in switch_dict.items()]}
        super().command(content=json.dumps(switch_body))

    def get_status(self, switch_list=None):
        """
        Get status of switch(es).

        Parameters:
            switch_list  : List with switches names to get status.

        Ex:
            obj.get_status(['switch_1','switch_2'])
        """
        if switch_list is None:
            return

        # Get status
        device_status_dict = super().get_device_status()

        # Create return
        result_status = {}
        for d in device_status_dict:
            if d['code'] in switch_list:
                result_status[d['code']] = d['value']

        return result_status

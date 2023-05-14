
from HuaweiFusionSolar import HuaweiFusionSolar

"""
HuaweiInverter is designed to extract infromation for inverter devices that are
compatible with Huawei SmartPVMS.

There are two types of inverters:
    1) String Inverter          Device Type: 1
    2) Residential Inverter     Device Type: 38
"""

################################################################################
# Huawei Inverter Type
################################################################################
DEVICE_TYPE = {
    "string" : 1,
    "residential" : 38
}

class HuaweiInverter(HuaweiFusionSolar):
    def __init__(self, client_name=None, client_pass=None, client_domain=None, device_type=None, device_id=None):
        """
        Connect to Huawei SmartPVMS

        Parameters:
            client_name     : Client username for SmartPVMS access.
            client_pass     : Client password for SmartPVMS access.
            client_domain   : Client domain name of the SmartPVMS system.
            device_type     : Inverter device type ("string" | "residential")
            device_id       : Inverter device id.
        """
        self.device_id = device_id
        self.device_type = device_type

        # Validate device_type
        if device_type not in DEVICE_TYPE:
            raise ValueError("Invalid value for device type!")

        self.device_type = DEVICE_TYPE[device_type]

        # Call constructor for HuaweiFusionSolar
        super().__init__(client_name, client_pass, client_domain)


    def real_time_data(self):
        """
        Get inverter real time data.
        """
        return super().device_real_time_data(self.device_type,
                                            devIds = self.device_id)


    def daily_data(self, collectTime):
        """
        Get inverter daily data.
        """
        return super().device_daily_data(self.device_type, collectTime,
                                        devIds = self.device_id)


    def monthly_data(self, collectTime):
        """
        Get inverter monthly data.
        """
        return super().device_monthly_data(self.device_type, collectTime,
                                        devIds = self.device_id)


    def yearly_data(self, collectTime):
        """
        Get inverter yearly data.
        """
        return super().device_yearly_data(self.device_type, collectTime,
                                        devIds = self.device_id)

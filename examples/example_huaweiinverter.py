import sys
import time
sys.path.append('../HuaweiFusionSolar')

from HuaweiInverter import HuaweiInverter

# TODO: add client_name, client_password and client_domain, plant_id
# device_id and device_type
CLIENT_NAME = 'TODO'
CLIENT_PASS = 'TODO'
CLIENT_DOMAIN = 'TODO'
DEVICE_ID = 'TODO'
DEVICE_TYPE = 'TODO'    # residential or string

obj = HuaweiInverter(
                    client_name=CLIENT_NAME,
                    client_pass=CLIENT_PASS,
                    client_domain=CLIENT_DOMAIN,
                    device_type=DEVICE_TYPE,
                    device_id=DEVICE_ID
                    )

current_time_ms = int(time.time() * 1000)

print("Inverter real time active power:")
print(obj.real_time_active_power())

print("Inverter daily data:")
print(obj.daily_data(current_time_ms))

print("Inverter monthly data:")
print(obj.monthly_data(current_time_ms))

print("Inverter yearly data:")
print(obj.yearly_data(current_time_ms))

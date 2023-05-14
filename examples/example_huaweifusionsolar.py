import sys
import time
sys.path.append('../HuaweiFusionSolar')

from HuaweiFusionSolar import HuaweiFusionSolar

# TODO: add client_name, client_password and client_domain, plant_id
# device_id and device_type
CLIENT_NAME = 'TODO'
CLIENT_PASS = 'TODO'
CLIENT_DOMAIN = 'TODO'
PLANT_ID = 'TODO'
DEVICE_ID = 'TODO'
DEVICE_TYPE = 'TODO'    # integer value

obj = HuaweiFusionSolar(
                        client_name=CLIENT_NAME,
                        client_pass=CLIENT_PASS,
                        client_domain=CLIENT_DOMAIN
                        )

print("Plant list:")
print(obj.plant_list(1))

print("Plant real-time data:")
print(obj.plant_real_time_data(PLANT_ID))

current_time_ms = int(time.time() * 1000)

print("Plant hourly data:")
print(obj.plant_hourly_data(PLANT_ID, current_time_ms))

print("Plant daily data:")
print(obj.plant_daily_data(PLANT_ID, current_time_ms))

print("Plant monthly data:")
print(obj.plant_monthly_data(PLANT_ID, current_time_ms))

print("Plant yearly data:")
print(obj.plant_yearly_data(PLANT_ID, current_time_ms))

print("Device list:")
print(obj.device_list(PLANT_ID))

print("Device real-time data:")
print(obj.device_real_time_data(DEVICE_TYPE, devIds=DEVICE_ID))

print("Device daily data:")
print(obj.device_daily_data(DEVICE_TYPE, current_time_ms, devIds=DEVICE_ID))

print("Device monthly data:")
print(obj.device_monthly_data(DEVICE_TYPE, current_time_ms, devIds=DEVICE_ID))

print("Device yearly data:")
print(obj.device_yearly_data(DEVICE_TYPE, current_time_ms, devIds=DEVICE_ID))

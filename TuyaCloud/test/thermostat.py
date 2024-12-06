import sys
import time
sys.path.append('../TuyaCloud')

from TuyaThermostat import TuyaThermostat
from TuyaCloud import TuyaCloud

# TODO: add client_id, client_secret and device_id
CLIENT_REGION = 'TODO'
CLIENT_ID = 'TODO'
CLIENT_SECRET = 'TODO'
DEVICE_ID = 'TODO'

# Connect a Tuya Switch device
obj = TuyaThermostat(
                client_region=CLIENT_REGION,
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                device_id=DEVICE_ID
            )

print("Turning thermostat on...")
obj.turn_on()

print("Sleep 5 seconds...")
time.sleep(5)

print("Turning thermostat off...")
obj.turn_off()

print("Get status...")
print(obj.get_status())

print("Enable open window detection...")
obj.window_check_on()

print("Sleep 5 seconds...")
time.sleep(5)

print("Disable open window detection...")
obj.window_check_off()

print("Sleep 5 seconds...")
time.sleep(5)

print("Enable frost protection...")
obj.frost_on()

print("Sleep 5 seconds...")
time.sleep(5)

print("Disable frost protection...")
obj.frost_off()

print("Sleep 5 seconds...")
time.sleep(5)

print("Sleep 5 seconds...")
time.sleep(5)

print("Get room temperature...")
print(obj.get_room_temperature())

print("Sleep 5 seconds...")
time.sleep(5)

print("Get trigger temperature...")
print(obj.get_trigger_temperature())

print("Sleep 5 seconds...")
time.sleep(5)

print("Set trigger temperature...")
obj.set_trigger_temperature(10000)

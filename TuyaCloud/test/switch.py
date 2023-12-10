import sys
import time
sys.path.append('../TuyaCloud')

from TuyaSwitch import TuyaSwitch
from TuyaCloud import TuyaCloud

# TODO: add client_id, client_secret and device_id
CLIENT_REGION = 'TODO'
CLIENT_ID = 'TODO'
CLIENT_SECRET = 'TODO'
DEVICE_ID = 'TODO'

# Connect a Tuya Switch device
obj = TuyaSwitch(
                client_region=CLIENT_REGION,
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                device_id=DEVICE_ID
            )

# Get switch_1 status
print("Get switch_1 status...")
print (obj.get_status(['switch_1']))

# Turn switch_1 on
print("Turning switch_1 on...")
obj.turn_on(['switch_1'])

# Sleep 10 s
print("Sleep 10 seconds...")
time.sleep(10)

# Get switch_1 status
print("Get switch_1 status...")
print (obj.get_status(['switch_1']))

# Turn switch_1 off
print("Turning switch_1 off...")
obj.turn_off(['switch_1'])

# Get switch_1 status
print("Get switch_1 status...")
print (obj.get_status(['switch_1']))

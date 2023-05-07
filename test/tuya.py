import sys
import time
sys.path.append('../tuyacloud')

from tuyaswitch import TuyaSwitch

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

# Turn switch_1 on
print("Turning switch_1 on...")
obj.turn_on(['switch_1'])

# Sleep 10 s
print("Sleep 10 seconds...")
time.sleep(10)

# Turn switch_1 off
print("Turning switch_1 off...")
obj.turn_off(['switch_1'])

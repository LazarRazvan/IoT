import sys
import time
import json
import threading
from datetime import datetime
from flask import Flask, request, render_template, jsonify

# Append path for TuyaCloud
sys.path.append('../../TuyaCloud')

from TuyaSwitch import TuyaSwitch
from TuyaThermostat import TuyaThermostat

"""
Scenario: TODO
"""

###############################################################################
# Application logic
###############################################################################

app = Flask(__name__)
#
app_data = {}
#
thermostat = None
#
living_obj = None
#
TASK_SLEEP_TIME = 300
#
TUYA_LOG_FILE="tuya.log"
#
lights = ["living", "bucatarie", "hol", "baie1", "baie2"]

###############################################################################

def application_init(file):
    global app_data
    global thermostat

    print()
    print("Initialize application ...")
    print()

    #######################################################
    # Init application input
    #######################################################
    try:
        f = open(file)
    except OSError:
        print("Could not open file: %s" % file)
        sys.exit()

    with f:
        data = json.load(f)
        #
        #######################################################
        # Initialize tuya light objects
        #######################################################
        for light in lights:
            print()
            print(f'Initialize {light} object...')
            print()
            #
            light_device_id = data[f'app_tuya_{light}_device_id']
            light_switch_name = data[f'app_tuya_{light}_switch_name']
            #
            obj = TuyaSwitch(
                                client_region   = data['app_tuya_client_region'],
                                client_id       = data['app_tuya_client_id'],
                                client_secret   = data['app_tuya_client_secret'],
                                device_id       = light_device_id,
                                log_file        = TUYA_LOG_FILE
                            )

            app_data[light] = {"object" : obj, "switch_name" : light_switch_name}

        #######################################################
        # Initialize tuya thermostat
        #######################################################
        print()
        print(f'Initialize thermostat object...')
        print()
        #
        thermostat_device_id = data[f'app_tuya_thermostat_device_id']
        #
        thermostat = TuyaThermostat(
                            client_region   = data['app_tuya_client_region'],
                            client_id       = data['app_tuya_client_id'],
                            client_secret   = data['app_tuya_client_secret'],
                            device_id       = thermostat_device_id,
                            log_file        = TUYA_LOG_FILE
                        )


        #
        print()
        print("Application initialized successfully!")
        print()


###############################################################################
# Server logic
###############################################################################
@app.after_request
def add_cache_control(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/set_button', methods=['POST'])
def set_button():
    global app_data
    global thermostat

    #
    # Extract name and state from request
    #
    post_data = request.get_json()
    print(post_data)
    name = post_data['name']
    state = post_data['state']
    #
    # If unknown light, skip
    #
    if name not in app_data.keys():
        return "Error"
    #
    # Get associate tuya object
    #
    tuya_obj = app_data[name]['object']
    switch_name = app_data[name]['switch_name']
    #
    # Handle action
    #
    if state == "on":
        tuya_obj.turn_on([switch_name])
    else:
        tuya_obj.turn_off([switch_name])

    return "Success"

@app.route('/get_button')
def get_button():
    global app_data
    global thermostat

    result = {}
    #
    #
    #
    for key, value in app_data.items():
        tuya_obj = value['object']
        switch_name = value['switch_name']
        state = tuya_obj.get_status(switch_name)[switch_name]
        result[key] = state
    #
    #
    #
    result["set_temp"] = thermostat.get_trigger_temperature()
    result["room_temp"] = thermostat.get_room_temperature()
    #
    #
    #
    return jsonify(result)

if __name__ == '__main__':
    application_init('data.json')
    app.run(host="0.0.0.0",port=5001)


import sys
import time
import json
import threading
from flask import Flask, request, render_template

# Append path for TuyaCloud and HuaweiFusionSolar
sys.path.append('../../TuyaCloud')
sys.path.append('../../HuaweiFusionSolar')

from TuyaSwitch import TuyaSwitch
from HuaweiInverter import HuaweiInverter

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
app_lock = threading.Lock()
#
app_thread = None
#
stop_event = threading.Event()
#
tuya_obj = None
#
inverter_obj = None
#
TASK_SLEEP_TIME = 300
#
TUYA_LOG_FILE="tuya.log"
#
HUAWEI_LOG_FILE="huawei.log"

###############################################################################

def application_init(file):
    global app_data
    global tuya_obj
    global inverter_obj

    print()
    print("Initialize application ...")
    print()

    #######################################################
    # Init application data
    #######################################################
    app_data = {
        'app_state' : False,
        'app_error' : None,
        'app_config_trigger_value' : None,
        'app_status_active_power' : None,
        'app_status_switch_state' : None,
    }

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
        # Initialize tuya object
        #######################################################
        print()
        print("Initialize tuya...")
        print()
        tuya_obj = TuyaSwitch(
                        client_region   = data['app_tuya_client_region'],
                        client_id       = data['app_tuya_client_id'],
                        client_secret   = data['app_tuya_client_secret'],
                        device_id       = data['app_tuya_device_id'],
                        log_file        = TUYA_LOG_FILE
                    )
        #
        #######################################################
        # Initialize huawei inverter object
        #######################################################
        print()
        print("Initialize huawei...")
        print()
        inverter_obj = HuaweiInverter(
                        client_name     = data['app_huawei_client_name'],
                        client_pass     = data['app_huawei_client_pass'],
                        client_domain   = data['app_huawei_client_domain'],
                        device_type     = data['app_huawei_device_type'],
                        device_id       = data['app_huawei_device_id'],
                        log_file        = HUAWEI_LOG_FILE
                        )
    #
    print()
    print("Application initialized successfully!")
    print()


def application_task():
    global app_data
    global app_lock
    global tuya_obj
    global inverter_obj

    while not stop_event.is_set():
        #######################################################
        # With lock acquired, read inverter real time active
        # power and decice action for smart switch:
        #
        # 1) turn_on
        #    If inverter active power is larger than trigger
        #    value set.
        #
        # 2) turn_off
        #    If inverter active power is smaller than trigger
        #    value set.
        #
        # 2) nothing to do
        #    If inverter active power is larger than trigger
        #    value set and smart switch is already on.
        #######################################################
        app_lock.acquire()
        #
        try:
            app_data['app_status_active_power'] = inverter_obj.real_time_active_power()
        except ValueError as e:
            app_data['app_error'] = str(e)
            app_lock.release()
            application_stop()
            return
        #
        try:
            app_data['app_status_switch_state'] = tuya_obj.get_status(['switch_1'])['switch_1']
        except ValueError as e:
            app_data['app_error'] = str(e)
            app_lock.release()
            application_stop()
            return
        #
        if float(app_data['app_status_active_power']) >= float(app_data['app_config_trigger_value']):
            tuya_obj.turn_on(['switch_1'])
            app_data['app_status_switch_state'] = tuya_obj.get_status(['switch_1'])['switch_1']
        else:
            tuya_obj.turn_off(['switch_1'])
            app_data['app_status_switch_state'] = tuya_obj.get_status(['switch_1'])['switch_1']
        #
        app_lock.release()

        #######################################################
        # Check application stop condition.
        #######################################################
        if stop_event.is_set():
            break

        #######################################################
        # Thread sleep.
        #######################################################
        stop_event.wait(TASK_SLEEP_TIME)


# Lock is acquired when function is called
def application_start(post_data):
    global app_data
    global app_thread
    global stop_event
    global tuya_obj
    global inverter_obj

    #######################################################
    # Update application data
    #######################################################
    print("Application start...")
    app_data['app_state'] = True
    app_data['app_config_trigger_value'] = post_data['app_config_trigger_value']

    #######################################################
    # Start working thread
    #######################################################
    print("Start thread...")
    try:
        if app_thread is None or not app_thread.is_alive():
            # Create and start the task thread
            stop_event.clear()
            app_thread = threading.Thread(target=application_task)
            app_thread.start()
    except:
        # TODO
        app_data['app-error'] = "Thread Start Error"
        return

# Lock is acquired when function is called
def application_stop():
    global app_lock
    global tuya_obj
    global app_data
    global stop_event

    #######################################################
    # Reset application data
    #######################################################
    print("Application stop...")
    app_data['app_state'] = False
    app_data['app_config_trigger_value'] = None
    app_data['app_status_active_power'] = None
    app_data['app_status_switch_state'] = None

    print("Turn off the switch")
    tuya_obj.turn_off(['switch_1'])

    print("Stop thread...")
    stop_event.set()


###############################################################################
# Server logic
###############################################################################
@app.after_request
def add_cache_control(response):
    print("Function is called")
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/app_state_change', methods=['POST'])
def app_state_change():
    global app_data
    global app_lock

    # Read data
    post_data = request.get_json()
    post_app_state = post_data['app_state']

    # TODO: Debug print
    print("Post data: %s" % (post_data))

    # Error if trying to turn on an application already turned on
    app_lock.acquire()
    if post_app_state == True and app_data['app_state'] == True:
        app_lock.release()
        print("Error, application is already running...")
        return "Error, application is already running"

    try:
        if post_app_state == True:
            application_start(post_data)
        else:
            application_stop()

        pass
    finally:
        app_lock.release()

    # TODO: Debug print
    print("App data: %s" % (app_data))

    return "Success"

@app.route('/', methods=['GET'])
def index():
    global app_data
    global app_lock

    app_lock.acquire()
    data = app_data
    app_lock.release()

    print("Get data: %s" % (data))

    return render_template('index.html', data = data)

if __name__ == '__main__':
    application_init('data.json')
    app.run()

"""
Meathook.py contains a class to interface with the meathook device itself.
J.Zalger 2020
"""
import json
import requests
import threading
from string import Template
from sseclient import SSEClient

string_val_map = {"ON": "1", "OFF": "0"}


class MeatHook:

    main_state_mapping = ["fridge_temp", "fridge_rh", "external_temp",
                          "fridge_state", "humidifier_state", "fan_state", "door_state"]
    aux_state_mapping = ["fridge_temp_setpoint", "fridge_rh_setpoint", "temp_alarm", "rh_alarm",
                         "control_algorithm", "temp_alarm_delta", "rh_alarm_delta", "temp_control", "rh_control"]

    variables = main_state_mapping + aux_state_mapping
    events = []

    api_get_url = Template("https://api.particle.io/v1/devices/$device_id/$var_name")
    api_func_url = Template("https://api.particle.io/v1/devices/$device_id/$func_name")
    api_vitals_url = Template("https://api.particle.io/v1/diagnostics/$device_id/last")
    api_sse_url = Template("https://api.spark.io/v1/events/$event?access_token=$token")

    def __init__(self, device_id, token_id):
        self.device_id = device_id
        self.token_id = token_id
        self.state = None

        # SSE Callback Functions to be assigned by consumer
        self.temp_alarm_callback = None
        self.rh_alarm_callback = None
        self.door_alarm_callback = None

        # Initialize the device state, then subscribe to the feed.
        self.state = self._get_state()

        # Instead of the Web UI polling the device actively, which could result in rate limiting,
        # the object will listen to the status stream and cache the results to return to the client
        _t1 = threading.Thread(target=self._subscribe_to_event, args=("main_state", self._update_main_state)).start()
        _t2 = threading.Thread(target=self._subscribe_to_event, args=("aux_state", self._update_aux_state)).start()
        _t3 = threading.Thread(target=self._subscribe_to_event, args=("temp_alarm", self._handle_temp_alarm)).start()
        _t4 = threading.Thread(target=self._subscribe_to_event, args=("rh_alarm", self._handle_rh_alarm)).start()

    def _get_variable(self, var):
        """Returns the current device state as a JSON formatted string"""
        val = None
        if var not in MeatHook.variables:
            return dict()
        try:
            r = requests.get(MeatHook.api_get_url.substitute(dict(device_id=self.device_id, var_name=var)),
                             params=dict(access_token=self.token_id))
            if r.status_code == requests.codes.ok:
                val = dict(r.json())["result"]
                if val is True:
                    val = "1"
                elif val is False:
                    val = "0"
            else:
                raise requests.exceptions.RequestException
        except requests.exceptions.RequestException:
            pass
        return val

    def _get_state(self):
        print("Querying the device state. Will take ~15s")
        state = dict()
        for var in MeatHook.variables:
            state[var] = self._get_variable(var)
        return state

    # Event handlers
    def _update_main_state(self, msg):
        s = msg['data'].split(',')
        self.state.update({k: v for (k, v) in zip(MeatHook.main_state_mapping, s)})

    def _update_aux_state(self, msg):
        s = msg['data'].split(',')
        self.state.update({k: v for (k, v) in zip(MeatHook.aux_state_mapping, s)})

    def _handle_temp_alarm(self, msg):
        s = msg['data']
        self.state['temp_alarm'] = "1"

    def _handle_rh_alarm(self, msg):
        s = msg['data']
        self.state['rh_alarm'] = "1"

    @property
    def device_health(self):
        return dict()

    def set_led_state(self, new_light_state):
        success = self._call_func("set_led_state", new_light_state)
        if success:
            self.state['led_state'] = new_light_state
        return success

    def set_temp_setpoint(self, new_setpoint):
        success = self._call_func("set_temp_setpoint", new_setpoint)
        if success:
            self.state['fridge_temp_setpoint'] = new_setpoint
        return success

    def set_rh_setpoint(self, new_setpoint):
        success = self._call_func("set_rh_setpoint", new_setpoint)
        if success:
            self.state["fridge_rh_setpoint"] = new_setpoint
        return success

    def set_fan_state(self, new_state):
        success = self._call_func("set_fan_state", new_state)
        if success:
            self.state['fan_state'] = string_val_map[new_state]
        return success

    def set_fridge_state(self, new_state):
        success = self._call_func("set_fridge_state", new_state)
        if success:
            self.state['fridge_state'] = string_val_map[new_state]
        return success

    def set_temp_control(self, new_state):
        success = self._call_func("set_temp_control", new_state)
        if success:
            self.state['temp_control'] = string_val_map[new_state]
        return success

    def set_rh_control(self, new_state):
        success = self._call_func("set_rh_control", new_state)
        if success:
            self.state['rh_control'] = string_val_map[new_state]
        return success

    def set_temp_alarm_setpoint(self, new_state):
        success = self._call_func("set_temp_alarm_delta", new_state)
        if success:
            self.state['temp_alarm_delta'] = new_state
        return success

    def set_rh_alarm_setpoint(self, new_state):
        success = self._call_func("set_rh_alarm_delta", new_state)
        if success:
            self.state['rh_alarm_delta'] = new_state
        return success

    def set_control_alg(self, new_alg):
        if new_alg in ["basic", "pid", "learning"]:
            success = self._call_func("set_control_algorithm", new_alg)
            if success:
                self.state['control_algorithm'] = new_alg
            return success
        else:
            return False

    def _call_func(self, func_name, arg):
        try:
            r = requests.post(MeatHook.api_func_url.substitute(
                dict(device_id=self.device_id, func_name=func_name)),
                data=dict(args=str(arg), access_token=self.token_id))
            if r.status_code == requests.codes.ok:
                return True
            else:
                print("Call to %s failed with arg %s" % (func_name, arg))
                print(r.content)
                return False
        except requests.exceptions.RequestException:
            return False

    def _subscribe_to_event(self, event, callback):
        messages = SSEClient(MeatHook.api_sse_url.substitute(dict(event=event, token=self.token_id)))
        for msg in messages:
            if msg.data:
                callback(json.loads(msg.data))

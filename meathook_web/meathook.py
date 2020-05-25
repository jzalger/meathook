"""
Meathook.py contains a class to interface with the meathook device itself.
J.Zalger 2020
"""
import time
import json
import requests
from string import Template
from sseclient import SSEClient


class MeatHook:

    variables = ["external_temp", "fridge_temp", "fridge_rh", "fridge_temp_setpoint",
                 "fridge_state", "fridge_rh_setpoint"]
    main_state_mapping = ["fridge_temp", "fridge_rh", "external_temp",
                          "fridge_state", "humidifier_state", "fan_state"]
    aux_state_mapping = ["temp_setpoint", "rh_setpoint", "temp_alarm", "rh_alarm",
                         "control_algorithm", "temp_alarm_delta", "rh_alarm_delta"]
    events = []

    api_get_url = Template("https://api.particle.io/v1/devices/$device_id/$var_name")
    api_func_url = Template("https://api.particle.io/v1/devices/$device_id/$func_name?arg=$arg:access_token=$token")
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
        self._subscribe_to_event("main_state", self._update_main_state)
        self._subscribe_to_event("aux_state", self._update_aux_state)

    def _get_variable(self, var):
        """Returns the current device state as a JSON formatted string"""
        state = None
        if var not in MeatHook.variables:
            return dict()
        try:
            r = requests.get(MeatHook.api_get_url.substitute(dict(device_id=self.device_id, var_name=var)),
                             params=dict(access_token=self.token_id))
            if r.status_code == requests.codes.ok:
                state = dict(r.json())["result"]
            else:
                raise requests.exceptions.RequestException
        except requests.exceptions.RequestException:
            pass
        return state

    def _get_state(self):
        state = dict()
        for var in MeatHook.variables:
            state[var] = self._get_variable(var)
        return state

    def _update_main_state(self, msg):
        s = msg['data'].split(',')
        self.state.update({k: v for (k, v) in zip(MeatHook.main_state_mapping, s)})

    def _update_aux_state(self, msg):
        s = msg['data'].split(',')
        self.state.update({k: v for (k, v) in zip(MeatHook.aux_state_mapping, s)})

    @property
    def device_health(self):
        return dict()

    def set_temp_setpoint(self, new_setpoint):
        return self._call_func("set_temp_setpoint", new_setpoint)

    def set_rh_setpoint(self, new_setpoint):
        return self._call_func("set_rh_setpoint", new_setpoint)

    def set_fan_state(self, new_state):
        return self._call_func("set_fan_state", new_state)

    def set_fridge_state(self, new_state):
        return self._call_func("set_fridge_state", new_state)

    def set_temp_control(self, new_state):
        return self._call_func("set_temp_control", new_state)

    def set_rh_control(self, new_state):
        return self._call_func("set_rh_control", new_state)

    def set_temp_alarm_point(self, new_state):
        return self._call_func("set_temp_alarm_threashold", new_state)

    def set_rh_alarm_point(self, new_state):
        return self._call_func("set_rh_alarm_threashold", new_state)

    def set_control_alg(self, new_alg):
        if new_alg in ["basic", "pid", "learning"]:
            return self._call_func("set_control_algorithm", new_alg)
        else:
            return False

    def _call_func(self, func_name, arg):
        try:
            r = requests.get(MeatHook.api_func_url.substitute(dict(device_id=self.device_id, func_name=func_name, arg=str(arg))),
                             params=dict(access_token=self.token_id))
            if r.status_code == requests.codes.ok:
                return True
            else:
                return False
        except requests.exceptions.RequestException:
            return False

    def _subscribe_to_event(self, event, callback):
        messages = SSEClient(MeatHook.api_sse_url.substitute(dict(event=event, token=self.token_id)))
        for msg in messages:
            if msg.data:
                callback(json.loads(msg.data))

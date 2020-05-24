"""
Meathook.py contains a class to interface with the meathook device itself.
J.Zalger 2020
"""
import time
import requests
from string import Template
from sseclient import SSEClient


class MeatHook:

    variables = ["external_temp", "fridge_temp", "fridge_rh", "fridge_temp_setpoint",
                 "fridge_state", "fridge_rh_setpoint"]
    events = []

    api_get_url = Template("https://api.particle.io/v1/devices/$device_id/$var_name")
    api_func_url = Template("https://api.particle.io/v1/devices/$device_id/$func_name?arg=$arg:access_token=$token")
    api_vitals_url = Template("https://api.particle.io/v1/diagnostics/$device_id/last")
    api_sse_url = Template("https://api.spark.io/v1/events/$event?access_token=$token")

    def __init__(self, device_id, token_id):
        self.device_id = device_id
        self.token_id = token_id

        # SSE Callback Functions to be assigned by consumer
        self.temp_alarm_callback = None
        self.rh_alarm_callback = None
        self.door_alarm_callback = None

    @property
    def state(self):
        """Returns the current device state as a JSON formatted string"""
        state = dict()
        for variable in MeatHook.variables:
            try:
                r = requests.get(MeatHook.api_get_url.substitute(dict(device_id=self.device_id, var_name=variable)),
                                 params=dict(access_token=self.token_id))
                if r.status_code == requests.codes.ok:
                    # FIXME: This probably doesnt work correctly
                    state[variable] = dict(r.json())["result"]
                else:
                    raise requests.exceptions.RequestException
            except requests.exceptions.RequestException:
                pass
            time.sleep(1)  # Rate limit the API queries
        return state

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
        events = SSEClient(MeatHook.api_sse_url.substitute(dict(event=event, token=self.token_id)))
        for event in events:
            callback(event)

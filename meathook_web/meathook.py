"""
Meathook.py contains a class to interface with the meathook device itself.
J.Zalger 2022
"""
import json
import requests
import logging
import threading
import concurrent.futures
from sseclient import SSEClient
from distutils.util import strtobool

mhlog = logging.getLogger("meathook_web.meathook")

string_val_map = {"ON": "1", "OFF": "0"}


class MeatHook(object):
    state_variables = ["fridge_temp", "fridge_rh", "external_temp", "fridge_state", "fan_state", "door_state",
                       "temp_setpoint", "temp_alarm", "rh_alarm", "control_algorithm", "temp_alarm_delta",
                       "rh_alarm_limit", "temp_control", "es_state", "es_temp_setpoint", "es_start", "es_stop",
                       "current_temp_setpoint"]

    def __init__(self, device_id, token_id, api_config):
        self.device_id = device_id
        self.token_id = token_id
        self.api_config = api_config
        self.state = dict()
        self.sse_stream_thread = threading.Thread(target=self._start_stream)

    def init_state(self):
        if self.is_online:
            mhlog.debug("Initializing device state")
            self.get_state()

    def start_stream(self):
        mhlog.debug("Starting device SSE Stream")
        self.sse_stream_thread.start()

    def stop_stream(self):
        self.sse_stream_thread.join(timeout=1)
        mhlog.debug("Stopped device SSE Stream")

    def _start_stream(self):
        stream = SSEClient(self.api_config["sse_url"].substitute(dict(device_id=self.device_id, token=self.token_id)))
        for event in stream:
            if event.data != "":
                self._handle_state_update(event)

    def _handle_state_update(self, event):
        event_data = json.loads(event.data)
        if event_data['coreid'] == self.device_id:
            device_data_pairs = event_data['data'].split(",")
            device_data_pairs = [pair.split("=") for pair in device_data_pairs]
            device_data = {pair[0]: pair[1] for pair in device_data_pairs}
            for variable, value in device_data.items():
                if value == "True" or value == "False":
                    device_data[variable] = bool(strtobool(value))
            self.state.update(device_data)

    def _get_variable(self, var):
        """Returns the current device state as a JSON formatted string"""
        r = requests.get(self.api_config["get_url"].substitute(dict(device_id=self.device_id, var_name=var)),
                         params=dict(access_token=self.token_id))
        if r.status_code == requests.codes.ok:
            return r.json()["result"]
        else:
            mhlog.debug("_get_variable failed with invalid return code. Variable: %s" % var)
            return None

    def get_state(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as thread_pool:
            completed = thread_pool.map(self._get_variable, self.state_variables)
        new_state = {k: v for (k, v) in zip(MeatHook.state_variables, completed)}
        self.state.update(new_state)

    @property
    def is_online(self):
        url = self.api_config["ping_url"].substitute(dict(device_id=self.device_id))
        response = requests.put(url, data={'access_token': self.token_id})
        if response.status_code == requests.codes.ok:
            return response.json()["online"]
        else:
            mhlog.debug("is_online failed with invalid response code")
            return False

    def set_led_state(self, new_light_state):
        success = self._call_func("set_led_state", new_light_state)
        if success:
            self.state['led_state'] = new_light_state
        else:
            mhlog.warning("set_led_state failed")
        return success

    def set_temp_setpoint(self, new_setpoint):
        success = self._call_func("set_temp_setpoint", new_setpoint)
        if success:
            self.state['fridge_temp_setpoint'] = new_setpoint
        else:
            mhlog.warning("set_temp_setpoint failed")
        return success

    def set_fan_state(self, new_state):
        success = self._call_func("set_fan_state", new_state)
        if success:
            self.state['fan_state'] = string_val_map[new_state]
        else:
            mhlog.warning("set_fan_state failed")
        return success

    def set_fridge_state(self, new_state):
        success = self._call_func("set_fridge_state", new_state)
        if success:
            self.state['fridge_state'] = string_val_map[new_state]
        else:
            mhlog.warning("set_fridge_state failed")
        return success

    def set_temp_control(self, new_state):
        success = self._call_func("set_temp_control", new_state)
        if success:
            self.state['temp_control'] = string_val_map[new_state]
        else:
            mhlog.warning("set_temp_control failed")
        return success

    def set_temp_alarm_delta(self, new_state):
        success = self._call_func("set_temp_alarm_delta", new_state)
        if success:
            self.state['temp_alarm_delta'] = new_state
        else:
            mhlog.warning("set_temp_alarm_delta failed")
        return success

    def set_rh_alarm_limit(self, new_state):
        success = self._call_func("set_rh_alarm_limit", new_state)
        if success:
            self.state['rh_alarm_limit'] = new_state
        else:
            mhlog.warning("set_rh_alarm_limit failed")
        return success

    def set_control_alg(self, new_alg):
        if new_alg in ["basic", "pid", "learning"]:
            success = self._call_func("set_control_algorithm", new_alg)
            if success:
                self.state['control_algorithm'] = new_alg
            else:
                mhlog.warning("set_control_alg failed")
            return success
        else:
            mhlog.warning("Invalid algorithm passed to set_control_alg")
            return False

    def set_es_state(self, new_state):
        success = self._call_func("es_state", new_state)
        if success:
            self.state['es_state'] = new_state
        else:
            mhlog.warning("set_est_state failed")
        return success

    def set_es_temp_setpoint(self, new_state):
        success = self._call_func("es_temp_setpoint", new_state)
        if success:
            self.state['es_temp_setpoint'] = new_state
        else:
            mhlog.warning("set_es_temp_setpoint failed")
        return success

    def set_es_timing(self, new_state):
        # new state must contain both es_start_string and es_end_string as a dict.
        start_success = self._call_func("es_start", new_state['es_start_string'])
        end_success = self._call_func("es_stop", new_state['es_stop_string'])
        if start_success and end_success:
            self.state['es_start_string'] = new_state['es_start_string']
            self.state['es_stop_string'] = new_state['es_stop_string']
            return True
        else:
            mhlog.warning("set_es_timing failed")
            return False

    def _call_func(self, func_name, arg):
        try:
            r = requests.post(self.api_config["func_url"].substitute(
                dict(device_id=self.device_id, func_name=func_name)),
                data=dict(args=str(arg), access_token=self.token_id))
            if r.status_code == requests.codes.ok:
                return True
            else:
                mhlog.warning("_call_func failed. Func Name: %s, Arg: %s" % (func_name, arg))
                return False
        except requests.exceptions.RequestException:
            return False

"""
Meathook.py contains a class to interface with the meathook device itself.
J.Zalger 2020
"""
import json
import requests
import threading
import concurrent.futures
from sseclient import SSEClient

string_val_map = {"ON": "1", "OFF": "0"}


class MeatHook(object):
    state_variables = ["fridge_temp", "fridge_rh", "external_temp", "fridge_state", "fan_state", "door_state",
                       "temp_setpoint", "temp_alarm", "rh_alarm", "control_alg", "temp_alarm_delta",
                       "rh_alarm_limit", "temp_control"]

    def __init__(self, device_id, token_id, api_config, init_state=True):
        self.device_id = device_id
        self.token_id = token_id
        self.api_config = api_config
        self.state = dict()

        # Initialize the device state, then subscribe to the feed.
        if self.is_online and init_state:
            self.get_state()

        self.subscribed_events = ['state']
        self.event_handlers = dict(state=self._handle_state_update)
        self.sse_stream_thread = threading.Thread(target=self._start_stream)
        self.start_stream()

    def start_stream(self):
        self.sse_stream_thread.start()

    def stop_stream(self):
        self.sse_stream_thread.join(timeout=1)

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
            self.state.update(device_data)

    def _get_variable(self, var):
        """Returns the current device state as a JSON formatted string"""
        r = requests.get(self.api_config["get_url"].substitute(dict(device_id=self.device_id, var_name=var)),
                         params=dict(access_token=self.token_id))
        if r.status_code == requests.codes.ok:
            return r.json()["result"]
        else:
            return None

    def get_state(self):
        print("Querying the device state")
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as thread_pool:
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
            return False

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

    def set_temp_alarm_delta(self, new_state):
        success = self._call_func("set_temp_alarm_delta", new_state)
        if success:
            self.state['temp_alarm_delta'] = new_state
        return success

    def set_rh_alarm_limit(self, new_state):
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
            r = requests.post(self.api_config["func_url"].substitute(
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

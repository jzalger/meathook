"""
Unit Tests for meathook.py
"""
from mhconfig_template import api_config
import meathook_web.meathook as meathook
import threading


def test_basic_init(device):
    assert device.device_id == "1234" 
    assert device.token_id == "1234"
    assert device.api_config == api_config
    assert isinstance(device.sse_stream_thread, threading.Thread)
    assert isinstance(device.state, dict)

def test_start_stream(device):
    device.start_stream()
    assert device.sse_stream_thread.is_alive() == True

def test_stop_stream(device):
    device.sse_stream_thread.start()
    device.stop_stream()
    assert device.sse_stream_thread.is_alive() == False
    
def test_handle_state_update(device, event):
    device._handle_state_update(event)
    assert isinstance(device.state, dict)
    assert device.state['fridge_temp'] == '25.159996'
    assert device.state['fridge_rh'] == '56.595303'
    assert device.state['external_temp'] == '30.952381'
    assert device.state['fridge_state'] == False
    assert device.state['fan_state'] == False
    assert device.state['door_state'] == False
    assert device.state['temp_setpoint'] ==  '5.500000'
    assert device.state['temp_alarm'] == False
    assert device.state['rh_alarm'] == False
    assert device.state['control_algorithm'] == 'basic'
    assert device.state['temp_alarm_delta'] == '25.000000'
    assert device.state['rh_alarm_limit'] == '80.000000'
    assert device.state['temp_control'] == False
    assert device.state['es_state'] == False
    assert device.state['es_temp_setpoint'] == '10.000000'
    assert device.state['es_start'] == "20:00"
    assert device.state['es_stop'] == "11:00"
    assert device.state['current_temp_setpoint'] == "5.500000"

"""
Unit Tests for meathook.py
"""
from mhconfig_template import api_config
import threading


def test_basic_init(basic_device):
    assert basic_device.device_id == "1234" 
    assert basic_device.token_id == "1234"
    assert basic_device.api_config == api_config
    assert isinstance(basic_device.sse_stream_thread, threading.Thread)
    assert isinstance(basic_basic_device.state, dict)

def test_start_stream(basic_device):
    basic_device.start_stream()
    assert basic_device.sse_stream_thread.is_alive() is True

def test_stop_stream(basic_device):
    basic_device.sse_stream_thread.start()
    basic_device.stop_stream()
    assert basic_device.sse_stream_thread.is_alive() is False
    
def test_handle_state_update(basic_device, event):
    basic_device._handle_state_update(event)
    assert isinstance(basic_device.state, dict)
    assert basic_device.state['fridge_temp'] == '25.159996'
    assert basic_device.state['fridge_rh'] == '56.595303'
    assert basic_device.state['external_temp'] == '30.952381'
    assert basic_device.state['fridge_state'] is False
    assert basic_device.state['fan_state'] is False
    assert basic_device.state['door_state'] is False
    assert basic_device.state['temp_setpoint'] ==  '5.500000'
    assert basic_device.state['temp_alarm'] is False
    assert basic_device.state['rh_alarm'] is False
    assert basic_device.state['control_algorithm'] == 'basic'
    assert basic_device.state['temp_alarm_delta'] == '25.000000'
    assert basic_device.state['rh_alarm_limit'] == '80.000000'
    assert basic_device.state['temp_control'] is False
    assert basic_device.state['es_state'] is False
    assert basic_device.state['es_temp_setpoint'] == '10.000000'
    assert basic_device.state['es_start'] == "20:00"
    assert basic_device.state['es_stop'] == "11:00"
    assert basic_device.state['current_temp_setpoint'] == "5.500000"

"""
Unit Tests for meathook_web.py
"""
import pytest
from mhconfig_template import api_config


def test_main(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert b"Meat Hook" in response.data

    
def test_get_device_state(test_client):
    response = test_client.get("/get-device-state")
    assert response.status_code == 200
    assert b'{}\n' in response.data

def test_get_var_state():
    pass
    
def test_set_led_state():
    pass
    
def test_set_temp_control():
    pass
    
def test_set_fan_state():
    pass
    
def test_set_temp_setpoint():
    pass
    
def test_set_ctl_algorithm():
    pass
    
def test_set_fridge_state():
    pass
    
def test_set_temp_alarm_threashold():
    pass
    
def test_set_rh_alarm_limit():
    pass
    
def test_set_es_state():
    pass
    
def test_set_es_temp_setpoint():
    pass
    
def test_set_es_timing():
    pass


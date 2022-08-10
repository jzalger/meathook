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
    pytest.skip("To be implemented")
    
def test_set_led_state():
    pytest.skip("To be implemented")
    
def test_set_temp_control():
    pytest.skip("To be implemented")
    
def test_set_fan_state():
    pytest.skip("To be implemented")
    
def test_set_temp_setpoint():
    pytest.skip("To be implemented")
    
def test_set_ctl_algorithm():
    pytest.skip("To be implemented")
    
def test_set_fridge_state():
    pytest.skip("To be implemented")
    
def test_set_temp_alarm_threashold():
    pytest.skip("To be implemented")
    
def test_set_rh_alarm_limit():
    pytest.skip("To be implemented")
    
def test_set_es_state():
    pytest.skip("To be implemented")
    
def test_set_es_temp_setpoint():
    pytest.skip("To be implemented")
    
def test_set_es_timing():
    pytest.skip("To be implemented")


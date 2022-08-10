import pytest
import json
import sseclient
from meathook_web.meathook import MeatHook
from meathook_web import meathook_web
from mhconfig_template import api_config

@pytest.fixture(scope="module")
def test_client():
    app = meathook_web.meathook
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client

@pytest.fixture
def device():
    device = MeatHook("1234", "1234", api_config)
    return device

@pytest.fixture
def event():
    data = '{"data":"fridge_temp=25.159996,fridge_rh=56.595303,external_temp=30.952381,fridge_state=False,fan_state=False,door_state=False,temp_setpoint=5.500000,temp_alarm=False,rh_alarm=False,control_algorithm=basic,temp_alarm_delta=25.000000,rh_alarm_limit=80.000000,temp_control=False,es_state=False,es_temp_setpoint=10.000000,es_start=20:00,es_stop=11:00,current_temp_setpoint=5.500000","ttl":60,"published_at":"2022-08-10T22:47:09.414Z","coreid":"1234"}'
    event = sseclient.Event(data=data, event="DATA")
    return event

import os
import logging.handlers
import simplejson as json
import importlib.util
from flask import Flask, render_template, request, jsonify
from meathook_web import meathook
spec = importlib.util.spec_from_file_location("mhconfig", os.getenv("MHCONFIG_FILE"))
mhconfig = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mhconfig)

mhlog = logging.getLogger('meathook_web')
mhlog.setLevel(logging.INFO)
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
syslog_handler = logging.handlers.SysLogHandler(address=mhconfig.syslog_host)
syslog_handler.setFormatter(log_formatter)
mhlog.addHandler(syslog_handler)
meathook.mhlog = mhlog

meathook_app = Flask(__name__)

device = meathook.MeatHook(mhconfig.device_id, mhconfig.particle_token, api_config=mhconfig.api_config)
if mhconfig.testing is False:
    device.init_state()
    device.start_stream()


@meathook_app.route('/')
def main():
    return render_template('meathook.html')


@meathook_app.route("/get-device-state")
def get_device_state():
    return jsonify(device.state)


@meathook_app.route('/refresh-device-state')
def refresh_device_state():
    """Forces a full re-query of the device"""
    device.get_state()
    return jsonify(device.state)


@meathook_app.route("/get-var-state", methods=["GET"])
def get_var_state():
    var = request.args.get("var")
    return jsonify(device.state(var))


@meathook_app.route("/set-led-state", methods=["GET"])
def set_led_state():
    new_state = request.args.get("new_state")
    return jsonify(device.set_led_state(new_state))


@meathook_app.route('/set-temp-ctl', methods=["GET"])
def set_temp_control():
    new_state = request.args.get("new_state")
    return jsonify(device.set_temp_control(new_state))


@meathook_app.route("/set-fan-state", methods=["GET"])
def set_fan_state():
    new_state = request.args.get("new_state")
    return jsonify(device.set_fan_state(new_state))


@meathook_app.route("/set-temp-setpoint", methods=["GET"])
def set_temp_setpoint():
    new_state = request.args.get("new_state")
    return jsonify(device.set_temp_setpoint(new_state))


@meathook_app.route("/set-ctl-alg", methods=["GET"])
def set_ctl_algorithm():
    new_state = request.args.get("new_state")
    return jsonify(device.set_control_alg(new_state))


@meathook_app.route("/set-fridge-state", methods=["GET"])
def set_fridge_state():
    new_state = request.args.get("new_state")
    return jsonify(device.set_fridge_state(new_state))


@meathook_app.route("/set-temp-alarm-point", methods=["GET"])
def set_temp_alarm_threashold():
    new_state = request.args.get("new_state")
    return jsonify(device.set_temp_alarm_delta(new_state))


@meathook_app.route("/set-rh-alarm-limit", methods=["GET"])
def set_rh_alarm_limit():
    new_state = request.args.get("new_state")
    return jsonify(device.set_rh_alarm_limit(new_state))


@meathook_app.route("/set-es-state", methods=["GET"])
def set_es_state():
    new_state = request.args.get("new_state")
    return jsonify(device.set_es_state(new_state))


@meathook_app.route("/set-es-temp-setpoint", methods=["GET"])
def set_es_temp_setpoint():
    new_state = request.args.get("new_state")
    return jsonify(device.set_es_temp_setpoint(new_state))


@meathook_app.route("/set-es-timing", methods=["GET"])
def set_es_timing():
    new_state = json.loads(request.args.get("new_state"))
    return jsonify(device.set_es_timing(new_state))


if __name__ == '__main__':
    mhlog.info("Launching MeatHook Web App")
    meathook_app.run(debug=mhconfig.testing, host=mhconfig.web_host)

import os
import importlib.util
from flask import Flask, render_template, request, jsonify
from meathook import MeatHook
spec = importlib.util.spec_from_file_location("mhconfig", os.getenv("MHCONFIG_FILE"))
mhconfig = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mhconfig)

meathook = Flask(__name__)
device = MeatHook(mhconfig.device_id, mhconfig.particle_token, api_config=mhconfig.api_config)


@meathook.route('/')
def main():
    return render_template('meathook.html')


@meathook.route("/get-device-state")
def get_device_state():
    return jsonify(device.state)


@meathook.route("/get-var-state", methods=["GET"])
def get_var_state():
    var = request.args.get("var")
    return jsonify(device.state(var))


@meathook.route("/set-led-state", methods=["GET"])
def set_led_state():
    new_state = request.args.get("new_state")
    return jsonify(device.set_led_state(new_state))


@meathook.route('/set-temp-ctl', methods=["GET"])
def set_temp_control():
    new_state = request.args.get("new_state")
    return jsonify(device.set_temp_control(new_state))


@meathook.route("/set-fan-state", methods=["GET"])
def set_fan_state():
    new_state = request.args.get("new_state")
    return jsonify(device.set_fan_state(new_state))


@meathook.route("/set-temp-setpoint", methods=["GET"])
def set_temp_setpoint():
    new_state = request.args.get("new_state")
    return jsonify(device.set_temp_setpoint(new_state))


@meathook.route("/set-ctl-alg", methods=["GET"])
def set_ctl_algorithm():
    new_state = request.args.get("new_state")
    return jsonify(device.set_control_alg(new_state))


@meathook.route("/set-fridge-state", methods=["GET"])
def set_fridge_state():
    new_state = request.args.get("new_state")
    return jsonify(device.set_fridge_state(new_state))


@meathook.route("/set-temp-alarm-point", methods=["GET"])
def set_temp_alarm_threashold():
    new_state = request.args.get("new_state")
    return jsonify(device.set_temp_alarm_delta(new_state))


@meathook.route("/set-rh-alarm-limit", methods=["GET"])
def set_rh_alarm_limit():
    new_state = request.args.get("new_state")
    return jsonify(device.set_rh_alarm_limit(new_state))


@meathook.route("/set-es-state", methods=["GET"])
def set_es_state():
    new_state = request.args.get("new_state")
    return jsonify(device.set_es_state(new_state))


@meathook.route("/set-es-temp-setpoint", methods=["GET"])
def set_es_temp_setpoint():
    new_state = request.args.get("new_state")
    return jsonify(device.set_es_temp_setpoint(new_state))


@meathook.route("/set-es-timing", methods=["GET"])
def set_es_timing():
    new_state = request.args.get("new_state")
    return jsonify(device.set_es_timing(new_state))


if __name__ == '__main__':
    meathook.run(debug=True, host=mhconfig.web_host)

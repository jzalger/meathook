from flask import Flask, render_template, request, jsonify
from meathook import MeatHook
from secrets import device_id, particle_token

meathook = Flask(__name__)
device = MeatHook(device_id, particle_token)

#     return dict(current_temp=8.5, current_rh=46, current_ext_temp=30,
#                 temp_alert=False, rh_alert=False, door_alert=False,
#                 temp_setpoint=8.6, rh_setpoint=45, temp_alarm_delta=10, rh_alarm_delta=20)


@meathook.route('/')
def main():
    return render_template('meathook.html')


@meathook.route("/get-var-state", methods=["GET"])
def get_var_state():
    var = request.args.get("var")
    return device.get_state(var)


@meathook.route('/set-temp-ctl', methods=["GET"])
def set_temp_control():
    new_state = request.args.get("new_state")
    return device.set_temp_control(new_state)


@meathook.route('/set-rh-ctl', methods=["GET"])
def set_rh_control():
    new_state = request.args.get("new_state")
    return device.set_rh_control(new_state)


@meathook.route("/set-fan-state", methods=["GET"])
def set_fan_state():
    new_state = request.args.get("new_state")
    return device.set_fan_state(new_state)


@meathook.route("/set-temp-setpoint", methods=["GET"])
def set_temp_setpoint():
    new_state = request.args.get("new_state")
    return device.set_temp_setpoint(new_state)


@meathook.route("/set-humidity-setpoint", methods=["GET"])
def set_rh_setpoint():
    new_state = request.args.get("new_state")
    return device.set_rh_setpoint(new_state)


@meathook.route("/set-ctl-alg", methods=["GET"])
def set_ctl_algorithm():
    new_state = request.args.get("new_state")
    return device.set_control_alg(new_state)


@meathook.route("/set-fridge-state", methods=["GET"])
def set_fridge_state():
    new_state = request.args.get("new_state")
    return device.set_fridge_state(new_state)


@meathook.route("/set-temp-alarm-point", methods=["GET"])
def set_temp_alarm_threashold():
    new_state = request.args.get("new_state")
    return device.set_temp_alarm_point(new_state)


@meathook.route("/set-rh-alarm-point", methods=["GET"])
def set_rh_alarm_threashold():
    new_state = request.args.get("new_state")
    return device.set_rh_alarm_point(new_state)


if __name__ == '__main__':
    meathook.run(debug=True)

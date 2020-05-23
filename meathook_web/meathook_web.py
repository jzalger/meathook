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
    state = device.state
    return render_template('meathook.html', state=state)


@meathook.route('/set-temp-ctl', methods=["GET"])
def set_temp_control():
    new_state = request.args.get("new_state")
    return device.set_temp_control(new_state)


@meathook.route('/set-rh-ctl', method=["GET"])
def set_rh_control():
    new_state = request.args.get("new_state")
    return device.set_rh_control(new_state)


if __name__ == '__main__':
    meathook.run(debug=True)

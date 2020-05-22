from flask import Flask, render_template
meathook = Flask(__name__)


def get_state():
    return dict(current_temp=8.5, current_rh=46, current_ext_temp=30,
                temp_alert=False, rh_alert=False, door_alert=False,
                temp_setpoint=8.6, rh_setpoint=45, temp_alarm_delta=10, rh_alarm_delta=20)


@meathook.route('/')
def main():
    state = get_state()
    return render_template('meathook.html', state=state)


@meathook.route('/current-temp')
def current_temp():
    return 0


@meathook.route('/current-rh')
def current_rh():
    return 0.0


if __name__ == '__main__':
    meathook.run(debug=True)

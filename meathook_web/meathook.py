from flask import Flask, render_template
meathook = Flask(__name__)


@meathook.route('/')
def main():
    return render_template('meathook.html')


@meathook.route('/current-temp')
def current_temp():
    return 0


@meathook.route('current-rh')
def current_rh():
    return 0.0


if __name__ == '__main__':
    meathook.run(debug=True)

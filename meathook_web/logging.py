import time
import requests
from string import Template
from influxdb import InfluxDBClient
from secrets import device_id, particle_token, influx_db_name, influx_host, influx_port

api_get_url = Template("https://api.particle.io/v1/devices/$device_id/$var_name")
api_vitals_url = Template("https://api.particle.io/v1/diagnostics/$device_id/last")

poll_frequency = 60  # Frequency in seconds


def query_device(did, variable):
    r = requests.get(api_get_url.substitute(dict(device_id=did, var_name=variable)),
                     data=dict(access_token=particle_token))
    return r.json()


def insert_data(new_data):
    client = InfluxDBClient(host=influx_host, port=influx_port)
    client.switch_database(influx_db_name)
    client.write_points(new_data)


def main():
    variables = ["external_temp, fridge_temp, fridge_rh, fridge_temp_setpoint,"
                 "fridge_state, fridge_rh_setpoint"]
    # while True:
    for variable in variables:
        data = query_device(device_id, variable)
        print(data)
        # insert_data(data)
        time.sleep(1)  # Rate limit the API queries
    time.sleep(poll_frequency)


if __name__ == "__main__":
    main()

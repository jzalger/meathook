"""
Configuration data
"""
from string import Template
api_get_url = Template("https://api.particle.io/v1/devices/$device_id/$var_name")
api_func_url = Template("https://api.particle.io/v1/devices/$device_id/$func_name")
api_vitals_url = Template("https://api.particle.io/v1/diagnostics/$device_id/last")
api_sse_url = Template("https://api.particle.io/v1/devices/$device_id/events/state?access_token=$token")
api_ping_url = Template("https://api.particle.io/v1/devices/$device_id/ping")
api_config = dict(get_url=api_get_url,
                  func_url=api_func_url,
                  vitals_url=api_vitals_url,
                  sse_url=api_sse_url,
                  ping_url=api_ping_url)

device_id = ""  # ID of particle device
particle_token = ""
web_host = "0.0.0.0"

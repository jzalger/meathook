job "meathook" {
  datacenters = ["dc1"]
  type = "service"

  group "meathook" {
    # Specify the number of these tasks we want.
    count = 1

    network {
      port "https" {
        static = 5100
      }
    }

    service {
      name = "meathook"
      tags = ["meathook", "webservice", "tls", "vault"]
      port = "https"
      check {
        type     = "http"
        protocol = "https"
        path     = "/"
        interval = "60s"
        timeout  = "10s"
        tls_skip_verify = true
      }
    }

    task "meathook" {
      driver = "docker"

      env {
        SECRETS_FILE = "/run/secrets/secrets.py"
      }

      config {
        image = "jzalger/meathook:latest"
        ports = ["https"]
        volumes = ["secrets:/run/secrets"]
      }

      template {
        data = <<EOF
{{ with secret "pki_int/issue/app-certificates" "common_name=meathook" "ttl=96h"}}
{{ .Data.private_key }}
{{ end }}
EOF
        destination = "secrets/meathook.key"
      }

      template {
        data = <<EOF
{{ with secret "pki_int/issue/app-certificates" "common_name=meathook" "ttl=96h"}}
{{ .Data.certificate }}
{{ end }}
EOF
        destination = "secrets/meathook.crt"
      }

      template {
        data = <<EOF
{{ with secret "kv/data/machine/dev/apps/meathook" }}
particle_token = "{{ .Data.data.cloud_api_token }}"
web_host = "{{ .Data.data.web_host }}"
device_id = "{{ .Data.data.device_id }}"
syslog_host = {{ .Data.data.syslog_host }}
{{ end }}
EOF
        destination = "secrets/secrets.py"
      }
      resources {
        cpu    = 512 # MHz
        memory = 256 # MB
      }
      vault {
        policies = ["meathook-dev"]
      }
    }
  }
}

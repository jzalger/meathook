# Meat Hook

![CI](https://github.com/jzalger/meathook/workflows/CI/badge.svg?branch=dev)
![GitHub](https://img.shields.io/github/license/jzalger/meathook)
![GitHub Pipenv locked Python version (branch)](https://img.shields.io/github/pipenv/locked/python-version/jzalger/meathook/master)
[![codecov](https://codecov.io/gh/jzalger/meathook/branch/master/graph/badge.svg)](https://codecov.io/gh/jzalger/meathook)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=jzalger_meathook&metric=bugs)](https://sonarcloud.io/summary/new_code?id=jzalger_meathook)

Meat Hook is a temperature and humidity controlled fridge for dry aging meat.
This project goes through designing the circuit and PCB as well as the surrounding full-stack web application and data
logging utilities. It also explores using various control algorithms including basic, PID, and machine learning approaches.

The controller is based on the [Particle Photon](http://www.particle.io), a Wifi enabled ARM based processor with a cloud-based API.
The web application backend is written in Python using the Flask framework. The frontend uses HTML and Javascript, leveraging the Bootstrap framework.

![User Interface](docs/img/meathook_ui.png)

## Circuit and PCB Design

Below is a simple block diagram showing the sensors and actuators in the fridge.

![Schematic](docs/img/schematic.png?raw=true)

![PCB](docs/img/pcb.png?raw=true)

![Block Diagram](docs/img/block_diagram.png?"raw=true)

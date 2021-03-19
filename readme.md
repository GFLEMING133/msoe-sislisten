# Sislisten

This repository is the home for all code related to mood lighting.

## Getting Set Up:

This server is built with flask and python3.

### Windows

Install python from [here](https://www.python.org/downloads/windows/).

Install flask from [here](https://flask.palletsprojects.com/en/1.1.x/installation/)

Install Pyaudio from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio), since the `pip` repo for Pyaudio is not stable. Download the wheel based on the python version that you have installed. For example, if you have python 3.9, you should install the PyAudio‑0.2.11‑cp39‑cp39‑win_amd64.whl file. Once downloading the file, execute `pip install PyAudio‑0.2.11‑cp39‑cp39‑win_amd64.whl`. This should install PyAudio.

### Linux

Run `sudo apt install python3` and `sudo apt install pip3`. Say `Y` to both.

Install flask using:
`sudo apt install python-flask` and say `Y` to installation.

## Running the Server:
You will need to install packages for python to run correctly:

`pip3 install -r requirements.txt1`

Run with: `python3 server.py`

## Running the Tests:
Tests in this repository were built with Pytest. Pytest has it's documentation [here](https://docs.pytest.org/en/stable/), and you run unit tests by executing the following command at the root of the repository:

`pytest` 

* Note that if you are on Windows you may or may not have to run tests from the `tests` subdirectory, which may require changing file paths for some tests to pass (incidence: 1 of 2 windows developers)


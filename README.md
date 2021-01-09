# Orientation Visualization

This is a simple python script to visualize the 3D orientation of an embedded device. Raw acceleration and angular velocity are ploted as well. The application reads the data in JSON format from a serial port.

![demo](/doc/img/orientation-viz.png)

The application is meant to be used with [Rust 3D Orientation Demo](https://github.com/stefanluethi/rust-3d-orientation-demo).

## Interface

The Application expects the data to be formated as follows:

**Orientation:**
```json
{
    "meas":"angle",
    "values":{
        "x":1.2,
        "y":1.2,
        "z":1.2
    },
    "unit":"°"
}
```

**Acceleration:**
```json
{
    "meas":"acc",
    "values":{
        "x":1.2,
        "y":1.2,
        "z":1.2
    },
    "unit":"g"
}
```

**Angular Velocity:**
```json
{
    "meas":"gyro",
    "values":{
        "x":1.2,
        "y":1.2,
        "z":1.2
    },
    "unit":"dps"
}
```

**Temperature:**
```json
{
    "meas":"temp",
    "values":{
        "T":23.4
    },
    "unit":"°C"
}
```

## Prerequisites

You will need:
- python 3

Preferably install the python requirements in a virtual environment.

```sh
pip install -R requirements.txt
```

## Usage

If not specified otherwise the application will try to open `/dev/ttyACM0`.

```sh
python main.py /dev/ttyACM1
```


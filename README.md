# ina219_meter
INA219 and 100A shunt based current monitoring for signalK

This script is designed to work with generic INA219 I2C IIC Bi-Directional DC Current Power Supply Sensor.
The sensor requires surface mounted 100R resitor to be de-soldered and instead connect it to a 100A/100mv shunt.

The script reads the values and "publishes" volts and amps read from the shunt to SignalK within the standard 'topic' (i.e. vessel/self/..etc) server running on Pi4 on localhost.
SignalK needs to have MQTT plugin installed and configured.

The script depends on the INA219 library. https://pypi.org/project/pi-ina219/
The script needs paho mqtt client to publish the data. https://pypi.org/project/paho-mqtt/


If the script is started via systemctl, the service needs 30 seconds and start after signalk service.

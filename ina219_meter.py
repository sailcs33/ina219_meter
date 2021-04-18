#!/usr/bin/env python3
from ina219 import INA219
from ina219 import DeviceRangeError
import time
from paho.mqtt import client as mqtt_client

#shunt rated resistance (Ohms law. R = E / I --- 100A / (100mV/1000) = .001 Ohm
SHUNT_OHMS = 0.001
ina = INA219(SHUNT_OHMS)


#Check if the INA219 is ready
def ina219_check_func():
    while True:
        try:
            ina.is_conversion_ready()  #check if INA216 is ready
        except OSError:
            print("INA219 is not ready")
            time.sleep(1)
        else:
            if ina.current_overflow():  #if wires to the shunt disconnect this will show FALSE
                print("INA219 is not sensing the shunt")
                time.sleep(1)
            else:
                #if no issues are detected go back to work
                break  

#Configure INA216
ina.configure(ina.RANGE_16V, ina.GAIN_1_40MV, ina.ADC_128SAMP, ina.ADC_12BIT)

# MQTT Broker Info
broker = 'openplotter'
port = 1883
topic_v = "vessels/self/sensors/housebatt/Volt"
topic_a = "vessels/self/sensors/housebatt/Amp"
client_id = 'python-mqtt-001'

#Establish connection to the broker
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client):
#    no_current = 0
    while True:

        time.sleep(2)

        #Check if INA219 is all still good.
        ina219_check_func()

        #Measure volts and amps
        shunt_v = float("{:6.3f}".format (ina.voltage()))
        shunt_a = float("{:6.3f}".format (ina.current() / 1000))

        #send volts if over 11
        if shunt_v >= 11.0:
            client.publish(topic_v, shunt_v)
            #print(f"Sending {shunt_v} Volts")

        #Only send amps if over .5A in either direction
        if abs(shunt_a) >= 0.3:
            client.publish(topic_a, shunt_a)
 #           no_current = 0
            #print(f"Sending {shunt_a} Amps")

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)

run()

import paho.mqtt.client as mqtt
import time
import re
import sys
import serial
import _thread
import queue
import queue
from cloudmqtt import *     # contains all the connection details

### -> indicates debugging print statements

def on_connect(client, userdata, flags, rc):
    if(rc == 0):
        print("Connection Successful")
    else:
        print("Connection Failed!")
        sys.exit(0)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")
        sys.exit(0)

def getInfo(ser,q):
    while(1):
        ser.flush()
        time.sleep(0.1)
        line = str(ser.readline())
        ##print(line)
        numbers = re.findall(":(\d*),(\d*),(\d*),(\d*),(\d*),(\d*);", line)
        ##print("\nnumbers: ",numbers,"\n")
        q.put(numbers)
##        for number in line:
##            ###print(number)
##            return number
    ser.close()


ser = serial.Serial("COM3", baudrate = 57600)
client = mqtt.Client("pythonArduinoSender")
client.on_connect = on_connect
client.on_disconnect = on_disconnect
print("Connecting to broker")
client.loop_start()
client.username_pw_set(username, password)
client.connect(broker, port, 60)
time.sleep(5)
q = queue.Queue()
_thread.start_new_thread(getInfo,(ser,q,))
##getInfo(ser)
i = 0
j = 1
speed1, speed2 = 0,0
while(1):
    try:
        line = q.get()
        client.publish("/python/ultra/left", line[0][0], qos = 1)
        time.sleep(0.1)
        client.publish("/python/ultra/mid", line[0][1], qos = 1)
        time.sleep(0.1)
        client.publish("/python/ultra/right", line[0][2], qos = 1)
        time.sleep(0.1)
        client.publish("/python/speed", line[0][3], qos = 1)
        time.sleep(0.1)
        client.publish("/python/lap/min", line[0][4], qos = 1)
        time.sleep(0.1)
        client.publish("/python/lap/sec", line[0][5], qos = 1)
        time.sleep(0.1)
        print("published ",line )
    except Exception as e:
        print(e)

client.loop_forever()



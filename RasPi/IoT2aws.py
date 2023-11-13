from gpiozero import DistanceSensor

# import boto3

import time
import paho.mqtt.client as mqtt
import ssl
import json
import _thread
import random
from datetime import datetime as dt

def on_connect(client, userdata, flags, response_code):
    print(f'connected to broker: {response_code}')

with open('./brokerPassword.txt', 'r') as f:
    brokerPassword = f.read()

mqttClient = mqtt.Client(protocol=mqtt.MQTTv311)
mqttClient.on_connect = on_connect
# mqttClient.tls_set(ca_certs='./ca.crt')
# mqttClient.tls_set(ca_certs='./ca.crt',certfile='./client.crt',keyfile='./client.key',tls_version=ssl.PROTOCOL_TLSv1_2)
mqttClient.username_pw_set('mqtt', brokerPassword)

mqttClient.tls_insecure_set(True)
mqttClient.connect("192.168.68.114", 1883)

def publish_data(txt):
    print(txt)
    sensor = DistanceSensor(echo=24, trigger=18)

    while True:
        data = sensor.distance * 100
        print(f'distance: {data} cm')
        epochTimestamp = dt.now().strftime('%s')
        valueId = random.choice(['AI00', 'AI01', 'AI02', 'AI03', 'AI04', 'AI05', 'AI06', 'AI07', 'AI08', 'AI09', 'DI00', 'DI01', 'DI02', 'DI03', 'DI04', 'DI05', 'DI06', 'DI07', 'DI08', 'DI09'])
        if 'AI' in valueId:
            dataPayload = json.dumps({'id':valueId,'v': data, 'q':False, 't':epochTimestamp})
        else:
            dataPayload = json.dumps({'id':valueId,'v': random.choice([0,1]), 'q':False, 't':epochTimestamp})
        mqttClient.publish('RasPi/data', payload=dataPayload)
        time.sleep(1)



_thread.start_new_thread(publish_data, ('new thread',))
mqttClient.loop_forever()
from gpiozero import DistanceSensor

# import boto3

import time
import paho.mqtt.client as mqtt
import ssl
import json
import _thread

def on_connect(client, userdata, flags, response_code):
    print(f'connected to AWS IoT status: {response_code}')

mqttClient = mqtt.Client()
mqttClient.on_connect = on_connect
mqttClient.tls_set(ca_certs='./rootCA.pem',certfile='./certificate.pem.crt',keyfile='./private.pem.key',tls_version=ssl.PROTOCOL_SSLv23)
mqttClient.tls_insecure_set(True)
mqttClient.connect("a3nrtfu6i3fchr-ats.iot.ap-southeast-2.amazonaws.com", 8883, 60)

def publish_data(txt):
    print(txt)
    sensor = DistanceSensor(echo=24, trigger=18)

    while True:
        data = sensor.distance * 100
        print(f'distance: {data} cm')
        mqttClient.publish('RasPi/data', payload=json.dumps({'msg': data}))
        time.sleep(1)

_thread.start_new_thread(publish_data, ('new thread',))
mqttClient.loop_forever()
from gpiozero import DistanceSensor

# import boto3

import time
import paho.mqtt.client as mqtt
import json
import _thread
from datetime import datetime as dt

def on_connect(client, userdata, flags, response_code):
    connackString = {0: 'Connection successful',
                      1: 'Connection refused - incorrect protocol version',
                      2: 'Connection refused - invalid client identifier',
                      3: 'Connection refused - server unavailable',
                      4: 'Connection refused - bad username or password',
                      5: 'Connection refused - not authorized'}
    print(f'connected to broker: {connackString[response_code]}')


def publish_data(txt):
    print(txt)
    sensor = DistanceSensor(echo=24, trigger=18)

    while True:
        data = sensor.distance * 100
        epochTimestamp = dt.now().strftime('%s')
        
        dataPayload = json.dumps({'id':'distance','value': data, 'timestamp':epochTimestamp})
        mqttClient.publish('RasPi/data', payload=dataPayload)
        time.sleep(1)


if __name__ == '__main__':
    
    mqttClient = mqtt.Client(protocol=mqtt.MQTTv311)
    mqttClient.tls_set(ca_certs='./rootCA.pem', certfile='./certificate.pem.crt', keyfile='./private.pem.key')
    mqttClient.on_connect = on_connect
    mqttClient.connect("a3nrtfu6i3fchr-ats.iot.ap-southeast-2.amazonaws.com", 8883)
    _thread.start_new_thread(publish_data, ('new thread',))
    mqttClient.loop_forever()
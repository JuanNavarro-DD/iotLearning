from gpiozero import DistanceSensor
import picamera

import time
import paho.mqtt.client as mqtt
import ssl
import json
import _thread

def on_connect(client, userdata, flags, response_code):
    print(f'connected to AWS IoT status: {response_code}')

client = mqtt.Client()
client.on_connect = on_connect
client.tls_set(ca_certs='./rootCA.pem',certfile='./certificate.pem.crt',keyfile='./private.pem.key',tls_version=ssl.PROTOCOL_SSLv23)
client.tls_insecure_set(True)
client.connect("a3nrtfu6i3fchr-ats.iot.ap-southeast-2.amazonaws.com", 8883, 60)

def publish_data(txt):
    print(txt)
    sensor = DistanceSensor(echo=24, trigger=18)
    

    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        camera.start_preview()
        # Camera warm-up time
        time.sleep(2)
        camera.capture('foo.jpg')

    while True:
        data = sensor.distance * 100
        print(f'distance: {data} cm')
        client.publish('RasPi/data', payload=json.dumps({'msg': data}))
        time.sleep(1)

_thread.start_new_thread(publish_data, ('new thread',))
client.loop_forever()
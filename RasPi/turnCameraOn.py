import subprocess
import time
import paho.mqtt.client as mqtt
import logging
import json

_logger = logging.getLogger(__name__)


def startStreaming():
    bash_script = './startStreaming.sh'

    # Start the bash script
    process = subprocess.Popen(bash_script, shell=True)
    time.sleep(300)

    process.terminate()
    try:
        process.communicate(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()

def turn_camera_on(value):
    if value < 20:
        startStreaming()
        _logger.info('camera turned on')

def on_connect(client, userdata, flags, response_code):
    connackString = {0: 'Connection successful',
                      1: 'Connection refused - incorrect protocol version',
                      2: 'Connection refused - invalid client identifier',
                      3: 'Connection refused - server unavailable',
                      4: 'Connection refused - bad username or password',
                      5: 'Connection refused - not authorized'}
    _logger.critical(f'connected to broker: {connackString[response_code]}')

def on_message(client, userdata, message):
    _logger.info(f'received message: {message.payload.decode()}')
    messageDict = json.loads(message.payload.decode())
    turn_camera_on(messageDict['value'])
    client.publish('pong', 'received message')

def mqtt_client(host:str, port:int):
    mqttClient = mqtt.Client()
    mqttClient.tls_set(ca_certs='./rootCA.pem', certfile='./certificate.pem.crt', keyfile='./private.pem.key')
    mqttClient.on_connect = on_connect
    mqttClient.on_message = on_message
    mqttClient.connect(host, port=port)
    

if __name__ == '__main__':
    mqttClient = mqtt_client("a3nrtfu6i3fchr-ats.iot.ap-southeast-2.amazonaws.com", 8883)
    mqttClient.subscribe('RasPi/data')
    mqttClient.loop_forever()
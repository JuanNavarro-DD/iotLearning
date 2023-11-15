import subprocess
import time
import threading
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient as mqttClient
import logging
import os
import signal
import json

_logger = logging.getLogger(__name__)


def startStreaming():
    bash_script = './startStreaming.sh'
    global trigger_flag

    # Start the bash script
    process = subprocess.Popen(['/bin/bash',bash_script], start_new_session=True)
    time.sleep(60)

    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    

    process.terminate()
    process.wait()
    trigger_flag = True
    threading.Timer(30.0, reset_trigger_flag).start()
    try:
        process.communicate(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()

def turn_camera_on(value):
    global trigger_flag
    if value < 10 and not trigger_flag:
        startStreaming()
        _logger.critical('camera turned on')
def reset_trigger_flag():
    global trigger_flag
    trigger_flag = False

def on_connect(client, userdata, flags, response_code):
    connackString = {0: 'Connection successful',
                      1: 'Connection refused - incorrect protocol version',
                      2: 'Connection refused - invalid client identifier',
                      3: 'Connection refused - server unavailable',
                      4: 'Connection refused - bad username or password',
                      5: 'Connection refused - not authorized'}
    _logger.critical(f'connected to broker: {connackString[response_code]}')

def on_message(client, userdata, message):
    print(f'received message: {message.payload.decode()}')
    _logger.critical(f'received message: {message.payload.decode()}')
    messageDict = json.loads(message.payload.decode())
    turn_camera_on(messageDict['value'])

# def mqtt_client(host:str, port:int):
#     mqttClient = mqtt.Client()
#     mqttClient.tls_set(ca_certs='./readerKeys/rootCA.pem', certfile='./readerKeys/certificate.pem.crt', keyfile='./readerKeys/private.pem.key')
#     mqttClient.on_connect = on_connect
#     mqttClient.on_message = on_message
#     mqttClient.connect(host, port=port)
#     return mqttClient
    

if __name__ == '__main__':
    trigger_flag = False
    myMqttClient = mqttClient('myClient')
    myMqttClient.configureEndpoint("a3nrtfu6i3fchr-ats.iot.ap-southeast-2.amazonaws.com", 8883)
    myMqttClient.configureCredentials("./readerKeys/rootCA.pem", "./readerKeys/private.pem.key", "./readerKeys/certificate.pem.crt")
    myMqttClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    myMqttClient.configureDrainingFrequency(2)  # Draining: 2 Hz
    myMqttClient.configureConnectDisconnectTimeout(10)  # 10 sec
    myMqttClient.configureMQTTOperationTimeout(5)  # 5 sec

    myMqttClient.connect()
    myMqttClient.subscribe('RasPi/data', 1, on_message)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('Disconnecting...')
        myMqttClient.disconnect()
        print('Disconnected')

    # mqttClient = mqtt_client("a3nrtfu6i3fchr-ats.iot.ap-southeast-2.amazonaws.com", 8883)
    # mqttClient.subscribe('RasPi/data')
    # mqttClient.loop_forever()
# OW - IOT
This repo will contain all the code for the IOT projects using Raspberry pi and Arduino in AWS.


## Raspberry Pi
For the different projects in this repo we will need to set up a user in the raspberry pi. To do this we will need to run the following steps:

1. Create a new user in the AWS account that we want the raspberry pi to be connected to. This can be done by an admin of the AWS account. The raspberry pi user does not need console access
2. Set up the raspberry pi with the new user credentials. This can be done by running the following command in the raspberry pi terminal:
```bash
aws configure
```
This requires aws cli to be installed in the raspberry pi. To install aws cli run the following command:
```bash
sudo apt-get install awscli
```

### Raspberry Pi - AWS IoT
In this project we have a Raspberry Pi Zero W connected to an ultrasonic sensor. The raspberry pi will send the distance measured by the sensor to AWS IoT through mqtt. The raspberry pi is also subscribed to a topic in AWS IoT and will receive messages from AWS IoT. The raspberry pi will then turn the camera on depending on the distance measured by the sensor and start streaming video to AWS Kinesis Video Streams.

Both, the sensor data and video stream, will be part of a scene in AWS TwinMaker. The scene will be displayed in a grafana dashboard.

#### Raspberry Pi - AWS IoT - Kinesis Video Streams
To stream video from the raspberry pi to AWS Kinesis Video Streams we will need to configure the raspberry pi to use the camera module. To do this we will need to run the following command in the raspberry pi terminal:
```bash
sudo raspi-config
```
Then select the following options:
1. Interfacing Options
2. Legacy Camera
3. Enable

Once the camera is enabled we will need to download and build the Kinesis Video Streams Producer SDK for C++ in the raspberry pi. To do this we will need to run the following commands in the raspberry pi terminal:
```bash
sudo apt-get update
git clone https://github.com/awslabs/amazon-kinesis-video-streams-producer-sdk-cpp.git
mkdir -p amazon-kinesis-video-streams-producer-sdk-cpp/build
cd amazon-kinesis-video-streams-producer-sdk-cpp/build
cmake .. -DBUILD_GSTREAMER_PLUGIN=ON -DBUILD_DEPENDENCIES=FALSE
make
```

The [startStreaming.sh](RasPi/startStreaming.sh) script will start the video streaming from the raspberry pi to AWS Kinesis Video Streams. This script gets run from the [turnCameraOn.py](RasPi/turnCameraOn.py) script.

## AWS IoT
This project uses AWS IoT to send and receive messages from the raspberry pi. The raspberry pi will send the distance measured by the sensor to AWS IoT through mqtt. The raspberry pi is also subscribed to a topic in AWS IoT and will receive messages from AWS IoT core. The raspberry pi will then turn the camera on depending on the distance measured by the sensor and start streaming video to AWS Kinesis Video Streams. An IoT Twin Maker workspace is configured to display the scene in a grafana dashboard.

Most of the configuration and services for this project are deployed using cdk. There are some configurations such as the IoT Core Thing connection that are needed to be done manually because they use certificates to connect the raspberry pi to AWS IoT. This code is available in the [stack folder](RasPi/IoTTwinMaker).
### AWS IoT - IoT Core
IoT Core is used to send and receive messages from the raspberry pi. The raspberry pi will send the distance measured by the sensor to AWS IoT through mqtt. The raspberry pi is also subscribed to a topic in AWS IoT and will receive messages from AWS IoT core. There is a rule in IoT Core that will send the messages received from the raspberry pi to IoT SiteWise.

### AWS IoT - IoT SiteWise
IoT Site Wise is used as the bridge between IoT Core and IoT Twin Maker. IoT SiteWise will receive the sensor data from IoT Core and will send it to IoT Twin Maker. This is done using the IoT site Wise connector already defined in IoT Twin Maker.

### AWS IoT - IoT Twin Maker
IoT Twin Maker is used to display the scene in a grafana dashboard. In IoT twin maker a scene is created using 3D models found online and the sensor data received from IoT SiteWise. The scene is then displayed in a grafana dashboard as well as the video streaming and the sensor data.


# References
1. [AWS Kinesis Video Streams Producer SDK for C++](https://docs.aws.amazon.com/kinesisvideostreams/latest/dg/producersdk-cpp-rpi-download.html)
2. [AWS cdk python documentation](https://docs.aws.amazon.com/cdk/api/v2/python/)
3. [3D models](https://www.turbosquid.com/)
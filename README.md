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

# References
1. [AWS Kinesis Video Streams Producer SDK for C++](https://docs.aws.amazon.com/kinesisvideostreams/latest/dg/producersdk-cpp-rpi-download.html)
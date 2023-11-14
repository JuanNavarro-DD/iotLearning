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


export GST_PLUGIN_PATH='~/amazon-kinesis-video-streams-producer-sdk-cpp/build'
export AWS_DEFAULT_REGION='ap-southeast-2'
export AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id)
export AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key)
cd ~/amazon-kinesis-video-streams-producer-sdk-cpp/build/



./kvs_gstreamer_sample RaspberryPiCamera

wait  # Wait for child processes to exit
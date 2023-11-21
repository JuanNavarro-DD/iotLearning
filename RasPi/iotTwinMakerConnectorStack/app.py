#!/usr/bin/env python3
import os

import aws_cdk as cdk

from iot_twin_maker_connector_stack.iot_twin_maker_connector_stack_stack import IotTwinMakerConnectorStackStack


app = cdk.App()
IotTwinMakerConnectorStackStack(app, "IotTwinMakerConnectorStackStack")

app.synth()

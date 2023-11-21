import aws_cdk as core
import aws_cdk.assertions as assertions

from iot_twin_maker_connector_stack.iot_twin_maker_connector_stack_stack import IotTwinMakerConnectorStackStack

# example tests. To run these tests, uncomment this file along with the example
# resource in iot_twin_maker_connector_stack/iot_twin_maker_connector_stack_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = IotTwinMakerConnectorStackStack(app, "iot-twin-maker-connector-stack")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })

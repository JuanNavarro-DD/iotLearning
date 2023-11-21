import aws_cdk as core
import aws_cdk.assertions as assertions

from iot_twin_maker_connector_stack.iot_twin_maker_connector_stack_stack import IotTwinMakerConnectorStackStack

# example tests. To run these tests, uncomment this file along with the example
# resource in iot_twin_maker_connector_stack/iot_twin_maker_connector_stack_stack.py
def test_lambda_runtime():
    app = core.App()
    stack = IotTwinMakerConnectorStackStack(app, "iot-twin-maker-connector-stack")
    template = assertions.Template.from_stack(stack )

    template.has_resource_properties("AWS::Lambda::Function", {
        "Runtime": "python3.12"
    })
    template.resource_properties_count_is("AWS::Lambda::Function", {"Runtime":"python3.12"}, 2)
def test_schema_init_lambda_created():
    app = core.App()
    stack = IotTwinMakerConnectorStackStack(app, "iot-twin-maker-connector-stack")
    template = assertions.Template.from_stack(stack )

    template.has_resource_properties("AWS::Lambda::Function", {
        "Handler": "schemaInitializer.handler"
    })

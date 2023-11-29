import aws_cdk as core
import aws_cdk.assertions as assertions

from io_t_twin_maker.io_t_twin_maker_stack import IoTTwinMakerStack

# example tests. To run these tests, uncomment this file along with the example
# resource in io_t_twin_maker/io_t_twin_maker_stack.py
def test_iot_TM_workspace():
    app = core.App()
    stack = IoTTwinMakerStack(app, "io-t-twin-maker")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::IoTTwinMaker::Workspace", {
        "WorkspaceId": "DLearnWorkspace"
    })
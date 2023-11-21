from aws_cdk import (
    Stack,
    aws_iottwinmaker as iottwinmaker,
    aws_lambda as _lambda,
    Duration
)
from constructs import Construct

class IotTwinMakerConnectorStackStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        readDynamoDbTableIoTLambda = _lambda.Function(self, 'readDynamoDbTableIoTLambda',
                                                        runtime=_lambda.Runtime.PYTHON_3_12,
                                                        code=_lambda.Code.from_asset('readDynamoDbTableIoT'),
                                                        handler='readDynamoTable.handler',
                                                        timeout=Duration.seconds(300),
                                                        )
        
        schemaInitializerIoTLambda = _lambda.Function(self, 'schemaInitializerIoTLambda',
                                                        runtime=_lambda.Runtime.PYTHON_3_12,
                                                        code=_lambda.Code.from_asset('schemaInitializerIoT'),
                                                        handler='schemaInitializer.handler',
                                                        timeout=Duration.seconds(300),
                                                        )

        twinMakerDynamoComponent = iottwinmaker.CfnComponentType(self, 'twinMakerDynamoComponent',
                                                             component_type_id="com.DLearn.DynamoDb.TwinMaker",
                                                             workspace_id="IoTDLearnTwinMaker",
                                                             description="creates connection to dynamoDB",
                                                             functions={
                                                                 "dataReader": iottwinmaker.CfnComponentType.FunctionProperty(
                                                                     implemented_by=iottwinmaker.CfnComponentType.DataConnectorProperty(
                                                                         is_native=False,
                                                                         lambda_=iottwinmaker.CfnComponentType.LambdaFunctionProperty(
                                                                             arn=readDynamoDbTableIoTLambda.function_arn
                                                                         )
                                                                     )
                                                                 ),
                                                                 "schemaInitializer": iottwinmaker.CfnComponentType.FunctionProperty(
                                                                     implemented_by=iottwinmaker.CfnComponentType.DataConnectorProperty(
                                                                         is_native=False,
                                                                         lambda_=iottwinmaker.CfnComponentType.LambdaFunctionProperty(
                                                                             arn=schemaInitializerIoTLambda.function_arn
                                                                         )
                                                                     )
                                                                 )
                                                             },
                                                             is_singleton=False,
                                                             tags={"projectName":"IoTDLearnTwinMaker"},
        )

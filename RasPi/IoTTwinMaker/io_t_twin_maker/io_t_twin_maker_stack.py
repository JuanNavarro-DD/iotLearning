from aws_cdk import (
    # Duration,
    Stack,
    aws_iottwinmaker as iottwinmaker,
    aws_iot as iot,
    aws_iotsitewise as iotsitewise,
    aws_s3 as s3,
    RemovalPolicy,
    aws_iam as iam,
    aws_kinesisvideo as kinesisvideo,
    aws_kms as kms,
    CfnTag
)
from constructs import Construct

class IoTTwinMakerStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        iotTwinMakerBucket = s3.Bucket(self, "IoTTwinMakerBucket",
                                       bucket_name="iot-twin-maker",
                                       removal_policy=RemovalPolicy.DESTROY,
                                       auto_delete_objects=True,
                                       block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
                                       )
        
        videoStream = kinesisvideo.CfnStream(self, "VideoStream",
                                            data_retention_in_hours=2,
                                            device_name="RaspiCamera",
                                            name="RaspiCameraStream",
                                            tags=[CfnTag(key="Project", value="DLearnIoT")]
                                            )

        siteWiseModel = iotsitewise.CfnAssetModel(self, "SiteWiseModel",
                                                    asset_model_name="DistanceSensorModel",
                                                    asset_model_description="Distance Sensor Model",
                                                    asset_model_properties=[iotsitewise.CfnAssetModel.AssetModelPropertyProperty(
                                                        data_type="DOUBLE",
                                                        name="Distance",
                                                        logical_id="Distance",
                                                        type=iotsitewise.CfnAssetModel.PropertyTypeProperty(
                                                            type_name="Measurement"
                                                        ),
                                                        unit="cm"),
                                                        iotsitewise.CfnAssetModel.AssetModelPropertyProperty(
                                                            data_type="STRING",
                                                            name="Raspberry ID",
                                                            logical_id="RaspiId",
                                                            type=iotsitewise.CfnAssetModel.PropertyTypeProperty(
                                                                type_name="Attributes"
                                                            ),
                                                        )
                                                        ]
                                                    )
        
        raspiAsset = iotsitewise.CfnAsset(self, "RaspiAsset",
                                          asset_name="DistanceRaspi",
                                          asset_model_id=siteWiseModel.attr_asset_model_id,
                                          tags=[CfnTag(key="Project", value="DLearnIoT")]
                                          )
        

        iotTwinMakerRole = iam.Role(self, "IoTTwinMakerRole",
                                    assumed_by=iam.ServicePrincipal("iottwinmaker.amazonaws.com"),
                                    role_name="IoTTwinMakerRole",
                                    )
        s3Policy = iam.PolicyStatement(
            actions=["s3:GetBucket*", "s3:GetObject", "s3:ListBucket","s3:PutObject", "s3:DeleteObject"],
            effect=iam.Effect.ALLOW,
            resources=[iotTwinMakerBucket.bucket_arn + "/*"]
        )
        iotSiteWisePolicy = iam.PolicyStatement(
            actions=["iotsitewise:*"],
            effect=iam.Effect.ALLOW,
            resources=[raspiAsset.attr_asset_arn]
        )

        distanceThing = iot.CfnThing(self, "DistanceThing",
                                     thing_name="DistanceRasPiSensor"
                                     )

        DLearnWorkspace = iottwinmaker.CfnWorkspace(self, "DLearnWorkspace",
                                                    role="",
                                                    s3_location=iotTwinMakerBucket.bucket_arn,
                                                    workspace_id="DLearnWorkspace",
                                                    description="IoT Twin Maker Sensor Workspace",
                                                    tags={
                                                        "Project": "DLearnIoT",
                                                    }
                                                    # workspace_data_retention_period=Duration.days(7),
                                                )
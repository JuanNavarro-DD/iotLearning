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
        
        kinesisVideoKey = kms.Key(self, "KinesisVideoKey",
                                alias="KinesisVideoKey",
                                description="Kinesis Video Key",
                                removal_policy=RemovalPolicy.DESTROY,
                                enabled=True,
                                enable_key_rotation=True,
                                )
        
        videoStream = kinesisvideo.CfnStream(self, "VideoStream",
                                            data_retention_in_hours=2,
                                            device_name="RaspiCamera",
                                            name="RaspiCameraStream",
                                            kms_key_id=kinesisVideoKey.key_id,
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
                                                                type_name="Attribute"
                                                            ),
                                                        )
                                                        ]
                                                    )
        
        raspiAsset = iotsitewise.CfnAsset(self, "RaspiAsset",
                                          asset_name="DistanceRaspi",
                                          asset_model_id=siteWiseModel.attr_asset_model_id,
                                          asset_properties=[iotsitewise.CfnAsset.AssetPropertyProperty(
                                              logical_id="Distance",
                                              alias="raspi/Distance")],
                                          tags=[CfnTag(key="Project", value="DLearnIoT")]
                                          )
        
        s3Policy = iam.PolicyStatement(
            actions=["s3:GetBucket*", "s3:GetObject", "s3:ListBucket","s3:PutObject", "s3:DeleteObject"],
            effect=iam.Effect.ALLOW,
            resources=[iotTwinMakerBucket.bucket_arn, iotTwinMakerBucket.arn_for_objects("*")]
        )
        iotSiteWisePolicy = iam.PolicyStatement(
            actions=["iotsitewise:*"],
            effect=iam.Effect.ALLOW,
            resources=[raspiAsset.attr_asset_arn]
        )

        iotTwinMakerRole = iam.Role(self, "IoTTwinMakerRole",
                                    assumed_by=iam.ServicePrincipal("iottwinmaker.amazonaws.com"),
                                    role_name="IoTTwinMakerRole",
                                    inline_policies={'IoTTwinMakerPolicy': iam.PolicyDocument(
                                        statements=[s3Policy,iotSiteWisePolicy]
                                    )}
                                    )
        



        distanceThing = iot.CfnThing(self, "DistanceThing",
                                     thing_name="DistanceRasPiSensor"
                                     )
        
        routingMqttRepublishPolicy = iam.PolicyStatement(
            actions=["iotsitewise:BatchPutAssetPropertyValue"],
            effect=iam.Effect.ALLOW,
            resources=[raspiAsset.attr_asset_arn]
        )
        timeSeriesMqttRepublishPolicy = iam.PolicyStatement(
            actions=["iotsitewise:BatchPutAssetPropertyValue"],
            effect=iam.Effect.ALLOW,
            resources=[f"arn:aws:iotsitewise:{self.region}:{self.account}:time-series/*"],
            conditions={"StringLike":{"iotsitewise:propertyAlias": ["raspi/Distance"]}}
        )
        routingRole = iam.Role(self, "RoutingRole",
                               assumed_by=iam.ServicePrincipal("iot.amazonaws.com"),
                               role_name="RoutingRole",
                               inline_policies={'RoutingPolicy': iam.PolicyDocument(
                                   statements=[routingMqttRepublishPolicy, timeSeriesMqttRepublishPolicy]
                               )}
                               )
        
        routingRule = iot.CfnTopicRule(self, "RoutingRule",
                                        rule_name="RoutingRule",
                                        topic_rule_payload=iot.CfnTopicRule.TopicRulePayloadProperty(
                                             sql="SELECT value FROM 'Raspi/distance' WHERE id = 'distance'",
                                             aws_iot_sql_version="2016-03-23",
                                             actions=[iot.CfnTopicRule.ActionProperty(
                                                  iot_site_wise=iot.CfnTopicRule.IotSiteWiseActionProperty(
                                                        put_asset_property_value_entries=[iot.CfnTopicRule.PutAssetPropertyValueEntryProperty(
                                                            property_values=[iot.CfnTopicRule.AssetPropertyValueProperty(
                                                                timestamp=iot.CfnTopicRule.AssetPropertyTimestampProperty(
                                                                    time_in_seconds="${floor(timestamp() / 1E3)}"
                                                                ),
                                                                value=iot.CfnTopicRule.AssetPropertyVariantProperty(
                                                                    double_value="${value}"
                                                                )
                                                            )],
                                                            property_alias="raspi/Distance",
                                                            asset_id=raspiAsset.attr_asset_id,
                                                            # property_id=siteWiseModel.attr_asset_model_id
                                                        )],
                                                        role_arn=routingRole.role_arn
                                                  )
                                             )]
                                        ),
                                        tags=[CfnTag(key="Project", value="DLearnIoT")]
                                        )

        DLearnWorkspace = iottwinmaker.CfnWorkspace(self, "DLearnWorkspace",
                                                    role=iotTwinMakerRole.role_arn,
                                                    s3_location=iotTwinMakerBucket.bucket_arn,
                                                    workspace_id="DLearnWorkspace",
                                                    description="IoT Twin Maker Sensor Workspace",
                                                    tags={
                                                        "Project": "DLearnIoT",
                                                    }
                                                    # workspace_data_retention_period=Duration.days(7),
                                                )
    
from aws_cdk import (
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
    aws_s3 as s3,
    Stack,
)
from aws_cdk.aws_lambda_python_alpha import PythonFunction, PythonLayerVersion
from constructs import Construct
import os


class ThumbnailSwitchStack(Stack):

    def __init__(self, scope: Construct, id: str, dependencies_layer: PythonLayerVersion, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Read video ID from environment variable
        video_id = os.getenv('VIDEO_ID', 'default_video_id')

        # Create S3 bucket for credentials
        bucket = s3.Bucket(self, "ephemeral-z90d7fs9dfwq")

        # Define Lambda thumbnail_switch
        thumbnail_switcher_lambda = PythonFunction(
            self, "ThumbnailSwitchFunction",
            entry="lambda/thumbnail_switch",  # The directory where your handler.py and requirements.txt are
            runtime=lambda_.Runtime.PYTHON_3_9,
            index="index.py",  # The file containing the handler thumbnail_switch
            handler="lambda_handler",
            layers=[dependencies_layer],
            environment={
                "S3_BUCKET_NAME": bucket.bucket_name,
                "S3_OBJECT_KEY": "cred.json",
                "VIDEO_ID": video_id
            }
        )

        # Grant Lambda permissions to read from S3
        bucket.grant_read(thumbnail_switcher_lambda)

        # Define API Gateway
        api = apigateway.RestApi(self, "thumbnail-switcher-api",
            rest_api_name="Thumbnail Switcher Service",
            description="This service switches YouTube thumbnails."
        )

        thumbnail_resource = api.root.add_resource("thumbnail")
        thumbnail_resource.add_method("POST", apigateway.LambdaIntegration(thumbnail_switcher_lambda),
                                      api_key_required=False)

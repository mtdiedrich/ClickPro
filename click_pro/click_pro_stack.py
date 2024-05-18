from aws_cdk import (
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
    aws_s3 as s3,
    aws_lambda_python_alpha as lambda_python,
    Stack,
)
from constructs import Construct
import os


class ClickProStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Read video ID from environment variable
        video_id = os.getenv('VIDEO_ID', 'default_video_id')

        # Create S3 bucket for credentials
        bucket = s3.Bucket(self, "ephemeral-z90d7fs9dfwq")

        # Define Lambda function with bundling
        thumbnail_switcher_lambda = lambda_python.PythonFunction(
            self, "ThumbnailSwitcherFunction",
            entry="lambda",  # The directory where your handler.py and requirements.txt are
            runtime=lambda_.Runtime.PYTHON_3_9,
            index="handler.py",  # The file containing the handler function
            handler="lambda_handler",
            bundling={
                "pip": True,  # Use Docker to install dependencies with pip
            },
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

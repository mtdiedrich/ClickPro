from aws_cdk import (
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
    aws_s3 as s3,
    Stack,
)
from aws_cdk.aws_lambda_python_alpha import PythonFunction, PythonLayerVersion
from constructs import Construct


class ThumbnailDownloadStack(Stack):

    def __init__(self, scope: Construct, id: str, dependencies_layer: PythonLayerVersion, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create S3 bucket for thumbnails
        bucket = s3.Bucket(self, "ephemeral-thumbnails")

        # Define thumbnail downloader Lambda thumbnail_switch
        thumbnail_downloader_lambda = PythonFunction(
            self, "ThumbnailDownloadFunction",
            entry="lambda/thumbnail_download",
            runtime=lambda_.Runtime.PYTHON_3_9,
            index="index.py",
            handler="lambda_handler",
            layers=[dependencies_layer],
            environment={
                "S3_BUCKET_NAME": bucket.bucket_name
            }
        )

        # Grant Lambda permissions to write to S3
        bucket.grant_write(thumbnail_downloader_lambda)

        # Define API Gateway
        api = apigateway.RestApi(self, "thumbnail-download-api",
            rest_api_name="Thumbnail Download Service",
            description="This service downloads YouTube thumbnails."
        )

        downloader_resource = api.root.add_resource("download-thumbnail")
        downloader_resource.add_method("POST", apigateway.LambdaIntegration(thumbnail_downloader_lambda), api_key_required=False)

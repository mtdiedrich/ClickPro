from aws_cdk import (
    cdk,
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
    aws_s3 as s3,
)

class ClickProStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create S3 bucket for credentials
        bucket = s3.Bucket(self, "YouTubeCredentialsBucket")

        # Define Lambda function
        thumbnail_switcher_lambda = lambda_.Function(
            self, "ThumbnailSwitcherFunction",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="handler.lambda_handler",
            code=lambda_.Code.from_asset("lambda"),
            environment={
                "S3_BUCKET_NAME": bucket.bucket_name,
                "S3_OBJECT_KEY": "path/to/credentials.json",
                "VIDEO_ID": "your_video_id"
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


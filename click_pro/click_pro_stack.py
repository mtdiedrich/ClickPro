from aws_cdk import (
    core,
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
    aws_s3 as s3,
    aws_s3_assets as s3_assets
)

class ClickProStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create S3 bucket for credentials
        bucket = s3.Bucket(self, "ephemeral-z90d7fs9dfwq")

        # Upload the deployment package to S3
        s3_deployment = s3_assets.Asset(self, "LambdaPackage",
            path="lambda/lambda_package.zip"
        )

        # Define Lambda function
        thumbnail_switcher_lambda = lambda_.Function(
            self, "ThumbnailSwitcherFunction",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="handler.lambda_handler",
            code=lambda_.Code.from_bucket(s3_deployment.bucket, s3_deployment.s3_object_key),
            environment={
                "S3_BUCKET_NAME": bucket.bucket_name,
                "S3_OBJECT_KEY": "cred.json",
                "VIDEO_ID": "ZhIUkujgPu0"
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

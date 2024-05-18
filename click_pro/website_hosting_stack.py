from aws_cdk import (
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    Stack,
)
from constructs import Construct
import aws_cdk as cdk

class WebsiteHostingStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create S3 bucket for hosting the website
        website_bucket = s3.Bucket(self, "WebsiteBucket",
            website_index_document="index.html",
            website_error_document="error.html",
            public_read_access=True,
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        # Deploy website contents to S3 bucket
        s3deploy.BucketDeployment(self, "DeployWebsite",
            sources=[s3deploy.Source.asset("./website")],
            destination_bucket=website_bucket,
        )

        # Output the website URL
        cdk.CfnOutput(self, "WebsiteURL",
            value=website_bucket.bucket_website_url
        )

        self.website_bucket = website_bucket

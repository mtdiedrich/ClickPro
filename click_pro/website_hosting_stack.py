from aws_cdk import (
    aws_s3 as s3,
    Stack,
    RemovalPolicy
)
from constructs import Construct

class WebsiteHostingStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create S3 bucket for hosting the website
        website_bucket = s3.Bucket(self, "WebsiteBucket",
            website_index_document="index.html",
            public_read_access=True,
            removal_policy=RemovalPolicy.DESTROY
        )

        self.website_bucket = website_bucket

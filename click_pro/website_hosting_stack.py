from aws_cdk import (
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    aws_iam as iam,
    aws_lambda as lambda_,
    Stack,
    Duration,
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
            removal_policy=cdk.RemovalPolicy.DESTROY,
            block_public_access=s3.BlockPublicAccess.BLOCK_ACLS
        )

        # Define bucket policy to allow public read access
        website_bucket.add_to_resource_policy(
            iam.PolicyStatement(
                actions=["s3:GetObject"],
                resources=[f"{website_bucket.bucket_arn}/*"],
                principals=[iam.AnyPrincipal()]
            )
        )

        # Deploy website contents to S3 bucket
        s3deploy.BucketDeployment(self, "DeployWebsite",
            sources=[s3deploy.Source.asset("./website")],
            destination_bucket=website_bucket,
            bundling=cdk.BundlingOptions(
                image=lambda_.Runtime.PYTHON_3_9.bundling_docker_image,
            )
        )

        # Output the website URL
        cdk.CfnOutput(self, "WebsiteURL",
            value=website_bucket.bucket_website_url
        )

        self.website_bucket = website_bucket

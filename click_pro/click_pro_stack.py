from aws_cdk import (
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
    aws_s3 as s3,
    Stack,
)
from aws_cdk.aws_lambda_python_alpha import PythonFunction, PythonLayerVersion
from constructs import Construct
import os

from thumbnail_switch_stack import ThumbnailSwitchStack
from thumbnail_download_stack import ThumbnailDownloadStack

class ClickProStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Define Lambda layer for dependencies
        dependencies_layer = PythonLayerVersion(
            self, "DependenciesLayer",
            entry="lambda/dependencies",
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_9]
        )

        ThumbnailDownloadStack(self, "ThumbnailDownloadStack", dependencies_layer)
        ThumbnailSwitchStack(self, "ThumbnailSwitchStack", dependencies_layer)
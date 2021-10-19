from aws_cdk import core as cdk
from xgboost_mlops.stacks import PlatformStack, TrainingStack, HostingStack

class TrainingStage(cdk.Stage):
    def __init__(self, scope: cdk.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        platform = PlatformStack(self, "PlatformStack")
        training = TrainingStack(self, "TrainingStack")

        # Outputs
        self.bucket_name = platform.bucket_name
        self.role_arn = platform.role_arn


class HostingStage(cdk.Stage):
    def __init__(self, scope: cdk.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        hosting = HostingStack(self, "HostingStack")

        # Outputs
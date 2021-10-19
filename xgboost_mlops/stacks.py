from aws_cdk import (
    core as cdk,
    aws_iam as iam,
    aws_s3 as s3
)


class PlatformStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(self,
            "xgboost_demo_bucket",
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        role = iam.Role(self,
            "sagemaker-training-full",
            role_name="PlatformRole",
            assumed_by=iam.ServicePrincipal('sagemaker.amazonaws.com'),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name('AmazonSageMakerFullAccess')
            ]
        )

        # Output
        self.bucket_name = cdk.CfnOutput(self,
            "BucketName",
            value=bucket.bucket_name
        )
        self.role_arn = cdk.CfnOutput(self,
            "RoleArn",
            value=role.role_arn
        )


class TrainingStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        role = iam.Role(self,
            'sagemaker-full',
            role_name="TrainingRole",
            assumed_by=iam.ServicePrincipal('sagemaker.amazonaws.com'),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name('AmazonSageMakerFullAccess')]
        )


class HostingStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        role = iam.Role(self,
            'sagemaker-full',
            role_name="HostingRole",
            assumed_by=iam.ServicePrincipal('sagemaker.amazonaws.com'),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name('AmazonSageMakerFullAccess')]
        )

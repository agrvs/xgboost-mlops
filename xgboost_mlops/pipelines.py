from aws_cdk import core as cdk
from aws_cdk import aws_codepipeline as aws_pipeline
from aws_cdk import aws_codepipeline_actions as aws_pipeline_actions
from aws_cdk import pipelines
from stages import HostingStage, TrainingStage


class TrainingPipelineStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        source_artifact = aws_pipeline.Artifact()
        cloud_assembly_artifact = aws_pipeline.Artifact()

        training_pipeline = pipelines.CdkPipeline(self, "TrainingPipeline",
            cloud_assembly_artifact=cloud_assembly_artifact,
            pipeline_name="TrainingPipeline",

            source_action=aws_pipeline_actions.GitHubSourceAction(
                action_name="GitHub",
                output=source_artifact,
                oauth_token=cdk.SecretValue.secrets_manager("sagemaker-cdk-demo"),
                owner="agrvs",
                repo="xgboost-mlops",
                trigger=aws_pipeline_actions.GitHubTrigger.POLL
            ),

            synth_action=pipelines.SimpleSynthAction(
                source_artifact=source_artifact,
                cloud_assembly_artifact=cloud_assembly_artifact,
                install_command="npm install -g aws-cdk && pip install -r requirements.txt",
                synth_command="cdk synth"
            )
        )


class HostingPipelineStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        source_artifact = aws_pipeline.Artifact()
        cloud_assembly_artifact = aws_pipeline.Artifact()

        hosting_pipeline = pipelines.CdkPipeline(self, "HostingPipeline",
            cloud_assembly_artifact=cloud_assembly_artifact,
            pipeline_name="HostingPipeline",

            source_action=aws_pipeline_actions.GitHubSourceAction(
                action_name="GitHub",
                output=source_artifact,
                oauth_token=cdk.SecretValue.secrets_manager("sagemaker-cdk-demo"),
                owner="agrvs",
                repo="xgboost-mlops",
                trigger=aws_pipeline_actions.GitHubTrigger.POLL
            ),

            synth_action=pipelines.SimpleSynthAction(
                source_artifact=source_artifact,
                cloud_assembly_artifact=cloud_assembly_artifact,
                install_command="npm install -g aws-cdk && pip install -r requirements.txt",
                synth_command="cdk synth"
            )
        )
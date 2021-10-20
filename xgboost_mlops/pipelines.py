from aws_cdk import(
    core as cdk,
    aws_codepipeline as aws_pipeline,
    aws_codepipeline_actions as aws_pipeline_actions,
    aws_iam as iam,
    pipelines
)
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
                synth_command="cdk synth TrainingPipelineStack"
            )
        )

        dev_app = TrainingStage(self, 'dev')
        dev_pipeline = training_pipeline.add_application_stage(dev_app)

        # UploadData
        dev_pipeline.add_actions(pipelines.ShellScriptAction(
            action_name="UploadData",
            run_order=dev_pipeline.next_sequential_run_order(),
            additional_artifacts=[source_artifact],
            commands=[
                "pip install boto3 sagemaker",
                "python3 xgboost_mlops/scripts/upload_data.py"
            ],
            role_policy_statements=[
                iam.PolicyStatement(
                    sid="UploadDataPolicy",
                    effect=iam.Effect.ALLOW,
                    actions=["*"],
                    resources=["*"]
                )
            ],
            use_outputs={
                "BUCKET": training_pipeline.stack_output(dev_app.bucket_name)
            }
        ))

        # StartTraining
        # dev_pipeline.add_actions(pipelines.ShellScriptAction(
        #     action_name="StartTraining",
        #     run_order=dev_pipeline.next_sequential_run_order(),
        #     additional_artifacts=[source_artifact],
        #     commands=[
        #         'pip install boto3 sagemaker',
        #         'python3 xgboost_mlops/scripts/start_training.py'
        #     ],
        #     role_policy_statements=[
        #         iam.PolicyStatement(
        #             sid='PipelinePolicy',
        #             effect=iam.Effect.ALLOW,
        #             actions=['*'],
        #             resources=['*']
        #     )],
        #     use_outputs={
        #         'BUCKET': training_pipeline.stack_output(dev_app.bucket_name),
        #         'ROLE': training_pipeline.stack_output(dev_app.role_arn)
        #     }
        # ))


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
                synth_command="cdk synth HostingPipelineStack"
            )
        )

        dev_app = HostingStage(self, 'dev')
        dev_pipeline = hosting_pipeline.add_application_stage(dev_app)

        # Hosting
        dev_pipeline.add_actions(pipelines.ShellScriptAction(
            action_name="Hosting",
            run_order=dev_pipeline.next_sequential_run_order(),
            additional_artifacts=[source_artifact],
            commands=[
                # "pip install boto3 sagemaker",
                "echo 'Hello World'"
            ],
            role_policy_statements=[
                iam.PolicyStatement(
                    sid="HostingPolicy",
                    effect=iam.Effect.ALLOW,
                    actions=["*"],
                    resources=["*"]
                )
            ],
            use_outputs={
                "ROLE_ARN": hosting_pipeline.stack_output(dev_app.role_arn)
            }
        ))
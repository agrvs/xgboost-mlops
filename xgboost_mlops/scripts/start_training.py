import os, boto3, sagemaker, time
from datetime import datetime

role = sagemaker.get_execution_role()
region = boto3.Session().region_name
sm = boto3.client("sagemaker", region_name=region)
hosting_pipeline = boto3.client('codepipeline')

bucket = os.getenv('BUCKET')
role = os.getenv('ROLE')
print(f"bucket: {bucket}")
# parameter_store

prefix = "sagemaker/xgboost-demo/data"
output_prefix = "output"
container = sagemaker.image_uris.retrieve("xgboost", region, "1.3-1")

now = datetime.now()
job_name = f"demo-xgboost-{now.strftime('%Y-%m-%d-%H-%M-%S')}"
print("Training job", job_name)

create_training_params = {
    "TrainingJobName": job_name,
    "StoppingCondition": {
        "MaxRuntimeInSeconds": 30
    },
    "AlgorithmSpecification": {
        "TrainingImage": container,
        "TrainingInputMode": "File"
    },
    "RoleArn": role,
    "OutputDataConfig": {
        "S3OutputPath": f"s3://{bucket}/{output_prefix}/single-xgboost"
    },
    "ResourceConfig": {
        "InstanceCount": 1,
        "InstanceType": "ml.m5.2xlarge",
        "VolumeSizeInGB": 5
    },
    "HyperParameters": {
        "max_depth": "5",
        "eta": "0.2",
        "gamma": "4",
        "min_child_weight": "6",
        "subsample": "0.7",
        "objective": "reg:linear",
        "num_round": "50",
        "verbosity": "2",
    },
    "InputDataConfig": [
        {
            "ChannelName": "train",
            "DataSource": {
                "S3DataSource": {
                    "S3DataType": "S3Prefix",
                    "S3Uri": f"s3://{bucket}/{prefix}",
                    "S3DataDistributionType": "FullyReplicated",
                }
            },
            "ContentType": "libsvm",
            "CompressionType": "None",
        },
    ],
}


sm.create_training_job(**create_training_params)

status = sm.describe_training_job(TrainingJobName=job_name)["TrainingJobStatus"]
print(status)
while status != "Completed" and status != "Failed":
    time.sleep(60)
    status = sm.describe_training_job(TrainingJobName=job_name)["TrainingJobStatus"]
    print(status)


# hosting_pipeline.start_pipeline_execution(name="HostingPipeline")
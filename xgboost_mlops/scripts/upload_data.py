import os, boto3, sagemaker


s3 = boto3.client('s3')
role = sagemaker.get_execution_role()
print(role)

BUCKET = os.getenv('BUCKET')
PREFIX = "xgboost-demo"
FILE_DATA = 'abalone'

s3.download_file(
    "sagemaker-sample-files",
    "datasets/tabular/uci_abalone/abalone.libsvm",
    FILE_DATA
)

sagemaker.Session().upload_data(FILE_DATA, bucket=BUCKET, key_prefix = f"{PREFIX}/data")
print("data uploaded")
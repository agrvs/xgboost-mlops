from sagemaker.session import production_variant
from sagemaker import session, get_execution_role
from datetime import datetime
import boto3, os

# role = get_execution_role()
role = os.getenv('ROLE')
print(f"bucket: {bucket}")

model_variant = production_variant(
    model_name="TestModel4",
    instance_type="ml.c5.4xlarge",
    initial_instance_count=1,
    variant_name="Variant1",
    initial_weight=1,
)

endpoint_name = f"DEMO-xgb-churn-pred-{datetime.now():%Y-%m-%d-%H-%M-%S}"
print(f"EndpointName: {endpoint_name}")

sm_session = session.Session(boto3.Session(profile_name='demo'))
sm_session.endpoint_from_production_variants(
    name=endpoint_name, production_variants=[model_variant]
)
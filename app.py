#!/usr/bin/env python3
import os
from aws_cdk import core as cdk
from xgboost_mlops.pipelines import TrainingPipelineStack, HostingPipelineStack


app = cdk.App()
TrainingPipelineStack(app, "TrainingPipelineStack")
HostingPipelineStack(app, "HostingPipelineStack")

app.synth()

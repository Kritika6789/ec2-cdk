import aws_cdk as cdk
import os
from ec2_cdk.ec2_cdk_stack import Ec2CdkStack

app = cdk.App()
Ec2CdkStack(app, "Ec2CdkStack",env=cdk.Environment(
        account="459685751152",
        region="ap-south-1"
    ) ) # temporary token from GitHub)
app.synth()


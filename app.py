import aws_cdk as cdk
import os
from ec2_cdk.ec2_cdk_stack import Ec2CdkStack

app = cdk.App()
account = os.environ.get("CDK_DEFAULT_ACCOUNT")
region = os.environ.get("CDK_DEFAULT_REGION")
Ec2CdkStack(app, "Ec2CdkStack",env=cdk.Environment(
        account=account,
        region=region
    ) )
app.synth()


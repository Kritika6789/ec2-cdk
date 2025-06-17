import aws_cdk as cdk
import os
from resources.ec2_cdk_stack import Ec2CdkStack
from resources.s3_cdk_stack import S3CdkStack
app = cdk.App()
account = os.environ.get("CDK_DEFAULT_ACCOUNT")
region = os.environ.get("CDK_DEFAULT_REGION")
Ec2CdkStack(app, "Ec2CdkStack",env=cdk.Environment(
        account=account,
        region=region
    ) )
S3CdkStack(app, "S3CdkStack")
app.synth()


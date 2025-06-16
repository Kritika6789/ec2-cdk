import aws_cdk as cdk
from ec2_cdk.ec2_cdk_stack import Ec2CdkStack

app = cdk.App()
Ec2CdkStack(app, "Ec2CdkStack")
app.synth()

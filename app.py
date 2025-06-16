import aws_cdk as cdk
from ec2_cdk.ec2_cdk_stack import Ec2CdkStack

app = cdk.App()
Ec2CdkStack(app, "Ec2CdkStack",github_repo="https://github.com/Kritika6789/ec2-cdk",  # e.g., "myusername/myrepo"
    github_token="BAP5FXHCDKHWLFCJV4LQMNDIJ7ZDG" ) # temporary token from GitHub)
app.synth()

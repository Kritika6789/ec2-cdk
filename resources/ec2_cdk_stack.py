from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam
)
from constructs import Construct

class Ec2CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        vpc = ec2.Vpc.from_lookup(self, "DefaultVPC", is_default=True)

        # Security Group
        sg = ec2.SecurityGroup(
            self, "GithubRunnerSG",
            vpc=vpc,
            description="Allow SSH and outbound",
            allow_all_outbound=True
        )
        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "Allow SSH")

        # IAM Role for EC2
        role = iam.Role(
            self, "GithubRunnerRole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore")
            ]
        )

        # UserData for installing GitHub Runner
    
        # EC2 Instance
        instance = ec2.Instance(
            self, "GithubRunnerInstance",
            instance_type=ec2.InstanceType("t3.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux2(),
            vpc=vpc,
            security_group=sg,
            role=role
        )


       
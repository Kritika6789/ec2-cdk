from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam
    # aws_sqs as sqs,
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
        user_data = ec2.UserData.for_linux()
        user_data.add_commands(
            "cd /opt",
            "mkdir actions-runner && cd actions-runner",
            "curl -o actions-runner-linux-x64-2.325.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.325.0/actions-runner-linux-x64-2.325.0.tar.gz",
            "tar xzf ./actions-runner-linux-x64-2.325.0.tar.gz",
            "sudo chown -R ec2-user:ec2-user /opt/actions-runner",
            "cd /opt/actions-runner",
            "chmod +x config.sh",
            # Replace below with your actual runner registration token
            "./config.sh --url https://github.com/Kritika6789/ec2-cdk --token BAP5FXCQNDA3EFJ3HZBE45DIKALWW --name ec2-instance-12 --labels ec2-instance-12 --unattended",
            "./run.sh"
        )

        # EC2 Instance
        instance = ec2.Instance(
            self, "GithubRunnerInstance",
            instance_type=ec2.InstanceType("t3.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux2(),
            vpc=vpc,
            security_group=sg,
            role=role,
            user_data=user_data
        )


       
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam
)
from constructs import Construct

class Ec2CdkStack(Stack):

      def __init__(self, scope: Construct, construct_id: str, github_repo: str, github_token: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # You can also create a new VPC if needed
        vpc = ec2.Vpc(self, "RunnerVpc", max_azs=2)

        # Security group for SSH and internet
        sg = ec2.SecurityGroup(self, "RunnerSG", vpc=vpc, allow_all_outbound=True)
        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "Allow SSH")

        # IAM role for EC2 (optional)
        role = iam.Role(self, "RunnerRole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com")
        )
        role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore")
        )

        # GitHub runner install script
        user_data = ec2.UserData.for_linux()

        user_data.add_commands(
            "mkdir actions-runner && cd actions-runner",
            "curl -o actions-runner-linux-x64-2.325.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.325.0/actions-runner-linux-x64-2.325.0.tar.gz",
            "tar xzf ./actions-runner-linux-x64-2.325.0.tar.gz",
            f"./config.sh --url https://github.com/{github_repo} --token {github_token}  --name python-cdk-2 --labels ec2-instance --unattended --replace",
            "./run.sh &"
        )

        # EC2 instance
        instance = ec2.Instance(self, "GitHubRunnerInstance",
            instance_type=ec2.InstanceType("t3.medium"),
            machine_image=ec2.MachineImage.latest_amazon_linux2(),
            vpc=vpc,
            security_group=sg,
            role=role,
            user_data=user_data
        )
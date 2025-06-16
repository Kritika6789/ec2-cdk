from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2
    # aws_sqs as sqs,
)
from constructs import Construct

class Ec2CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        vpc = ec2.Vpc(self, "MyVpc",
            max_azs=2,
            cidr="10.0.0.0/16",
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="public-subnet",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                )
            ]
        )

        # Create Security Group
        sg = ec2.SecurityGroup(self, "MySG",
            vpc=vpc,
            allow_all_outbound=True
        )

        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "Allow SSH access")
        user_data = ec2.UserData.for_linux()
        user_data.add_commands(
            "mkdir actions-runner && cd actions-runner",
            "curl -o actions-runner-linux-x64-2.325.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.325.0/actions-runner-linux-x64-2.325.0.tar.gz",
            "tar xzf ./actions-runner-linux-x64-2.325.0.tar.gz",
            f"./config.sh --url https://github.com/Kritika6789/ec2-cdk --token BAP5FXHDWFRIY4HKOOPIHODIKAA3Y --name ec2-instance --label ec2-instance  --unattended --replace",
            "./run.sh &"
        )
        # Create EC2 Instance
        instance = ec2.Instance(self, "MyInstance",
            instance_type=ec2.InstanceType("t3.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux2023(),
            vpc=vpc,
            security_group=sg,
            key_name="key-1.pem",
            user_data=user_data
 # Replace with your EC2 keypair
        )
        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "Ec2CdkQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )

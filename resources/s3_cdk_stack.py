from aws_cdk import (
    # Duration,
    Stack,
    aws_s3 as s3,
    RemovalPolicy
    # aws_sqs as sqs,
)
from constructs import construct

class S3CdkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        s3.Bucket(self, "MyBucket",
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )


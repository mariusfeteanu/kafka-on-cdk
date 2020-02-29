from aws_cdk import core
from aws_cdk import aws_ec2


class NetworkStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.vpc = aws_ec2.Vpc(self, 'vpc-msk')

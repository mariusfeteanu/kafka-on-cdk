from aws_cdk import core
from aws_cdk import aws_ecs
from aws_cdk import aws_ec2
from aws_cdk import aws_ecr
from aws_cdk import aws_ecr_assets

class E2ETestStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc: aws_ec2.IVpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        e2e_cluster = aws_ecs.Cluster(self, 'e2e-cluster',
            vpc=vpc,
            cluster_name='e2e-cluster')

        e2e_image = aws_ecr_assets.DockerImageAsset(self, 'e2e-image',
            directory='test/e2e')

        e2e_task = aws_ecs.FargateTaskDefinition(self, 'e2e-task',
            family='e2e-task')

        e2e_task.add_container('e2e-test-kafka',
            image=aws_ecs.ContainerImage.from_docker_image_asset(e2e_image),
            logging=aws_ecs.AwsLogDriver(stream_prefix='e2e'))
        
        e2e_security_group = aws_ec2.SecurityGroup(self, 'e2e', vpc=vpc)
        self.e2e_security_group = e2e_security_group  # expose it to give it access to kafka

        core.CfnOutput(self,"subnets", 
            value=','.join([subnet.subnet_id for subnet in vpc.private_subnets]))

        core.CfnOutput(self, "securitygroup", 
            value=e2e_security_group.security_group_id)

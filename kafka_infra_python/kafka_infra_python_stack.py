from aws_cdk import core
from aws_cdk import aws_ec2
from aws_cdk import aws_msk


DEFAULT_KAFKA_PORT = 9094


class KafkaInfraPythonStack(core.Stack):

    def __init__(
            self,
            scope: core.Construct,
            id: str,
            e2e_security_group: aws_ec2.SecurityGroup,
            vpc: aws_ec2.Vpc,
            **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        cluster_sec_group = aws_ec2.SecurityGroup(self, 'msk-cluster-sec-group',
            vpc=vpc)
        cluster_sec_group.add_ingress_rule(
            peer=e2e_security_group,
            connection=aws_ec2.Port(
                string_representation='kafka',
                protocol=aws_ec2.Protocol.TCP,
                from_port=DEFAULT_KAFKA_PORT,
                to_port=DEFAULT_KAFKA_PORT
            ))

        cluster = aws_msk.CfnCluster(self,'msk-cluster',
            cluster_name='cdk-test',
            number_of_broker_nodes=len(vpc.private_subnets),  # this is the minimum number needed
            kafka_version='2.3.1',
            broker_node_group_info=aws_msk.CfnCluster.BrokerNodeGroupInfoProperty(
                instance_type="kafka.m5.large",
                client_subnets=[
                    subnet.subnet_id
                    for subnet
                    in vpc.private_subnets],
                security_groups=[cluster_sec_group.security_group_id]
            )
        )

        core.CfnOutput(self, "arn",
            value=cluster.ref)

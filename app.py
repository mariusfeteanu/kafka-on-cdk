#!/usr/bin/env python3

from aws_cdk import core

from kafka_infra_python.kafka_infra_python_stack import KafkaInfraPythonStack
from kafka_infra_python.e2e_test_stack import E2ETestStack
from kafka_infra_python.network_stack import NetworkStack


app = core.App()

network = NetworkStack(app, "kafka-infra-python-network")

e2e = E2ETestStack(app, "kafka-infra-python-e2e-test",
        vpc=network.vpc)
e2e.add_dependency(network)

kafka = KafkaInfraPythonStack(app, "kafka-infra-python",
        vpc=network.vpc,
        e2e_security_group=e2e.e2e_security_group)
kafka.add_dependency(e2e)

app.synth()

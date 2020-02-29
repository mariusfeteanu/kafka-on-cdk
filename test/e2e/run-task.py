import time

import boto3


cf = boto3.client('cloudformation')
msk = boto3.client('kafka')
ecs = boto3.client('ecs')


def get_output(stack_name, output_name):
    resp = cf.describe_stacks(StackName=stack_name)
    assert len(resp['Stacks']) == 1
    outputs = {
        output['OutputKey']: output['OutputValue']
        for output
        in resp['Stacks'][0]['Outputs']}
    return outputs[output_name]


e2e_stack_name = 'kafka-infra-python-e2e-test'
e2e_subnets = get_output(e2e_stack_name, 'subnets').split(',')
e2e_security_group = get_output(e2e_stack_name, 'securitygroup')

print(f'{e2e_subnets=}')
print(f'{e2e_security_group=}')

msk_stack_name = 'kafka-infra-python'
msk_cluster_arn = get_output(msk_stack_name, 'arn')
msk_bootstrap_brokers = msk.get_bootstrap_brokers(ClusterArn=msk_cluster_arn)['BootstrapBrokerStringTls']

print(f'{msk_cluster_arn=}')
print(f'{msk_bootstrap_brokers=}')


e2e_cluster = 'e2e-cluster'
e2e_task_definition = 'e2e-task'

task_run_resp = ecs.run_task(
    cluster=e2e_cluster,
    taskDefinition=e2e_task_definition,
    launchType='FARGATE',
    networkConfiguration={
        'awsvpcConfiguration': {
            'subnets': e2e_subnets,
            'securityGroups': [e2e_security_group],
            'assignPublicIp': 'DISABLED'
        }
    },
    overrides={'containerOverrides':[{
        'name': 'e2e-test-kafka',
        'environment':[
            {'name': 'KAFKA_BROKERS', 'value': msk_bootstrap_brokers}
        ]
    }]}
)

assert len(task_run_resp['tasks']) == 1
assert len(task_run_resp['tasks'][0]['containers']) == 1
task_arn = task_run_resp['tasks'][0]['containers'][0]['taskArn']

print(f'{task_run_resp=}')


stop_code = None
exit_code = 1  # assume failure until we get a better response
max_retries = 100

while not stop_code and max_retries:
    describe_resp = ecs.describe_tasks(
        cluster=e2e_cluster,
        tasks=[task_arn])
    assert len(describe_resp['tasks']) == 1
    task_state = describe_resp['tasks'][0]
    if 'stopCode' in task_state:
        stop_code = task_state['stopCode']
        if stop_code == 'EssentialContainerExited':
            assert len(task_state['containers']) == 1
            exit_code = task_state['containers'][0]['exitCode']
        break
    
    max_retries -= 1
    time.sleep(5)

print(f'{task_state=}')
exit(exit_code)  # exit with the same code as the container, or 1 if unexpected result

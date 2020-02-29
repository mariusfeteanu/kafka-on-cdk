![Deploy to AWS and Test](https://github.com/mariusfeteanu/kafka-infra-python/workflows/Deploy%20to%20AWS%20and%20Test/badge.svg)

Deploys a MSK cluster using CDK. Includes a github actions pipeline to deploy it. There are also tests using ECS to validate that the Kafka cluster works.

### Pre-requisites
- python 3.8+
- nodejs v13.5.0+
- aws account credentials with enough privileges to deploy required services (see list at the end **TODO: create services list**)

### Quick start
**warning: this will deploy a real kafka cluster into your infra, costing at least 15 USD/day**

- fork the repo
- set `aws_access_key_id` and `aws_secret_access_key` in the repo secrets
- trigger the github action
- get some tea, this will take 20 minutes on the first run

Go here for the full explanation: [blog.sogdian.co.uk](https://blog.sogdian.co.uk/posts/kafka-cluster-using-aws-cdk.html)


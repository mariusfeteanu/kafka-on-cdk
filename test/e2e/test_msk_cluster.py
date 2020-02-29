import os

from kafka import KafkaProducer, KafkaAdminClient
from kafka.admin.new_topic import NewTopic
from kafka.errors import TopicAlreadyExistsError

assert 'KAFKA_BROKERS' in os.environ
KAFKA_BROKERS = os.environ['KAFKA_BROKERS'].split(',')

TOPIC_NAME = "test-topic"

def test_connectivity():
    admin = KafkaAdminClient(
        bootstrap_servers=KAFKA_BROKERS,
        security_protocol='SSL')
    try:
        admin.create_topics([
            NewTopic(TOPIC_NAME, 3, 2)
        ])
    except TopicAlreadyExistsError:
        print(f"Topic '{TOPIC_NAME}' already exists.")


    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKERS,
        security_protocol='SSL')
    producer.send(
        topic=TOPIC_NAME,
        value=b'yes')

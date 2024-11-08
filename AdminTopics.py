
from kafka import KafkaAdminClient, KafkaProducer, KafkaConsumer
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError


# Kafka broker addresses
KAFKA_BROKERS = ["host.docker.internal:9092", "host.docker.internal:9093", "host.docker.internal:9094"]

# Topic name
TOPIC_NAME = "Weather-topic"


# Function to check if the topic exists
def topic_exists(admin_client, topic_name):
    topic_metadata = admin_client.list_topics()
    return topic_name in topic_metadata

# Function to create a Kafka topic if it doesn't exist
def create_topic():
    admin_client = KafkaAdminClient(bootstrap_servers=KAFKA_BROKERS)
    if topic_exists(admin_client, TOPIC_NAME):
        print(f"Topic '{TOPIC_NAME}' already exists.")
    else:
        topic = NewTopic(name=TOPIC_NAME, num_partitions=3, replication_factor=2)
        try:
            admin_client.create_topics([topic])
            print(f"Topic '{TOPIC_NAME}' created successfully.")
        except TopicAlreadyExistsError:
            print(f"Topic '{TOPIC_NAME}' already exists.")
    admin_client.close()




create_topic()
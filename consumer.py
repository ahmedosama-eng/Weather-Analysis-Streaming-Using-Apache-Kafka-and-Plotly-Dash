from kafka import KafkaConsumer
import json
from AdminTopics import KAFKA_BROKERS
from AdminTopics import TOPIC_NAME


consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=KAFKA_BROKERS,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda v: json.loads(v.decode("utf-8"))
    )


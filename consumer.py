import json
from kafka import KafkaConsumer, KafkaProducer
import pandas as pd

kafka_server = ["192.168.0.102"]

topic = "weathertopic"

consumer = KafkaConsumer(
    bootstrap_servers=kafka_server,
    value_deserializer=json.loads,
    auto_offset_reset="latest",
)

consumer.subscribe(topic)

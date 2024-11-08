
from kafka import KafkaProducer
import json
import time
from AdminTopics import KAFKA_BROKERS
from AdminTopics import TOPIC_NAME

import pandas as pd 


data=pd.read_csv('data\weatherHistory.csv')
data['Formatted Date'] = data['Formatted Date'].str.slice(start=0,stop=16)
chunk_size=5
chunks = [data.iloc[i:i + chunk_size] for i in range(0, len(data),chunk_size)]



producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

def produce_messages():
    current_index=0
    while current_index < len(chunks):
        batch = chunks[current_index]
        data = {
            "chanks" :batch
        }
        current_index += 1
        producer.send(TOPIC_NAME, batch.to_dict(orient='list'))
        producer.flush()
        time.sleep(2)





produce_messages()
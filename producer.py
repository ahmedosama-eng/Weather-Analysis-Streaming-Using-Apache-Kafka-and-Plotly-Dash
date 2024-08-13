import json
from datetime import datetime
from time import sleep
from random import choice
from kafka import KafkaProducer
import pandas as pd 

data=pd.read_csv('data\weatherHistory.csv')
data['Formatted Date'] = data['Formatted Date'].str.slice(start=0,stop=16)
chunk_size=5
chunks = [data.iloc[i:i + chunk_size] for i in range(0, len(data),chunk_size)]

kafka_server = ["192.168.0.102"]

topic = "weathertopic"

producer = KafkaProducer(
    bootstrap_servers=kafka_server,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

current_index=0
while current_index < len(chunks):
    batch = chunks[current_index]
    data = {
        "chanks" :batch
    }
    current_index += 1
    producer.send(topic, batch.to_dict(orient='list'))
    producer.flush()
    sleep(2)
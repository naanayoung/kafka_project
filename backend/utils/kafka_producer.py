from kafka import KafkaProducer
import json

producer = KafkaProducer(
        bootstrap_servers=['localhost:29092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_event_message(data: dict):
    producer.send('event-topic', value=data)
    producer.flush()

from django.core.management.base import BaseCommand
from kafka import KafkaConsumer
import json
from events.models import ConsumedEvent

class Command(BaseCommand):
    help = 'Kafka에서 메시지를 소비하고 DB에 저장합니다.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('✅ Kafka Consumer 시작...'))

        consumer = KafkaConsumer(
            'event-topic',
            bootstrap_servers=['localhost:29092'],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='event-consumer-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

        for message in consumer:
            data = message.value
            self.stdout.write(f"[메시지 수신] {data}")

            ConsumedEvent.objects.create(
                event_id=data.get('event_id'),
                title=data.get('title'),
                status=data.get('status', 'unknown')
            )


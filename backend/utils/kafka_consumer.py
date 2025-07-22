#장고 환경 로딩
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

# Kafka 관련
from kafka import KafkaConsumer
import json
import random
import string

# 쿠폰 모델 가져오기
from coupons.models import Coupon
from users.models import User
from events.models import Event


# Kafka Consumer 설정
consumer = KafkaConsumer(
        'coupon-topic',
        bootstrap_servers=['3.37.248.119:29092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='coupon-consumer-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Kafka Consumer 시작됨. 메시지 대기중...\n")

# 메시지 수신 루프
for message in consumer:
    data = message.value
    print(f"[메시지 수신] {data}")

    try:
        event_id = data.get('event_id')
        user_id = data.get('user_id')

        if not (event_id):
            print("이벤트 ID가 없습니다.")
            continue
        
        #if not (user_id):
        #    print("유저 ID가 없습니다.")
        #    continue

        #if not (event_id and user_id):
        #    print("이벤트 ID 또는 유저 ID가 없습니다.")
        #    continue

        # 쿠폰 코드 랜덤 생성
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

        # 객체 가져오기
        event = Event.objects.get(id=event_id)
        user = User.objects.get(id=user_id)

        print(f"랜덤 코드 생성 성공 : {code}")

        # 쿠폰 저장
        Coupon.objects.create(
            code=code,
            user=user,
            event=event
        )

        print(f"✅ 쿠폰 발급 성공: {code}")

    except Exception as e:
        print(f"❌ 쿠폰 발급 실패: {str(e)}")

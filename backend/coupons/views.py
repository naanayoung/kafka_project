from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Coupon
from .serializers import CouponSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from kafka import KafkaProducer
import json


class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    #permission_classes = [] # 로그인 안해도 (개발용)
    permission_classes = [permissions.IsAuthenticated]  # 로그인한 사용자만 쿠폰 발급할 수 있도록

# EventDetail에서 랜덤 쿠폰 발급할 때
class IssueCouponView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # 인증된 사용자만

    def post(self, request, *args, **kwargs):
        event_id = request.data.get("event_id")
        user_id = request.user.id if request.user and request.user.is_authenticated else None

        if not event_id:
            return Response({"error": "event_id is required"}, status=400)

        # Kafka 메시지 전송
        producer = KafkaProducer(
            bootstrap_servers='3.37.248.119:29092',  # 또는 EC2 Kafka 주소
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        producer.send('coupon-topic', {
            'event_id': event_id,
            'user_id': user_id
        })
        producer.flush()

        return Response({"message": "쿠폰 발급 요청 완료"})

# MyPage에서 발급된 쿠폰 목록 불러올 때
class UserCouponList(APIView):
    permission_classes = [permissions.IsAuthenticated] # 인증된 사용자만

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        coupons = Coupon.objects.filter(user_id=user_id)
        serializer = CouponSerializer(coupons, many=True)
        return Response(serializer.data)

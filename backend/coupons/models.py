from django.db import models
from users.models import User
from events.models import Event

class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    issued_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_expired(self):     # 쿠폰 유효기간 지났는지 확인
        return self.issued_at > self.event.end_date

    def __str__(self):
        return f"{self.code} ({'used' if self.is_used else 'unused'})"

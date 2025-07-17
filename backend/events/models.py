from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    total_coupons = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) :
        return self.title

class ConsumedEvent(models.Model):
    event_id = models.IntegerField()
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=50)
    consumed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event_id} - {self.title}"

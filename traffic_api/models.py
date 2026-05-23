
# Create your models here.

from django.db import models


class TrafficData(models.Model):

    road_name = models.CharField(max_length=100)

    vehicle_count = models.IntegerField()

    emergency_vehicle = models.BooleanField(default=False)

    signal_status = models.CharField(max_length=10, default="RED")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.road_name

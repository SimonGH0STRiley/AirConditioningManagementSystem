from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Record(models.Model):
    id = models.BigAutoField(primary_key=True)
    roomId = models.IntegerField(
        validators=[
            MinValueValidator(1)
        ]
    )
    mode = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(128),
            MinValueValidator(1)
        ]
    )
    startTime = models.DateTimeField()
    endTime = models.DateField()
    fanSpeed = models.IntegerField(
        default=2,
        validators=[
            MaxValueValidator(3),
            MinValueValidator(1)
        ]
    )
    fee = models.FloatField(
        validators=[
            MinValueValidator(0.0)
        ]
    )
# Create your models here.

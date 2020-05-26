from django.db import models

# Create your models here.
class Personnel(models.Model):
    name = models.CharField(max_length=64)
    age = models.PositiveIntegerField()
    phonenumber = models.CharField(max_length=32)

    class Meta:
        abstract = True


class ACAdministrator(Personnel):
    pass


class HotelManager(Personnel):
    pass


class FrontWaiter(Personnel):
    pass
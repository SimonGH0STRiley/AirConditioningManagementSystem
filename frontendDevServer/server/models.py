from django.db import models
from datetime import datetime,timezone


PLATFORMS = (('a', 'android'), ('i', 'ios'), ('w', 'windows'))
STATUS = (('ready'), ('pending'), ('resolved'), ('rejected'))

# Create your models here.


class room(models.Model):
    roomNumber = models.PositiveSmallIntegerField(primary_key=True,default=0)
    isActive = models.BooleanField(null=False)
    currentTemperature = models.PositiveSmallIntegerField(default=20)
    currentSpeed = models.PositiveSmallIntegerField(default=0)
    platform = models.CharField(max_length=1, choices=PLATFORMS, default='w')
    softwareVer = models.ForeignKey(
        'Software', related_name='software', on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class AC(models.Model):
    roomNumber = models.PositiveSmallIntegerField(primary_key=True,default=0)
    isACActive =  = models.BooleanField(null=False)
    targetTemperature = models.PositiveSmallIntegerField(default=20)
    targetSpeed = models.PositiveSmallIntegerField(default=0)
    requestStatus = models.CharField(max_length=7, choices=STATUS, default='ready')
    updateTime = models.DateTimeField(auto_now=True)

    @property
    def isACActive(self):
        delta = datetime.utcnow() - self.updateTime.replace(tzinfo=None)
        if delta.seconds > 5:
            return False
        else:
            return True


class Software(models.Model):
    title = models.CharField(max_length=30, null=True)
    version = models.CharField(max_length=10, null=True)
    description = models.TextField(
        max_length=500, help_text='Description of this version', null=True)
    platform = models.CharField(max_length=1, choices=PLATFORMS, default='a')
    filePath = models.FileField(upload_to='tmp/')
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s, %s, %s' % (self.title, self.platform, self.version)


'''
used for websocket p2p communication
'''
#该表使用于websocket索引channel进行一对一发信使用
class IPChannel(models.Model):
    ip = models.GenericIPAddressField()
    port = models.IntegerField()
    channelName = models.CharField(max_length=50)

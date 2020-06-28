from channels.db import database_sync_to_async
from server.models import IPChannel, Device, DeviceStatus

@database_sync_to_async
def saveIPChannelObj(_ip, _port, _channelName):
    results = IPChannel.objects.filter(ip=_ip, port=_port)
    if results.exists():
        obj = results[0]
        obj.port = _port
        obj.channelName = _channelName
        obj.save()
    else:
        IPChannel.objects.create(ip=_ip, port=_port, channelName=_channelName)


@database_sync_to_async
def deleteIPChannelObj(_ip, _port):
    IPChannel.objects.filter(ip=_ip, port=_port).delete()


@database_sync_to_async
def getChannelName(_ip):
    results = IPChannel.objects.filter(ip=_ip)
    if results.exists():
        obj = results[0]
        return obj.channelName
    else:
        return ""


@database_sync_to_async
def getDeviceIP(dID):
    results = Device.objects.filter(deviceID=dID)
    if results.exists():
        obj = results[0]
        return obj.ip
    return ""


@database_sync_to_async
def updateDeviceStatus(deviceObj):
    results = DeviceStatus.objects.filter(deviceID=deviceObj['deviceID'])
    if results.exists():
        obj = results[0]
        obj.position = deviceObj['position']
        obj.rotation = deviceObj['rotation']
        obj.power = deviceObj['power']
        obj.currentScene = deviceObj['currentScene']
        obj.isPlaying = deviceObj['isPlaying']
        obj.isCharging = deviceObj['isCharging']
        obj.save()
    else:
        DeviceStatus.objects.create(deviceID=deviceObj['deviceID'], position=deviceObj['position'], rotation=deviceObj['rotation'],
                                    power=deviceObj['power'], currentScene=deviceObj['currentScene'], isPlaying=deviceObj['isPlaying'],isCharging = deviceObj['isCharging'])


from rest_framework import serializers
from .models import Device, Software,DeviceStatus,Tracker


class RoomSerializer(serializers.ModelSerializer):

    # software = serializers.CharField(
    #   source='softwareVer.version', read_only=True)

    softwareInfo = serializers.SerializerMethodField()
    # 方法写法：get_ + 字段

    def get_softwareInfo(self, obj):
        # obj指这个model的对象
        sf = obj.softwareVer

        return {
            'title':sf.title,
            'version':sf.version,
            'path':self.context['request'].build_absolute_uri(sf.filePath.url)
        }

    #software = SoftwareSerializer(many = False,read_only = True)
    class Meta:
        model = room
        fields = ['roomNumber', 'isActive', 'currentTemperature',
                  'currentSpeed', 'platform', 'softwareInfo']


class RoomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = room
        fields = ['roomNumber', 'isActive', 'currentTemperature', 'currentSpeed', 'platform']


class SoftwareSerializer(serializers.ModelSerializer):

    class Meta:
        model = Software
        fields = '__all__'

class ACSerializer(serializers.ModelSerializer):
    class Meta:
        model = AC
        fields = ['roomNumber', 'isACActive', 'targetTemperature', 'targetSpeed', 'requestStatus']

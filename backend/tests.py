from django.test import TestCase
from django.utils import timezone
from .models import Room, TemperatureSensor
import datetime


# Create your tests here.
class TemperatureSensorTests(TestCase):
    def test_update_current_temp(self):
        current_time = timezone.now()
        room = Room(
            room_id='房间一', room_state=1, temp_mode=1, blow_mode=1,
            current_temp=32, target_temp=27, fee_rate=1, fee=0, duration=0
        )
        room.save()
        temp_sensor = TemperatureSensor(
            room_id='房间一', init_temp = 32, current_temp = 32, 
            last_update = current_time
        )
        temp_sensor.save()

        one_minute_later = current_time + datetime.timedelta(minutes=1)
        temp_sensor.update_current_temp(current_time=one_minute_later)
        self.assertIs(-1e-6 <= temp_sensor.current_temp - (32 - 0.5) <= 1e-6, True)
        
        room.room_state = 0
        room.save()
        two_minute_later = current_time + datetime.timedelta(minutes=2)
        temp_sensor.update_current_temp(current_time=two_minute_later)
        self.assertIs(-1e-6 <= temp_sensor.current_temp - 32 <= 1e-6, True)




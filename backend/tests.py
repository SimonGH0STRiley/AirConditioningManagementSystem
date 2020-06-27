from django.test import TestCase
from django.utils import timezone
from .models import Room, TemperatureSensor, Guest
import datetime


# Create your tests here.
class TemperatureSensorTests(TestCase):
    def test_update_current_temp(self):
        current_time = timezone.now()
        room = Room(
            room_id='房间一', room_state=0, temp_mode=1, blow_mode=1,
            current_temp=32, target_temp=27, fee_rate=1, fee=0, duration=0
        )
        room.save()
        temp_sensor = TemperatureSensor(
            room_id='房间一', init_temp = 32, current_temp = 32, 
            last_update = current_time
        )
        temp_sensor.save()
        guest = Guest(room_id='房间一', date_in=datetime.date.today(), date_out=datetime.date.today())
        guest.save()

        guest.requestOn()
        room = Room.objects.get(pk='房间一')
        self.assertIs(room.room_state == 1, True)

        one_minute_later = current_time + datetime.timedelta(minutes=1)
        temp_sensor.update_current_temp(current_time=one_minute_later)
        room = Room.objects.get(pk='房间一')
        self.assertIs(-1e-6 <= temp_sensor.current_temp - (32 - 0.5) <= 1e-6, True)
        
        guest.changeFanSpeed(2)
        two_minute_later = current_time + datetime.timedelta(minutes=2)
        temp_sensor.update_current_temp(current_time=two_minute_later)
        room = Room.objects.get(pk='房间一')
        self.assertIs(-1e-6 <= temp_sensor.current_temp - (32 - 0.5 - 0.6) <= 1e-6, True)

        guest.requestOff()
        room = Room.objects.get(pk='房间一')
        self.assertIs(room.room_state == 0, True)
        three_minute_later = current_time + datetime.timedelta(minutes=3)
        temp_sensor.update_current_temp(current_time=three_minute_later)
        room = Room.objects.get(pk='房间一')
        self.assertIs(-1e-6 <= temp_sensor.current_temp - (32 - 0.6) <= 1e-6, True)




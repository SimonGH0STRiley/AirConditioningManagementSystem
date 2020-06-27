from django.test import TestCase
from django.utils import timezone
from .models import Room, TemperatureSensor, Tenant, CentralAirConditioner, ACAdministrator, requestQueue
import datetime
import time


# Create your tests here.
class ScheduleTests(TestCase):
    def test_schedule_priority(self):
        admin = ACAdministrator()
        admin.startup()
        admin.poweron()
        # admin.setpara()

        central = CentralAirConditioner.objects.all()[0]
        self.assertEqual(central.temp_mode, 1)

        for i in range(4):
            current_time = timezone.now()
            room = Room(
                room_id=str(i), room_state=0, temp_mode=1, blow_mode=1 if i != 3 else 2,
                current_temp=32, target_temp=27, fee=0, duration=0
            )
            room.save()
            temp_sensor = TemperatureSensor(
                room_id=str(i), init_temp = 32.0, current_temp = 32.0, 
                last_update = current_time
            )
            temp_sensor.save()
            guest = Tenant(name=str(i), room_id=str(i), date_in=datetime.date.today(), date_out=datetime.date.today())
            guest.save()

            guest.requestOn()

        self.assertEqual(requestQueue.objects.all().filter(room_state=2).count(), 4)
        central.schedule()
        rooms = Room.objects.all()
        self.assertEqual(requestQueue.objects.all().filter(room_state=1).count(), 3)
        self.assertEqual(rooms.filter(room_id=3)[0].blow_mode, 2)
        self.assertEqual(rooms.filter(blow_mode=1).count(), 3)
        self.assertEqual(rooms.filter(room_id=3)[0].room_state, 1)


class TemperatureSensorTests(TestCase):
    def test_update_current_temp(self):
        admin = ACAdministrator()
        admin.startup()
        admin.poweron()
        # admin.setpara()

        central = CentralAirConditioner.objects.all()[0]
        self.assertEqual(central.temp_mode, 1)

        current_time = timezone.now()
        room = Room(
            room_id='1', room_state=0, temp_mode=1, blow_mode=1,
            current_temp=32, target_temp=27, fee=0, duration=0
        )
        room.save()
        temp_sensor = TemperatureSensor(
            room_id='1', init_temp = 32.0, current_temp = 32.0, 
            last_update = current_time
        )
        temp_sensor.save()
        guest = Tenant(room_id='1', date_in=datetime.date.today(), date_out=datetime.date.today())
        guest.save()

        guest.requestOn()
        room = Room.objects.get(pk='1')
        self.assertIs(room.room_state == 2, True)
        room.room_state = 1
        room.save()

        for i in range(61):
            central.schedule()
            room = Room.objects.get(pk='1')
            temp_sensor.update_current_temp(current_time + datetime.timedelta(seconds=i))
            
        room = Room.objects.get(pk='1')   
        self.assertAlmostEqual(temp_sensor.current_temp, 32 - 0.5)     
        
        guest.requestOff()
        room = Room.objects.get(pk='1')
        self.assertIs(room.room_state == 0, True)

        '''
        guest.changeFanSpeed(2)
        two_minute_later = current_time + datetime.timedelta(minutes=2)
        temp_sensor.update_current_temp(current_time=two_minute_later)
        room = Room.objects.get(pk='1')
        self.assertIs(-1e-6 <= temp_sensor.current_temp - (32 - 0.5 - 0.6) <= 1e-6, True)

        guest.requestOff()
        room = Room.objects.get(pk='1')
        self.assertIs(room.room_state == 0, True)
        three_minute_later = current_time + datetime.timedelta(minutes=3)
        temp_sensor.update_current_temp(current_time=three_minute_later)
        room = Room.objects.get(pk='1')
        self.assertIs(-1e-6 <= temp_sensor.current_temp - (32 - 0.6) <= 1e-6, True)'''
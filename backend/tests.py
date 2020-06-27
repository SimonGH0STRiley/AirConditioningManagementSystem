from django.test import TestCase
from django.utils import timezone
from .models import Room, TemperatureSensor, Tenant, Waiter, ServiceRecord, RequestRecord
import datetime


# Create your tests here.
# class TemperatureSensorTests(TestCase):
#     def test_update_current_temp(self):
#         current_time = timezone.now()
#         room = Room(
#             room_id='房间一', room_state=0, temp_mode=1, blow_mode=1,
#             current_temp=32, target_temp=27, fee=0, duration=0
#         )
#         room.save()
#         temp_sensor = TemperatureSensor(
#             room_id='房间一', init_temp = 32, current_temp = 32,
#             last_update = current_time
#         )
#         temp_sensor.save()
#         guest = Tenant(room_id='房间一', date_in=datetime.date.today(), date_out=datetime.date.today())
#         guest.save()
#
#         guest.requestOn()
#         room = Room.objects.get(pk='房间一')
#         self.assertIs(room.room_state == 2, True)
#         room.room_state = 1
#         room.save()
#
#         one_minute_later = current_time + datetime.timedelta(minutes=1)
#         temp_sensor.update_current_temp(current_time=one_minute_later)
#         room = Room.objects.get(pk='房间一')
#         self.assertIs(-1e-6 <= temp_sensor.current_temp - (32 - 0.5) <= 1e-6, True)
#
#         guest.changeFanSpeed(2)
#         two_minute_later = current_time + datetime.timedelta(minutes=2)
#         temp_sensor.update_current_temp(current_time=two_minute_later)
#         room = Room.objects.get(pk='房间一')
#         self.assertIs(-1e-6 <= temp_sensor.current_temp - (32 - 0.5 - 0.6) <= 1e-6, True)
#
#         guest.requestOff()
#         room = Room.objects.get(pk='房间一')
#         self.assertIs(room.room_state == 0, True)
#         three_minute_later = current_time + datetime.timedelta(minutes=3)
#         temp_sensor.update_current_temp(current_time=three_minute_later)
#         room = Room.objects.get(pk='房间一')
#         self.assertIs(-1e-6 <= temp_sensor.current_temp - (32 - 0.6) <= 1e-6, True)


class WaiterTest(TestCase):
    def test_RDR_invoice(self):
        current_time = timezone.now()
        date_in = current_time - datetime.timedelta(days=10)
        date_out = date_in + datetime.timedelta(days=5)
        request_record = RequestRecord(
            room_id='房间一', room_state=1, temp_mode=1,
            start_temp=32, target_temp=27, request_time=date_in + datetime.timedelta(minutes=1)
        )
        request_record.save()

        request_record = RequestRecord(
            room_id='房间一', room_state=2, temp_mode=1,
            start_temp=32, target_temp=27, request_time=date_in + datetime.timedelta(minutes=2)
        )
        request_record.save()

        request_record = RequestRecord(
            room_id='房间一', room_state=1, temp_mode=1,
            start_temp=32, target_temp=27, request_time=date_in + datetime.timedelta(minutes=3)
        )
        request_record.save()

        request_record = RequestRecord(
            room_id='房间一', room_state=0, temp_mode=1,
            start_temp=32, target_temp=27, request_time=date_in + datetime.timedelta(minutes=4)
        )
        request_record.save()

        request_record = RequestRecord(
            room_id='房间二', room_state=1, temp_mode=1,
            start_temp=32, target_temp=27, request_time=date_in + datetime.timedelta(minutes=1)
        )
        request_record.save()

        service_record = ServiceRecord(
            RR_id=1, blow_mode=1, start_time=date_in + datetime.timedelta(minutes=1),
            end_time=date_in + datetime.timedelta(seconds=90),
            power_comsumption=0.00833 * 60 * 30, ntemp=32 - 0.25, fee_rate=1, fee=0.00833 * 60 * 30
        )
        service_record.save()

        service_record = ServiceRecord(
            RR_id=5, blow_mode=1, start_time=date_in + datetime.timedelta(minutes=1),
            end_time=date_in + datetime.timedelta(seconds=90),
            power_comsumption=0.00833 * 60 * 30, ntemp=32 - 0.25, fee_rate=1, fee=0.00833 * 60 * 30
        )
        service_record.save()

        service_record = ServiceRecord(
            RR_id=1, blow_mode=0, start_time=date_in + datetime.timedelta(seconds=90),
            end_time=date_in + datetime.timedelta(minutes=2),
            power_comsumption=0.01666 * 60 * 30, ntemp=32 - 0.25 - 0.2, fee_rate=1, fee=0.01666 * 60 * 30
        )
        service_record.save()

        service_record = ServiceRecord(
            RR_id=3, blow_mode=1, start_time=date_in + datetime.timedelta(minutes=3),
            end_time=date_in + datetime.timedelta(minutes=4),
            power_comsumption=0.00833 * 60 * 30, ntemp=32 - 0.25 - 0.2 + 0.5, fee_rate=1, fee=0.00833 * 60 * 30
        )
        service_record.save()

        w = Waiter(name='waiter1', password='none', c_time=current_time)
        detailRecords = w.printRDR('房间一', date_in, date_out)
        invoice = w.printInvoice('房间一', date_in, date_out)
        expected_detailRecords = [
                                     dict(
                                         RR_id=1, blow_mode=0, start_time=date_in + datetime.timedelta(seconds=90),
                                         end_time=date_in + datetime.timedelta(seconds=90),
                                         power_comsumption=0.00833 * 60 * 30, ntemp=32 - 0.25, fee_rate=1,
                                         fee=0.00833 * 60 * 30
                                     ),
                                     dict(
                                         RR_id=1, blow_mode=0, start_time=date_in + datetime.timedelta(seconds=90),
                                         end_time=date_in + datetime.timedelta(minutes=2),
                                         ower_comsumption=0.01666 * 60 * 30, ntemp=32 - 0.25 - 0.2, fee_rate=1,
                                         fee=0.01666 * 60 * 30
                                     ),
                                     dict(
                                         RR_id=1, blow_mode=1, start_time=date_in + datetime.timedelta(minutes=3),
                                         end_time=date_in + datetime.timedelta(minutes=4),
                                         power_comsumption=0.00833 * 60 * 30, ntemp=32 - 0.25 - 0.2 + 0.5, fee_rate=1,
                                         fee=0.00833 * 60 * 30
                                     )
                                 ]
        self.assertQuerysetEqual(detailRecords, expected_detailRecords, map(repr, expected_detailRecords))
        self.assertDictEqual(invoice,
                             {
                                 "room_id": '房间一',
                                 "total_fee": 0.00833 * 60 * 30 * 2 + 0.01666 * 60 * 30,
                                 "date_in": date_in,
                                 "date_out": date_out
                             })

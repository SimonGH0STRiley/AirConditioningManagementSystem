from django.test import TestCase
from django.utils import timezone
from .models import Room, TemperatureSensor, Tenant, CentralAirConditioner, ACAdministrator, \
    RequestRecord, Waiter, ServiceRecord, Manager, requestQueue
import datetime
import time

'''
# Create your tests here.
class ManagerTest(TestCase):
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

    request_record = RequestRecord(
        room_id='房间二', room_state=2, temp_mode=1,
        start_temp=32, target_temp=27, request_time=date_in + datetime.timedelta(minutes=2)
    )
    request_record.save()
    service_record = ServiceRecord(
        RR_id=1, blow_mode=1, start_time=date_in + datetime.timedelta(minutes=1),
        end_time=date_in + datetime.timedelta(minutes=2), service_time=datetime.timedelta(minutes=1),
        power_comsumption=0.00833 * 60, now_temp=32 - 0.5, fee_rate=1.0, fee=0.00833 * 60
    )
    service_record.save()

    service_record = ServiceRecord(
        RR_id=5, blow_mode=1, start_time=date_in + datetime.timedelta(minutes=1),
        end_time=date_in + datetime.timedelta(minutes=2), service_time=datetime.timedelta(minutes=1),
        power_comsumption=0.00833 * 60, now_temp=32 - 0.5, fee_rate=1.0, fee=0.00833 * 60
    )
    service_record.save()

    service_record = ServiceRecord(
        RR_id=3, blow_mode=1, start_time=date_in + datetime.timedelta(minutes=3),
        end_time=date_in + datetime.timedelta(minutes=4), service_time=datetime.timedelta(minutes=1),
        power_comsumption=0.00833 * 60, now_temp=32 - 0.5 + 0.5 - 0.5, fee_rate=1.0, fee=0.00833 * 60
    )
    service_record.save()

    m = Manager(name='manager1', password='none', c_time=current_time)
    report = m.weeklyReport()



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

        request_record = RequestRecord(
            room_id='房间二', room_state=2, temp_mode=1,
            start_temp=32, target_temp=27, request_time=date_in + datetime.timedelta(minutes=2)
        )
        request_record.save()

        service_record = ServiceRecord(
            RR_id=1, blow_mode=1, start_time=date_in + datetime.timedelta(minutes=1),
            end_time=date_in + datetime.timedelta(minutes=2), service_time=datetime.timedelta(minutes=1),
            power_comsumption=0.00833 * 60, now_temp=32 - 0.5, fee_rate=1.0, fee=0.00833 * 60
        )
        service_record.save()

        service_record = ServiceRecord(
            RR_id=5, blow_mode=1, start_time=date_in + datetime.timedelta(minutes=1),
            end_time=date_in + datetime.timedelta(minutes=2), service_time=datetime.timedelta(minutes=1),
            power_comsumption=0.00833 * 60, now_temp=32-0.5, fee_rate=1.0, fee=0.00833 * 60
        )
        service_record.save()

        service_record = ServiceRecord(
            RR_id=3, blow_mode=1, start_time=date_in + datetime.timedelta(minutes=3),
            end_time=date_in + datetime.timedelta(minutes=4), service_time=datetime.timedelta(minutes=1),
            power_comsumption=0.00833 * 60, now_temp=32 - 0.5 + 0.5-0.5, fee_rate=1.0, fee=0.00833 * 60
        )
        service_record.save()

        w = Waiter(name='waiter1', password='none', c_time=current_time)
        detailRecords = w.printRDR('房间一', date_in, date_out)
        invoice = w.printInvoice('房间一', date_in, date_out)
        print(detailRecords)
        expected_detailRecords = [
            dict(
                RR_id=1, blow_mode=1, start_time=date_in + datetime.timedelta(minutes=1),
                end_time=date_in + datetime.timedelta(minutes=2), id=1, service_time=datetime.timedelta(minutes=1),
                power_comsumption=0.00833 * 60, now_temp=31.5, fee_rate=1.0, fee=0.00833 * 60
            ),
            dict(
                RR_id=3, blow_mode=1, start_time=date_in + datetime.timedelta(minutes=3),
                end_time=date_in + datetime.timedelta(minutes=4), id=3, service_time=datetime.timedelta(minutes=1),
                power_comsumption=0.00833 * 60, now_temp=32 - 0.5 + 0.5 - 0.5, fee_rate=1.0, fee=0.00833 * 60
            )
        ]
        self.assertDictEqual(detailRecords[0], expected_detailRecords[0])
        self.assertDictEqual(detailRecords[1], expected_detailRecords[1])
        self.assertDictEqual(invoice,
                             {
                                 "room_id": '房间一',
                                 "total_fee": 0.00833 * 60 * 2,
                                 "date_in": date_in,
                                 "date_out": date_out
                             })
'''
import os

class ScheduleTests(TestCase):
    def test_schedule_priority(self):
        admin = ACAdministrator()
        admin.startup()
        admin.poweron()

        central = CentralAirConditioner.objects.all()[0]
        
        current_temps = [32, 28, 30, 29, 35]
        temp_sensors = []
        for i in range(5):
            current_time = timezone.now()
            room = Room(
                room_id=str(i), room_state=0, temp_mode=1, blow_mode=1 if i != 3 else 2,
                current_temp=current_temps[i], target_temp=27, fee=0, duration=0
            )
            room.save()
            temp_sensor = TemperatureSensor(
                room_id=str(i), init_temp=32.0, current_temp=current_temps[i],
                last_update=current_time
            )
            temp_sensor.save()
            temp_sensors.append(temp_sensor)
            guest = Tenant(name=str(i), room_id=str(i), date_in=datetime.date.today(), date_out=datetime.date.today())
            guest.save()

            guest.requestOn()

        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            command = input('Admin. Your command is: ')
            if command == 'set para':
                change_item = input('You want to change: ')
                change_value = input('You want to set the value as: ')
                if change_item == 'temp_mode':
                    admin.setpara(temp_mode=int(change_value))
                if change_item == 'waiting_duration':
                    admin.setpara(waiting_duration=int(change_value))

                print('Set successfuly. Current parameters are as follows:')
                print(list(CentralAirConditioner.objects.all().values())[0])
                input('Press any key to continue')
                continue

            elif command == 'supervise all':
                try:
                    while True:
                        central.schedule()
                        os.system('cls' if os.name == 'nt' else 'clear')
                        waiting_request = requestQueue.objects.all().filter(room_state=2)
                        serving_request = requestQueue.objects.all().filter(room_state=1)
                        print('waiting rooms:\n')
                        for wr in waiting_request:
                            print('room_id =', wr.room_id, 'blow_mode =', wr.blow_mode, sep='\t')
                        print('serving rooms:\n')
                        for wr in serving_request:
                            print('room_id =', wr.room_id, 'blow_mode =', wr.blow_mode, 'service_duration =', wr.service_duration, sep='\t')
                        # print('waiting room:\n', waiting_request.values())
                        # print('serving room:\n', serving_request.values())
                        time.sleep(1)
                except KeyboardInterrupt:
                    pass
            
            elif command == 'supervise one room':
                os.system('cls' if os.name == 'nt' else 'clear')
                room_id = input('Please input the room_id: ')
                temp_sensor = temp_sensors[int(room_id)]
                try:
                    while True:
                        temp_sensor.update_current_temp()
                        temp_sensor.save()
                        central.schedule()
                        os.system('cls' if os.name == 'nt' else 'clear')
                        request = requestQueue.objects.get(room_id=room_id)
                        room = Room.objects.get(room_id=room_id)
                        print('room_id =', room_id, sep='\t')
                        print('target_temp =', room.target_temp, sep='\t')
                        print('current_temp =', room.current_temp, sep='\t')
                        if request.room_state == 2:
                            print('waiting')
                            print('blow_mode =', request.blow_mode, sep='\t')
                        else:
                            print('serving')
                            print('blow_mode =', request.blow_mode, sep='\t')
                            print('service_duration =', request.service_duration, sep='\t')
                        # print('waiting room:\n', waiting_request.values())
                        # print('serving room:\n', serving_request.values())
                        time.sleep(1)
                except KeyboardInterrupt:
                    pass

            elif command == 'exit':
                print("Good bye!")
                input()
                return
            else:
                print("Wrong command!")
                input()
                continue


'''
        self.assertEqual(requestQueue.objects.all().filter(room_state=2).count(), 4)
        central.schedule()
        rooms = Room.objects.all()
        self.assertEqual(requestQueue.objects.all().filter(room_state=1).count(), 3)
        self.assertEqual(rooms.filter(room_id=3)[0].blow_mode, 2)
        self.assertEqual(rooms.filter(blow_mode=1).count(), 3)
        self.assertEqual(rooms.filter(room_id=3)[0].room_state, 1)'''


'''
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
        self.assertIs(-1e-6 <= temp_sensor.current_temp - (32 - 0.6) <= 1e-6, True)
'''

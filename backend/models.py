from django.db import models
from django.db.models import Sum, Count
from django.utils import timezone
import time
import datetime
from django.db.models import F

# Create your models here.
# 制冷制热模式, 默认制冷
temp_mode_choice = (
    (1, '制冷模式'),
    (-1, '制热模式'),
)
# 送风模式，风速
blow_mode_choice = (
    (0, '低风'),
    (1, '中风'),
    (2, '高风'),
)
# 房间状态
room_state_choice = (
    (0, '关闭'),
    (1, '运行'),
    (2, '挂起'),
)

# 浮点误差
eps = 1e-6
# 费率：1元/度
fee_rate = 1
# 空调关机或待机，向初始温度变化，每分钟变化0.5℃，每秒变化除以60
default_temp_changing = 0.5 / 60
# 温度每秒变化速率
temp_change_speed_array = (
    (0.4 / 60, '低风温度变化'),
    (0.5 / 60, '中风温度变化'),
    (0.6 / 60, '高风温度变化'),
)
# 缺省目标温度
default_temp = 25
# 各档风速耗电量
feerate_choice = (
    (0.01666, '高风单位耗电量(度/秒)'),
    (0.00833, '中风单位耗电量(度/秒)'),  # 缺省风速
    (0.00556, '低风单位耗电量(度/秒)'),
)
# room_list
room_list = [1, 2, 3, 4, 5]


class Personel(models.Model):
    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256, default='')
    c_time = models.DateTimeField(auto_now_add=True)  # 角色创建时间，用于排序管理

    class Meta:
        ordering = ["-c_time"]  # 按创建时间降序排序, 优先显示新创建的
        abstract = True


class requestQueue(models.Model):
    room_id = models.CharField('房间号', max_length=64, primary_key=True)
    room_state = models.SmallIntegerField(choices=room_state_choice, default=2, verbose_name="房间送风状态")
    temp_mode = models.SmallIntegerField('制冷制热模式', choices=temp_mode_choice, default=1)
    blow_mode = models.SmallIntegerField('送风模式', choices=blow_mode_choice, default=1)
    # target_temp = models.IntegerField('目标温度')
    request_timestamp = models.DateTimeField('请求送风时间戳', auto_now_add=True)
    air_timestamp = models.DateTimeField('开始送风时间戳', null=True)
    service_duration = models.IntegerField('当前服务时长(秒)', default=0)


class ACAdministrator(Personel):
    def __str__(self):
        return self.name

    def poweron(self):
        central_air_conditioner = CentralAirConditioner.objects.all()[0]
        central_air_conditioner.ac_state = 'set_mode'
        central_air_conditioner.save()

    def setpara(self, temp_mode=None, cool_temp_highlimit=None, cool_temp_lowlimit=None, heat_temp_highlimit=None,
                heat_temp_lowlimit=None, \
                default_targettemp=None, feerate_h=None, feerate_m=None, feerate_l=None, max_load=None,
                waiting_duration=None):
        central_air_conditioner = CentralAirConditioner.objects.all()[0]
        if central_air_conditioner.ac_state == 'set_mode':
            if temp_mode is not None:
                central_air_conditioner.temp_mode = temp_mode
            if cool_temp_highlimit is not None:
                central_air_conditioner.cool_temp_highlimit = cool_temp_highlimit
            if cool_temp_lowlimit is not None:
                central_air_conditioner.cool_temp_lowlimit = cool_temp_lowlimit
            if heat_temp_highlimit is not None:
                central_air_conditioner.heat_temp_highlimit = heat_temp_highlimit
            if heat_temp_lowlimit is not None:
                central_air_conditioner.heat_temp_lowlimit = heat_temp_lowlimit
            if default_targettemp is not None:
                central_air_conditioner.default_temp = default_targettemp
            if feerate_h is not None:
                central_air_conditioner.feerate_H = feerate_h
            if feerate_m is not None:
                central_air_conditioner.feerate_M = feerate_m
            if feerate_l is not None:
                central_air_conditioner.feerate_L = feerate_l
            if max_load is not None:
                central_air_conditioner.max_load = max_load
            if waiting_duration is not None:
                central_air_conditioner.waiting_duration = waiting_duration
            central_air_conditioner.save()

    def startup(self):
        central_air_conditioner = CentralAirConditioner()
        central_air_conditioner.ac_state = 'ready'
        central_air_conditioner.save()

    def checkroomstate(self):
        central_air_conditioner = CentralAirConditioner.objects.all()[0]
        while central_air_conditioner.ac_state == 'ready':
            info = Room.objects.all()
            time.sleep(60)
            return info
            # 前端每分钟刷新显示房间的[models.Room.room_state, models.Room.current_temp, models.Room.target_temp,
            # (续)models.Room.blow_mode, models.Room.fee_rate, models.Room.fee, models.Room.duration]

    class Meta:
        verbose_name = "空调管理员"  # 可读性佳的名字
        verbose_name_plural = "空调管理员"  # 复数形式


class Waiter(Personel):
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "前台服务员"  # 可读性佳的名字
        verbose_name_plural = "前台服务员"  # 复数形式

    def printRDR(self, room_id, date_in, date_out):
        records = ServiceRecord.objects.filter(RR__room_id=room_id, start_time__range=(date_in, date_out)).values()
        return records

    def printInvoice(self, room_id, date_in, date_out):
        total_fee = ServiceRecord.objects.filter(RR__room_id=room_id, start_time__range=(date_in, date_out)).aggregate(
            Sum("fee")).get('fee__sum')
        invoice = {
            "room_id": room_id,
            "total_fee": total_fee,
            "date_in": date_in,
            "date_out": date_out
        }
        return invoice


class Manager(Personel):
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "酒店经理"  # 可读性佳的名字
        verbose_name_plural = "酒店经理"  # 复数形式

    def dailyReport(self, date_start, date_end):
        basic_room_info = RoomDailyReport.objects.filter(date__range=(date_start.date(), date_end.date())).\
            values('room_id', 'date', 'switch_count', 'schedule_count', 'change_temp_count', 'change_speed_count')

        for i in range((date_end - date_start).days+1):
            date = date_start+datetime.timedelta(days=i)
            day_service_items = ServiceRecord.objects.filter(start_time__date=date).values('RR__room_id').\
                annotate(Sum('service_time')).values('RR__room_id', 'service_time__sum')

            for k in day_service_items:
                for j in basic_room_info:
                    if j['date'] == date.date() and j['room_id'] == k['RR__room_id']:
                        j['service_time__sum'] = k['service_time__sum']

            day_room_fee = ServiceRecord.objects.filter(start_time__date=date).values('RR__room_id').\
                annotate(Sum('fee')).values('RR__room_id', 'fee__sum')

            for k in day_room_fee:
                for j in basic_room_info:
                    if j['date'] == date.date() and j['room_id'] == k['RR__room_id']:
                        j['fee__sum'] = k['fee__sum']

            day_detail_record = ServiceRecord.objects.filter(start_time__date=date).values('RR__room_id'). \
                annotate(detail_record_count=Count('RR__room_id')).values('RR__room_id', 'detail_record_count')

            for k in day_detail_record:
                for j in basic_room_info:
                    if j['date'] == date.date() and j['room_id'] == k['RR__room_id']:
                        j['detail_record_count'] = k['detail_record_count']

        return basic_room_info

    def weeklyReport(self, date_start, date_end):
        basic_room_info = RoomDailyReport.objects.filter(date__week__range=(date_start.week(), date_end.week())).\
            values('room_id', 'date', 'switch_count', 'schedule_count', 'change_temp_count', 'change_speed_count')

        for i in range((date_end - date_start).weeks + 1):
            date = date_start + datetime.timedelta(weeks=i)
            day_service_items = ServiceRecord.objects.filter(start_time__week=date.week()).values('RR__room_id'). \
                annotate(Sum('service_time')).values('RR__room_id', 'service_time__sum')

            for k in day_service_items:
                for j in basic_room_info:
                    if j['date'] == date.date() and j['room_id'] == k['RR__room_id']:
                        j['service_time__sum'] = k['service_time__sum']

            day_room_fee = ServiceRecord.objects.filter(start_time__week=date.week()).values('RR__room_id'). \
                annotate(Sum('fee')).values('RR__room_id', 'fee__sum')

            for k in day_room_fee:
                for j in basic_room_info:
                    if j['date'] == date.date() and j['room_id'] == k['RR__room_id']:
                        j['fee__sum'] = k['fee__sum']

            day_detail_record = ServiceRecord.objects.filter(start_time__week=date.week()).values('RR__room_id'). \
                annotate(detail_record_count=Count('RR__room_id')).values('RR__room_id', 'detail_record_count')

            for k in day_detail_record:
                for j in basic_room_info:
                    if j['date'] == date.date() and j['room_id'] == k['RR__room_id']:
                        j['detail_record_count'] = k['detail_record_count']

        return basic_room_info

    def monthlyReport(self, date_start, date_end):
        basic_room_info = RoomDailyReport.objects.filter(date__month__range=(date_start.month(), date_end.month())). \
            values('room_id', 'date', 'switch_count', 'schedule_count', 'change_temp_count', 'change_speed_count')

        for i in range((date_end - date_start).weeks + 1):
            date = date_start + datetime.timedelta(months=i)
            day_service_items = ServiceRecord.objects.filter(start_time__month=date.month()).values('RR__room_id'). \
                annotate(Sum('service_time')).values('RR__room_id', 'service_time__sum')

            for k in day_service_items:
                for j in basic_room_info:
                    if j['date'] == date.date() and j['room_id'] == k['RR__room_id']:
                        j['service_time__sum'] = k['service_time__sum']

            day_room_fee = ServiceRecord.objects.filter(start_time__month=date.month()).values('RR__room_id'). \
                annotate(Sum('fee')).values('RR__room_id', 'fee__sum')

            for k in day_room_fee:
                for j in basic_room_info:
                    if j['date'] == date.date() and j['room_id'] == k['RR__room_id']:
                        j['fee__sum'] = k['fee__sum']

            day_detail_record = ServiceRecord.objects.filter(start_time__month=date.month()).values('RR__room_id'). \
                annotate(detail_record_count=Count('RR__room_id')).values('RR__room_id', 'detail_record_count')

            for k in day_detail_record:
                for j in basic_room_info:
                    if j['date'] == date.date() and j['room_id'] == k['RR__room_id']:
                        j['detail_record_count'] = k['detail_record_count']

        return basic_room_info

    def yearlyReport(self):
        basic_room_info = RoomDailyReport.objects.filter(date__year__range=(date_start.year(), date_end.year())). \
            values('room_id', 'date', 'switch_count', 'schedule_count', 'change_temp_count', 'change_speed_count')

        for i in range((date_end - date_start).weeks + 1):
            date = date_start + datetime.timedelta(years=i)
            day_service_items = ServiceRecord.objects.filter(start_time__year=date.year()).values('RR__room_id'). \
                annotate(Sum('service_time')).values('RR__room_id', 'service_time__sum')

            for k in day_service_items:
                for j in basic_room_info:
                    if j['date'] == date.date() and j['room_id'] == k['RR__room_id']:
                        j['service_time__sum'] = k['service_time__sum']

            day_room_fee = ServiceRecord.objects.filter(start_time__year=date.year()).values('RR__room_id'). \
                annotate(Sum('fee')).values('RR__room_id', 'fee__sum')

            for k in day_room_fee:
                for j in basic_room_info:
                    if j['date'] == date.date() and j['room_id'] == k['RR__room_id']:
                        j['fee__sum'] = k['fee__sum']

            day_detail_record = ServiceRecord.objects.filter(start_time__year=date.year()).values('RR__room_id'). \
                annotate(detail_record_count=Count('RR__room_id')).values('RR__room_id', 'detail_record_count')

            for k in day_detail_record:
                for j in basic_room_info:
                    if j['date'] == date.date() and j['room_id'] == k['RR__room_id']:
                        j['detail_record_count'] = k['detail_record_count']

        return basic_room_info


class Tenant(models.Model):
    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256, default='')
    c_time = models.DateTimeField(auto_now_add=True)  # 角色创建时间，用于排序管理
    room_id = models.CharField('房间号', max_length=64, primary_key=True)
    date_in = models.DateField('入住日期', null=True)
    date_out = models.DateField('登出日期', null=True)

    class Meta:
        ordering = ["-c_time"]  # 按创建时间降序排序, 优先显示新创建的
        verbose_name = "房客"  # 可读性佳的名字
        verbose_name_plural = "房客"  # 复数形式

    def initiateTenant(self):
        pass

    def requestOn(self):
        room = Room.objects.get(pk=self.room_id)
        room.room_state = 2  # 开机后，房间空调处于待机状态，若中央空调能送风才处于工作状态
        # room.switch_count += 1
        room.save()
        room_daily_report = RoomDailyReport.objects.filter(room_id=self.room_id, date=datetime.date.today())
        if room_daily_report.count() == 0:
            room_daily_report = RoomDailyReport(room_id=self.room_id, date=datetime.date.today())
        else:
            room_daily_report = room_daily_report[0]
        room_daily_report.switch_count += 1
        room_daily_report.save()
        room.requestAir()

    def changeTargetTemp(self, target_temp):
        room = Room.objects.get(pk=self.room_id)
        room.target_temp = target_temp
        # room.change_temp_count += 1
        room.save()

        room_daily_report = RoomDailyReport.objects.filter(room_id=self.room_id, date=datetime.date.today())
        if room_daily_report.count() == 0:
            room_daily_report = RoomDailyReport(room_id=self.room_id, date=datetime.date.today())
        else:
            room_daily_report = room_daily_report[0]
        room_daily_report.change_temp_count += 1
        room_daily_report.save()

        room.cancelAir()
        room.requestAir()

    def changeFanSpeed(self, fan_speed):
        room = Room.objects.get(pk=self.room_id)
        room.blow_mode = fan_speed
        # room.change_speed_count += 1    
        room.save()
        room_daily_report = RoomDailyReport.objects.filter(room_id=self.room_id, date=datetime.date.today())
        if room_daily_report.count() == 0:
            room_daily_report = RoomDailyReport(room_id=self.room_id, date=datetime.date.today())
        else:
            room_daily_report = room_daily_report[0]
        room_daily_report.change_speed_count += 1
        room_daily_report.save()

        room.cancelAir()
        room.requestAir()

    def requestOff(self):
        room = Room.objects.get(pk=self.room_id)
        room.room_state = 0
        room.save()
        room.cancelAir()


class TemperatureSensor(models.Model):
    room_id = models.CharField(
        '房间号', max_length=64, unique=True, primary_key=True)
    init_temp = models.FloatField('初始温度')
    current_temp = models.FloatField('当前温度')
    last_update = models.DateTimeField('上次更新时间', default=timezone.now())

    def update_current_temp(self, current_time=None):
        if current_time is None:
            current_time = timezone.now()
        room = Room.objects.get(pk=self.room_id)
        # current_time =
        delta_update_time = current_time - self.last_update
        temp_change_direction = room.temp_mode
        if room.room_state != 1:
            delta_temp_change = default_temp_changing * delta_update_time.total_seconds()
            self.current_temp += temp_change_direction * delta_temp_change
            # 房间回温算法变化到室温为止
            if (temp_change_direction == 1 and self.current_temp > self.init_temp) or \
                    (temp_change_direction == -1 and self.current_temp < self.init_temp):
                self.current_temp = self.init_temp
        else:
            delta_temp_change = temp_change_speed_array[room.blow_mode][0] * \
                                delta_update_time.total_seconds()
            self.current_temp -= temp_change_direction * delta_temp_change
        room.current_temp = self.current_temp
        room.save()
        self.last_update = current_time


class RoomDailyReport(models.Model):
    room_id = models.CharField('房间号', max_length=64)
    date = models.DateField('日期', null=True)
    switch_count = models.IntegerField('开关次数', default=0)
    schedule_count = models.IntegerField('被调度次数', default=0)
    change_temp_count = models.IntegerField('调温次数', default=0)
    change_speed_count = models.IntegerField('调风次数', default=0)


class Room(models.Model):
    room_id = models.CharField(
        '房间号', max_length=64, unique=True, primary_key=True)
    room_state = models.SmallIntegerField(
        choices=room_state_choice, default=0, verbose_name="房间从控机状态")
    temp_mode = models.SmallIntegerField(
        '制冷制热模式', choices=temp_mode_choice, default=1)
    blow_mode = models.SmallIntegerField(
        '送风模式', choices=blow_mode_choice, default=1)
    current_temp = models.FloatField('当前温度')
    target_temp = models.IntegerField('目标温度', default=default_temp)
    # fee_rate = models.FloatField('费率')
    fee = models.FloatField('总费用')
    duration = models.IntegerField('服务时长(秒)')
    # send_reair = models.IntegerField('超目标温度后是否发送过请求', default=0)


    def requestAir(self):
        if requestQueue.objects.all().filter(room_id=self.room_id, )
        new_air_request = requestQueue(self.room_id, self.room_state, self.temp_mode, self.blow_mode)
        new_air_request.save()
        new_request_record = RequestRecord(  # 创建请求记录
            room_id=self.room_id, room_state=self.room_state, blow_mode=self.blow_mode,
            start_temp=self.current_temp, target_temp=self.target_temp, request_time=timezone.now()
        )
        new_request_record.save()

    def cancelAir(self):
        old_air_request = requestQueue.objects.get(pk=self.room_id)
        old_air_request.delete()

        old_request_record = RequestRecord.objects.get(room_id=self.room_id, finished=0)
        old_request_record.finished=1  # 结束请求记录
        old_request_record.save()
        ServiceRecord.objects.filter(RR=old_request_record.RR, room_id=self.room_id)\
            .update(end_time=timezone.now, power_comsumption=old_request_record.service_duration * old_request_record.blow_mode / 180.0,
            fee=old_request_record.service_duration * old_request_record.blow_mode / 180.0)


    def auto_ajust_temp(self):
        if self.room_state == 1:
            # 达到目标温度，取消送风
            if (self.temp_mode == 1 and self.current_temp <= self.target_temp + eps) or \
                    (self.temp_mode == -1 and self.current_temp >= self.target_temp - eps):
                self.cancelAir()
                # self.send_reair = 0
        elif self.room_state == 2:
            # 偏离目标温度一度，请求送风 self.send_reair == 0 and 
            if ((self.temp_mode == 1 and self.current_temp >= self.target_temp + 1 - eps) or \
                    (self.temp_mode == -1 and self.current_temp <= self.target_temp - 1 + eps)):
                self.requestAir()
                # self.send_reair = 1


class CentralAirConditioner(models.Model):
    ac_state_choice = (
        ('close', '关闭'),
        ('set_Model', '设置模式'),
        ('ready', '就绪'),
        ('none', '备用'),
    )
    ac_state = models.CharField(
        choices=ac_state_choice, max_length=64, default='close', verbose_name="中央空调状态")
    temp_mode = models.SmallIntegerField(
        '制冷制热模式', choices=temp_mode_choice, default=1)
    cool_temp_highlimit = models.IntegerField('制冷温控范围最高温', default=25)
    cool_temp_lowlimit = models.IntegerField('制冷温控范围最低温', default=18)
    heat_temp_highlimit = models.IntegerField('制热温控范围最高温', default=30)
    heat_temp_lowlimit = models.IntegerField('制热温控范围最低温', default=25)
    default_temp = models.IntegerField('缺省温度', default=25,)
    feerate_H = models.FloatField('高风费率', default=1.0 / 60)
    feerate_M = models.FloatField('中风费率', default=0.5 / 60)
    feerate_L = models.FloatField('低风费率', default=1.0 / 180)
    max_load = models.IntegerField('最大带机量', default=3)
    waiting_duration = models.IntegerField(default=120)

    # 需要每秒运行
    def billing(self):
        pass

    # 需要每秒钟运行
    def schedule(self):

        def send_air(satisfy_request):
            satisfy_room = Room.objects.get(pk=satisfy_request.room_id)  # 取得房间
            satisfy_room.room_state = 1
            satisfy_room.save()

            satisfy_request.room_state = 1  # 开始送风
            satisfy_request.air_timestamp = timezone.now()  # 送风开始时间
            satisfy_request.save()
            
            request_record = RequestRecord.objects.get(room_id=satisfy_request.room_id, finished=0)
            new_service_record = ServiceRecord(
                RR=request_record.RR, room_id=satisfy_request.room_id, blow_mode=request_record.blow_mode,
                start_time=timezone.now(), now_temp=satisfy_room.current_temp
            )
            new_service_record.save()

        def cancel_air(weaker_request):
            weaker_room = Room.objects.get(pk=weaker_request.room_id)
            weaker_room.room_state = 2
            # weaker_room.schedule_count += 1
            weaker_room.save()
            room_daily_report = RoomDailyReport.objects.filter(room_id=weaker_request.room_id, date=datetime.date.today())
            if room_daily_report.count() == 0:
                room_daily_report = RoomDailyReport(room_id=self.room_id, date=datetime.date.today())
            else:
                room_daily_report = room_daily_report[0]
            room_daily_report.schedule_count += 1
            room_daily_report.save()

            weaker_request.room_state = 2  # 停止送风
            weaker_request.request_timestamp = timezone.now()  # 重新计时
            weaker_request.save()

            old_request_record = RequestRecord.objects.get(room_id=weaker_request.room_id, finished=0)
            ServiceRecord.objects.filter(RR=old_request_record.RR, room_id=weaker_request.room_id)\
                .update(end_time=timezone.now(), power_comsumption=weaker_request.service_duration * weaker_request.blow_mode / 180.0,
                fee=weaker_request.service_duration * weaker_request.blow_mode / 180.0)

        all_rooms = Room.objects.all()
        all_requests = requestQueue.objects.all()
        current_request_cnt = len(all_requests)
        waiting_request = all_requests.filter(room_state=2)
        serving_request = all_requests.filter(room_state=1)
        current_load = len(serving_request)

        # 更新服务时间
        serving_request.update(service_duration=F('service_duration') + 1)

        # 全部送风请求都已满足，不需要调度
        if len(waiting_request) == 0:
            return

        for satisfy_request in waiting_request:
            # 尚未超过负载能力，满足送风请求
            if requestQueue.objects.all().filter(room_state=1).count() < self.max_load:
                #  与设定制冷制热模式一致
                if satisfy_request.temp_mode == self.temp_mode:
                    send_air(satisfy_request)


            else:  # 超过负载能力，需要进行调度
                current_time = timezone.now()
                serving_request = requestQueue.objects.all().filter(room_state=1)
                weaker_request = serving_request.filter(blow_mode__lt=satisfy_request.blow_mode)
                if len(weaker_request) > 0:  # 优先级调度，先满足高风速请求
                    weaker_request = weaker_request[0]  # 挑选出一个低风速请求
                    cancel_air(weaker_request)
                    send_air(satisfy_request)
                else:
                    equal_request = serving_request.filter(blow_mode=satisfy_request.blow_mode).order_by(
                        '-service_duration')
                    if len(
                            equal_request) > 0 and satisfy_request.request_timestamp <= current_time - datetime.timedelta(
                            seconds=self.waiting_duration):  # 时间片调度
                        equal_request = equal_request[0]  # 关掉服务时间最长的
                        cancel_air(equal_request)
                        send_air(satisfy_request)


class RequestRecord(models.Model):
    RR = models.BigAutoField(primary_key=True)
    room_id = models.CharField('房间号', max_length=64)
    room_state = models.SmallIntegerField("房间送风状态", choices=room_state_choice, default=2)
    temp_mode = models.SmallIntegerField('送风模式', choices=temp_mode_choice, default=2)
    start_temp = models.IntegerField('初始温度')
    blow_mode = models.IntegerField('风速')
    target_temp = models.IntegerField('目标温度')
    request_time = models.DateTimeField()
    finished = models.IntegerField('结束', default=0)


class ServiceRecord(models.Model):
    RR = models.BigIntegerField("RequestRecord")
    blow_mode = models.SmallIntegerField('送风模式', choices=blow_mode_choice, default=2)
    start_time = models.DateTimeField()
    room_id = models.CharField('房间号', max_length=64)
    end_time = models.DateTimeField(null=True)
    service_time = models.DurationField(default=timezone.timedelta)
    power_comsumption = models.FloatField('用电度数', default=0)
    now_temp = models.FloatField('当前温度')
    fee_rate = models.FloatField('费率', choices=feerate_choice, default=2)
    fee = models.FloatField(default=0.0)

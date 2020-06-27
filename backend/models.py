from django.db import models
from django.db.models import Sum
from django.utils import timezone
import time
import datetime

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
    (0.00833, '高风单位耗电量(度/秒)'),  # 缺省风速
    (0.00556, '高风单位耗电量(度/秒)'),
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


class ACAdministrator(Personel):
    def __str__(self):
        return self.name

    def poweron(self):
        CentralAirConditioner.ac_state = 'set_mode'
        CentralAirConditioner.save()

    def setpara(self, temp_mode=1, cool_temp_highlimit=25, cool_temp_lowlimit=18, heat_temp_highlimit=30, heat_temp_lowlimit=25, \
        default_targettemp=25, feerate_h=1/60, feerate_m=0.5/60, feerate_l=1/180, max_load=3, waiting_duration=120):
        if CentralAirConditioner.ac_state == 'set_mode':
            CentralAirConditioner.temp_mode = temp_mode
            CentralAirConditioner.cool_temp_highlimit = cool_temp_highlimit
            CentralAirConditioner.cool_temp_lowlimit = cool_temp_lowlimit
            CentralAirConditioner.heat_temp_highlimit = heat_temp_highlimit
            CentralAirConditioner.heat_temp_lowlimit = heat_temp_lowlimit
            CentralAirConditioner.default_temp = default_targettemp
            CentralAirConditioner.feerate_H = feerate_h
            CentralAirConditioner.feerate_M = feerate_m
            CentralAirConditioner.feerate_L = feerate_l
            CentralAirConditioner.max_load = max_load
            CentralAirConditioner.waiting_duration = waiting_duration
            CentralAirConditioner.save()

    def startup(self):
        CentralAirConditioner.ac_state = 'ready'
        CentralAirConditioner.save()

    def checkroomstate(self):
        while CentralAirConditioner.ac_state == 'ready':
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
        records = ServiceRecord.objects.filter(RR__room_id=room_id, start_time__range=(date_in, date_out))
        return records

    def printInvoice(self, room_id, date_in, date_out):
        total_fee = ServiceRecord.objects.filter(RR__room_id=room_id, start_time__range=(date_in, date_out)).aggregate(Sum("fee")).get('fee__sum')
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
        room.save()
        room.requestAir()

    def changeTargetTemp(self, target_temp):
        room = Room.objects.get(pk=self.room_id)
        room.target_temp = target_temp
        room.save()
        room.cancelAir()
        room.requestAir()

    def changeFanSpeed(self, fan_speed):
        room = Room.objects.get(pk=self.room_id)
        room.blow_mode = fan_speed
        room.save()
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
    last_update = models.TimeField('上次更新时间', default=timezone.now())

    def update_current_temp(self, current_time=timezone.now()):
        room = Room.objects.get(pk=self.room_id)
        # current_time =
        delta_update_time = current_time - self.last_update
        temp_change_direction = room.temp_mode
        if room.get_room_state_display() != '运行':
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
        self.last_update = current_time


class Room(models.Model):
    room_id = models.CharField(
        '房间号', max_length=64, unique=True, primary_key=True)
    room_state = models.SmallIntegerField(
        choices=room_state_choice, default=0, verbose_name="房间从控机状态")
    temp_mode = models.SmallIntegerField(
        '制冷制热模式', choices=temp_mode_choice, default=1)
    blow_mode = models.SmallIntegerField(
        '送风模式', choices=blow_mode_choice, default=1)
    current_temp = models.IntegerField('当前温度')
    target_temp = models.IntegerField('目标温度', default=default_temp)
    # fee_rate = models.FloatField('费率')
    fee = models.FloatField('总费用')
    duration = models.IntegerField('服务时长(秒)')

    def requestAir(self):
        new_air_request = requestQueue(self.room_id, self.room_state, self.temp_mode, self.blow_mode)
        new_air_request.save()

    def cancelAir(self):
        old_air_request = requestQueue.objects.get_object(pk=self.room_id)
        old_air_request.delete()

    def auto_ajust_temp(self):
        if self.room_state == 1:  
            # 达到目标温度，取消送风
            if (self.temp_mode == 1 and self.current_temp <= self.target_temp + eps) or \
                (self.temp_mode == -1 and self.current_temp >= self.target_temp - eps):
                self.cancelAir()
        elif self.room_state == 2:
            # 偏离目标温度一度，请求送风
            if (self.temp_mode == 1 and self.current_temp >= self.target_temp + 1 - eps) or \
                (self.temp_mode == -1 and self.current_temp <= self.target_temp - 1 + eps):
                self.requestAir()


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
        '制冷制热模式', choices=temp_mode_choice, default=0)
    cool_temp_highlimit = models.IntegerField('制冷温控范围最高温')
    cool_temp_lowlimit = models.IntegerField('制冷温控范围最低温')
    heat_temp_highlimit = models.IntegerField('制热温控范围最高温')
    heat_temp_lowlimit = models.IntegerField('制热温控范围最低温')
    default_temp = models.IntegerField('缺省温度')
    feerate_H = models.FloatField('高风费率')
    feerate_M = models.FloatField('中风费率')
    feerate_L = models.FloatField('低风费率')
    max_load = models.IntegerField('最大带机量', default=3)
    waiting_duration = models.IntegerField(default=120)

    def billing(self):
        pass

    # 需要每秒钟运行
    def schedule(self):
        all_rooms = Room.objects.all()
        all_requests = requestQueue.objects.all()
        current_request_cnt = len(all_requests)
        waiting_request = all_requests.filter(room_state=2)
        serving_request = all_requests.filter(room_state=1)
        current_load = len(serving_request)


        # 全部送风请求都已满足，不需要调度
        if current_request_cnt <= current_load:
            return 

        # 尚未超过负载能力，满足送风请求
        if current_request_cnt <= self.max_load:
            # 正处于待机状态，送风
            for satisfy_request in waiting_request:
                satisfy_room = Room.objects.get_object(pk = satisfy_request.room_id)
                #  与设定制冷制热模式一致
                if satisfy_room.temp_mode == self.temp_mode:
                    satisfy_room.room_state = 1
                    satisfy_request.room_state = 1
                    satisfy_request.air_timestamp = timezone.now()
                    satisfy_room.save()
        else: #  超过负载能力，需要进行调度
            for may_satisfy_request in waiting_request:
                weaker_request = serving_request.filter(blow_mode__ls=may_satisfy_request.blow_mode)
                if len(weaker_request) > 0:  # 优先级调度，先满足高风速请求
                    weaker_request = weaker_request[0]  # 挑选出一个低风速请求
                    weaker_request.room_state = 2  # 停止送风
                    weaker_request.request_timestamp = timezone.now()  # 重新计时
                    weaker_request.save()
                else:
                    equal_request = serving_request.filer(blow_mode=may_satisfy_request.blow_mode)
                    current_time = timezone.now()
                    if len(equal_request) > 0 and may_satisfy_request.request_timestamp <= current_time - datetime.timedelta(seconds=self.waiting_duration):  # 时间片调度
                        pass


class RequestRecord(models.Model):
    room_id = models.CharField('房间号', max_length=64)
    room_state = models.SmallIntegerField("房间送风状态", choices=room_state_choice, default=2)
    temp_mode = models.SmallIntegerField('送风模式', choices=temp_mode_choice, default=2)
    start_temp = models.IntegerField('初始温度')
    target_temp = models.IntegerField('目标温度')
    request_time = models.DateTimeField()


class ServiceRecord(models.Model):
    RR = models.ForeignKey("RequestRecord", on_delete=models.CASCADE)
    blow_mode = models.SmallIntegerField('送风模式', choices=blow_mode_choice, default=2)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    power_comsumption = models.FloatField('用电度数')
    ntemp = models.IntegerField('当前温度')
    fee_rate = models.FloatField('费率', choices=feerate_choice, default=2)
    fee = models.FloatField()

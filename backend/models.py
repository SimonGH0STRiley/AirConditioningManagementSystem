from django.db import models
from django.utils import timezone

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
# # 缺省目标温度
# default_temp = 25
# # 各档风速耗电量
feerate_choice = (
    (0.01666, '高风单位耗电量(度/秒)'),
    (0.00833, '高风单位耗电量(度/秒)'),  # 缺省风速
    (0.00556, '高风单位耗电量(度/秒)'),
)


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

    class Meta:
        verbose_name = "空调管理员"                      # 可读性佳的名字
        verbose_name_plural = "空调管理员"               # 复数形式


class Waiter(Personel):
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "前台服务员"                      # 可读性佳的名字
        verbose_name_plural = "前台服务员"               # 复数形式


class Manager(Personel):
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "酒店经理"                       # 可读性佳的名字
        verbose_name_plural = "酒店经理"                # 复数形式


class Tenant(models.Model):
    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256, default='')
    c_time = models.DateTimeField(auto_now_add=True)   # 角色创建时间，用于排序管理
    # room_id = models.CharField('房间号', max_length=64, primary_key=True)
    # date_in = models.DateField('入住日期', null=True)
    # date_out = models.DateField('登出日期', null=True)

    class Meta:
        ordering = ["-c_time"]                         # 按创建时间降序排序, 优先显示新创建的
        verbose_name = "房客"                          # 可读性佳的名字
        verbose_name_plural = "房客"                   # 复数形式

class Guest(Tenant):
    room_id = models.CharField('房间号', max_length=64, primary_key=True)
    date_in = models.DateField('入住日期', null=True)
    date_out = models.DateField('登出日期', null=True)
    def initiateTenant():
        pass
    def requestOn(self):
        room = Room.objects.get(pk=self.room_id)
        room.room_state = 1
        room.save()

    def changeTargetTemp(self, target_temp):
        room = Room.objects.get(pk=self.room_id)
        room.target_temp = target_temp
        room.save()

    def changeFanSpeed(self, fan_speed):
        room = Room.objects.get(pk=self.room_id)
        room.blow_mode = fan_speed
        room.save()
        
    def requestOff(self):
        room = Room.objects.get(pk=self.room_id)
        room.room_state = 0
        room.save()


class TemperatureSensor(models.Model):
    room_id = models.CharField('房间号', max_length=64, unique=True, primary_key=True)
    init_temp = models.FloatField('初始温度')
    current_temp = models.FloatField('当前温度')
    last_update = models.TimeField('上次更新时间', default=timezone.now())
    def update_current_temp(self, current_time = timezone.now()):
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
            delta_temp_change = temp_change_speed_array[room.blow_mode][0] * delta_update_time.total_seconds()
            self.current_temp -= temp_change_direction * delta_temp_change
        self.last_update = current_time


class Room(models.Model):
    room_state_choice = (
        (0, '关闭'),
        (1, '运行'),
        (2, '挂起'),
    )
    room_id = models.CharField('房间号', max_length=64, unique=True, primary_key=True)
    room_state = models.SmallIntegerField(choices=room_state_choice, default=0, verbose_name="房间从控机状态")
    temp_mode = models.SmallIntegerField('制冷制热模式', choices=temp_mode_choice, default=1)
    blow_mode = models.SmallIntegerField('送风模式', choices=blow_mode_choice, default=1)
    current_temp = models.IntegerField('当前温度')
    target_temp = models.IntegerField('目标温度')
    fee_rate = models.FloatField('费率')
    fee = models.FloatField('总费用')
    duration = models.IntegerField('服务时长(秒)')


# class CentralAirConditioner(models.Model):
#     ac_state_choice = (
#         ('close', '关闭'),
#         ('set_Model', '设置模式'),
#         ('ready', '就绪'),
#         ('none', '备用'),
#     )
#
#     ac_state = models.CharField(choices=ac_state_choice, max_length=64, default='close', verbose_name="中央空调状态")
#     temp_mode = models.SmallIntegerField('制冷制热模式', choices=temp_mode_choice, default=0)
#     temp_highlimit = models.IntegerField('温控范围最高温')
#     temp_lowlimit = models.IntegerField('温控范围最低温')
#     default_temp = models.IntegerField('缺省温度')
#     feerate_H = models.FloatField('高风费率')
#     feerate_M = models.FloatField('中风费率')
#     feerate_L = models.FloatField('低风费率')
#
#
# class DetailList(models.Model):
#     list_id = models.CharField('详单号', max_length=64, unique=True)
#     guest_id = models.CharField('房客编号', max_length=64)
#     room_id = models.CharField('房间号', max_length=64)
#     temp_mode = models.SmallIntegerField('制冷制热模式', choices=temp_mode_choice, default=0)
#     blow_mode = models.SmallIntegerField('送风模式', choices=blow_mode_choice, default=2)
#     fee_rate = models.FloatField('费率')
#     fee_duration = models.FloatField('服务时长(分钟)')
#     power_comsumption = models.FloatField('用电度数')
#     fee = models.FloatField('总费用')
#
#
# class BillList(models.Model):
#     list_id = models.CharField('账单号', max_length=64, unique=True)
#     guest_id = models.CharField('房客编号', max_length=64)
#     power_comsumption = models.FloatField('用电总度数')
#     fee = models.FloatField('总费用')
#
#
# class RequestQueue(models.Model):
#     queue_id = models.CharField('服务队列号', max_length=64, unique=True)
#     guest_id = models.CharField('房客编号', max_length=64)
#     room_id = models.CharField('房间号', max_length=64)
#     temp_mode = models.SmallIntegerField('制冷制热模式', choices=temp_mode_choice, default=0)
#     blow_mode = models.SmallIntegerField('送风模式', choices=blow_mode_choice, default=2)
#     request_time = models.DateTimeField('发送请求时间')
#     current_temp = models.IntegerField('当前温度')
#     target_temp = models.IntegerField('目标温度')
#
#
# class ServeQueue(models.Model):
#     queue_id = models.CharField('服务队列号', max_length=64, unique=True)
#     guest_id = models.CharField('房客编号', max_length=64)
#     room_id = models.CharField('房间号', max_length=64)
#     temp_mode = models.SmallIntegerField('制冷制热模式', choices=temp_mode_choice, default=0)
#     blow_mode = models.SmallIntegerField('送风模式', choices=blow_mode_choice, default=2)
#     start_time = models.DateTimeField('开始服务时间')
#     end_time = models.DateTimeField('结束服务时间')
#     fee_duration = models.FloatField('服务时长(分钟)')
#     fee_rate = models.FloatField('费率')
#     power_comsumption = models.FloatField('用电度数')
#     fee = models.FloatField('费用')
#
#
# class Report(models.Model):
#     guest_id = models.CharField('房客编号', max_length=64)
#     room_id = models.CharField('房间号', max_length=64)
#     temp_mode = models.SmallIntegerField('制冷制热模式', choices=temp_mode_choice, default=0)
#     blow_mode = models.SmallIntegerField('送风模式', choices=blow_mode_choice, default=2)
#     start_time = models.DateTimeField('开始服务时间')
#     end_time = models.DateTimeField('结束服务时间')
#     fee_duration = models.FloatField('服务时长(分钟)')
#     request_time = models.DateTimeField('发送请求时间')
#     end_request_time = models.DateTimeField('停止请求时间')
#     request_num = models.IntegerField('发送请求次数')
#     first_temp = models.IntegerField('初始温度')
#     target_temp = models.IntegerField('目标温度')
#     power_comsumption = models.FloatField('用电度数')
#     fee = models.FloatField('费用')
#
#     class Meta:
#         abstract = True
#
#
# class DayReport(Report):
#     # report_date = models.DateField('日报表所属日期')
#     day_power_comsumption = models.FloatField('每日总用电度数')
#     day_fee = models.FloatField('每日空调总费用')
#
#
# class WeekReport(Report):
#     # report_week = models.DateField('周报表所属周次')
#     week_power_comsumption = models.FloatField('每日总用电度数')
#     week_fee = models.FloatField('每日空调总费用')
#
#
# class MonthReport(Report):
#     # report_month = models.DateField('月报表所属月份')
#     daily_power_comsumption = models.FloatField('每日总用电度数')
#     daily_fee = models.FloatField('每日空调总费用')

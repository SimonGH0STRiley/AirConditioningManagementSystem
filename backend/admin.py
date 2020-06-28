from django.contrib import admin

# Register your models here.
from . import models
admin.site.register(models.ACAdministrator)
admin.site.register(models.Manager)
admin.site.register(models.Waiter)
admin.site.register(models.Tenant)
admin.site.register(models.Room)
admin.site.register(models.TemperatureSensor)
admin.site.register(models.CentralAirConditioner)
admin.site.register(models.requestQueue)
admin.site.register(models.RequestRecord)
admin.site.register(models.ServiceRecord)
admin.site.register(models.RoomDailyReport)

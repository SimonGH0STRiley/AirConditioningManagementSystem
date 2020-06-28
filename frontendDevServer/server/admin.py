from django.contrib import admin
from .models import Device,Software,Tracker
# Register your models here.
admin.site.site_header = 'ACMS 数据库管理系统'
admin.site.site_title = 'ACMS 数据库管理系统'

admin.site.register(Device)
admin.site.register(Software)
admin.site.register(Tracker)

from django.contrib import admin

# Register your models here.
from . import models
admin.site.register(models.ACAdministrator)
admin.site.register(models.Manager)
admin.site.register(models.Waiter)
admin.site.register(models.Tenant)

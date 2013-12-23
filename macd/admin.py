from django.contrib import admin
from macd.models import Mac, Device, SeenEvent

class MacAdmin(admin.ModelAdmin):
    pass
admin.site.register(Mac, MacAdmin)

class DeviceAdmin(admin.ModelAdmin):
    pass
admin.site.register(Device, DeviceAdmin)

class SeenEventAdmin(admin.ModelAdmin):
    pass
admin.site.register(SeenEvent, SeenEventAdmin)

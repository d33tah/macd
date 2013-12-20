import datetime

from macd.models import SeenEvent
from django.shortcuts import render

def index(request):
    time_threshold = datetime.date.today() - datetime.timedelta(hours=3)
    items = SeenEvent.objects.filter(date__gte=time_threshold)
    devices_list = []
    for item in items:
        if item.mac.device.description:
            devices_list += [item.mac.device.description]
        else:
            devices_list += ["%s (?)" % item.mac]
    devices = set(devices_list)
    return render(request, 'macd/index.html', {'devices': devices})

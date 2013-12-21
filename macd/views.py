import datetime

from macd.models import SeenEvent
from django.shortcuts import render

def index(request):
    time_threshold = datetime.datetime.now() - datetime.timedelta(minutes=10)
    items = SeenEvent.objects.filter(date__gte=time_threshold)
    devices_set = set(item.mac.device for item in items
                      if not item.mac.device.ignored)

    devices = []
    two_minutes = datetime.datetime.now() - datetime.timedelta(minutes=2)
    for device in devices_set:
        found_2min = False
        for mac in device.mac_set.all():
            items_for_mac = SeenEvent.objects.filter(date__gte=two_minutes,
                                                     mac=mac.mac)
            if len(items_for_mac) > 0:
                found_2min = True
                break
        if found_2min:
            devices += [str(device)]
        else:
            devices += ["(!) %s" % str(device)]

    return render(request, 'macd/index.html', {
        'devices': devices,
        'generated': datetime.datetime.now().strftime("%x %X")
    })

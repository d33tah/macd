import datetime

from macd.models import SeenEvent
from django.shortcuts import render
from django.utils import timezone

def index(request):
    now = timezone.now()
    time_threshold = now - datetime.timedelta(minutes=10)
    items = SeenEvent.objects.filter(date__gte=time_threshold)
    devices_set = set(item.mac.device for item in items
                      if not item.mac.device.ignored)

    devices = []
    two_minutes = now - datetime.timedelta(minutes=2)
    for device in devices_set:
        found_2min = False
        earliest_since = None
        macs = device.mac_set.all()
        items_for_mac = SeenEvent.objects.filter(mac__in=macs)[:10000]
        if len(items_for_mac) > 0:
            for i in range(1, len(items_for_mac)):
                curr, previous = items_for_mac[i].date, items_for_mac[i-1].date
                difference = previous - curr
                if earliest_since is None or previous < earliest_since:
                    earliest_since = previous
                if difference > datetime.timedelta(minutes=10):
                    break
            if items_for_mac[0].date > two_minutes:
                found_2min = True
        if earliest_since:
            earliest_since_local = timezone.localtime(earliest_since)
            earliest_since_formatted = earliest_since_local.strftime("%X")
            earliest_since_str = " (since %s)" % earliest_since_formatted
        else:
            earliest_since_str = ""
        if found_2min:
            device_str = str(device)
        else:
            device_str = "(!) %s" % str(device)
        device_str += earliest_since_str
        devices += [device_str]

    last_event_time = SeenEvent.objects.latest('date').date

    return render(request, 'macd/index.html', {
        'devices': devices,
        'last_event': timezone.localtime(last_event_time)
    })

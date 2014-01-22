import datetime
import subprocess

from macd.models import SeenEvent, Device
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

        devices += [{
            'leaving': found_2min,
            'name': str(device),
            'since': timezone.localtime(earliest_since)
        }]

    last_event_time = SeenEvent.objects.latest('date').date

    viewer_ip = request.META['REMOTE_ADDR']
    viewer_ip = '192.168.88.1'
    viewer_mac = ''
    if (viewer_ip.startswith('192.168.') or
            viewer_ip.startswith('172.16.') or
            viewer_ip.startswith('10.')):
        arp_output = subprocess.check_output(['/usr/sbin/arp', '-n'])
        arp_data_lines = [i for i in arp_output.split("\n")[1:] if i!='']
        arp_macs = {cols[0]: cols[2]
                    for line in arp_data_lines
                    for cols in [line.split()]}
        viewer_mac = arp_macs.get(viewer_ip, '')

    viewer_mac_unknown = list(Device.objects.filter(description='',
                                                    mac=viewer_mac))
    viewer_mac_unknown = True
    viewer_mac = 'test'

    return render(request, 'macd/index.html', {
        'devices': devices,
        'last_event': timezone.localtime(last_event_time),
        'viewer_mac': viewer_mac if viewer_mac_unknown else None,
    })

def unknown(request):
    macs = [m for d in Device.objects.filter(description='')
            for m in d.mac_set.all()]
    devices_dict = {mac: len(SeenEvent.objects.filter(mac=mac))
                    for mac in macs}
    devices = ["%s: %s" % (k, v)
               for k, v in reversed(sorted(devices_dict.items(),
                                           key=lambda x: x[1]))
               ]
    return render(request, 'macd/index.html', {
        'devices': devices,
        'last_event': timezone.localtime(last_event_time)
    })

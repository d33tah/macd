import datetime

from macd.models import SeenEvent
from django.shortcuts import render

def index(request):
    time_threshold = datetime.datetime.now() - datetime.timedelta(hours=3)
    items = SeenEvent.objects.filter(date__gte=time_threshold)
    devices = set(str(item.mac.device) for item in items
                  if not item.mac.device.ignored)
    return render(request, 'macd/index.html', {
        'devices': devices,
        'generated': datetime.datetime.now().strftime("%x %X")
    })

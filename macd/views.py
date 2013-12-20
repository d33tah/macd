import datetime

from macd.models import SeenEvent
from django.shortcuts import render

def index(request):
    time_threshold = datetime.date.today() - datetime.timedelta(hours=3)
    items = SeenEvent.objects.filter(date__gte=time_threshold)
    devices = set(item.mac.device.description for item in items
                  if not item.mac.device.ignored)
    return render(request, 'macd/index.html', {'devices': devices})

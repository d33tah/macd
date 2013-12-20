from django.db import models

class Device(models.Model):
    description = models.CharField(max_length=30)
    ignored = models.BooleanField()

    def __repr__(self):
        return self.description.encode('utf-8')

    def __str__(self):
        return self.description.encode('utf-8')

class Mac(models.Model):
    mac = models.CharField(max_length=17, primary_key=True)
    device = models.ForeignKey('Device')

    def __repr__(self):
        return self.mac

    def __str__(self):
        return self.mac

class SeenEvent(models.Model):
    ordering = ['date']

    mac = models.ForeignKey('Mac')
    date = models.DateTimeField()

    def __repr__(self):
        return "%s [%s]" % (self.mac, self.date)

    def __str__(self):
        return "%s [%s]" % (self.mac, self.date)

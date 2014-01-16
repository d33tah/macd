from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save

class Device(models.Model):
    description = models.CharField(max_length=30, blank=True)
    ignored = models.BooleanField()

    def __repr__(self):
        ret = self.description.encode('utf-8')
        if ret:
            return ret
        else:
            macs = self.mac_set.all()
            if not macs:
                return "empty: %s" % self.id
            else:
                return "%s (?)" % self.mac_set.all()[0]

    __str__ = __repr__

class Mac(models.Model):
    mac = models.CharField(max_length=17, primary_key=True)
    device = models.ForeignKey('Device')

    def __repr__(self):
        return self.mac

    __str__ = __repr__


@receiver(pre_save, sender=Mac)
def mac_save_handler(sender, instance, **kwargs):
    instance.mac = instance.mac.lower().replace('-',':')

class SeenEvent(models.Model):
    class Meta:
        ordering = ['-date']

    mac = models.ForeignKey('Mac')
    date = models.DateTimeField()

    def __repr__(self):
        return "%s [%s]" % (self.mac, self.date)

    def __str__(self):
        return "%s [%s]" % (self.mac, self.date)

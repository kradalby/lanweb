from django.db import models
from django.utils.translation import ugettext as _

# Create your models here.

class LanEvent(models.Model):
    name = models.CharField(_(u'Navn'), max_length=200)
    description = models.TextField(_(u'Beskrivelse'), )
    start_date = models.DateTimeField(_(u'Start dato'), editable=True)
    end_date = models.DateTimeField(_(u'Slutt dato'), editable=True)
    current = models.BooleanField(_(u'Current'), editable=True)
    location = models.CharField(_(u'Lokasjon'), max_length=200)
    price = models.IntegerField(_(u'Pris'))
    numberOfSeats = models.IntegerField(_(u'Antall plasser'), max_length=200)
    shortname = models.CharField(_(u'Shortname'), max_length=20, unique=True)
    

    def __unicode__(self):
        return self.name


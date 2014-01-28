from django.db import models
from apps.event.models import LanEvent
from django.utils.translation import ugettext as _

import os


class Sponsor(models.Model):

    name = models.CharField(_(u'Navn'), max_length=200)
    description = models.TextField(_(u'Beskrivelse'), )
    event = models.ForeignKey(LanEvent, null=False, verbose_name="Event", related_name="Event", editable=True)
    logo_img = models.ImageField(_(u'Logo Bilde'), upload_to='sponsor', max_length=150, blank=True, null=True)
    logo_svg = models.FileField(_(u'Logo SVG'), upload_to='sponsor', max_length=150, blank=True, null=True)
    url = models.URLField(_(u'URL'), max_length=200, blank=True)

    @property
    def image(self):
        if self.logo_svg:
            file_ext = self.logo_svg.name.split(os.path.basename('.'))[1]
            if file_ext == "svg" or file_ext == "svgz":
                return self.logo_svg.url
            else:
                return self.logo_img.url
        else:
            return self.logo_img.url

    def __unicode__(self):
        return self.name

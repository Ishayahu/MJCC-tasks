# -*- coding:utf-8 -*-
# coding=<utf8>

from django.db import models
import re

from django.utils.translation import ugettext_lazy as _
from django.forms import fields

MAC_RE = r'^([0-9a-fA-F]{2}([:-]?|$)){6}$'
mac_re = re.compile(MAC_RE)

class MACAddressFormField(fields.RegexField):
    default_error_messages = {
        'invalid': _(u'Enter a valid MAC address.'),
    }

    def __init__(self, *args, **kwargs):
        super(MACAddressFormField, self).__init__(mac_re, *args, **kwargs)

class MACAddressField(models.Field):
    empty_strings_allowed = False
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 17
        super(MACAddressField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def formfield(self, **kwargs):
        defaults = {'form_class': MACAddressFormField}
        defaults.update(kwargs)
        return super(MACAddressField, self).formfield(**defaults)

class Switch(models.Model):
    name = models.TextField()
    ip = models.GenericIPAddressField()
    mac = MACAddressField()
    commutiny_string = models.TextField(blank=True)
    location = models.TextField()
    parent_switch = models.ManyToManyField(
        'Switch', related_name="children_switch", blank=True)

    def __unicode__(self):
        return u';'.join((str(self.id),
                          self.name,
                          self.ip,
                          self.location))

# -*- coding: utf-8 -*-

from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter

from usertags.params import CHART_TYPE_DICT

register = template.Library()


# settings value
@register.simple_tag
def settings_value(name):
    return getattr(settings, name, "")
    

@stringfilter
@register.filter
def charttype_name(charttype):
    return CHART_TYPE_DICT.get(charttype, '未知')
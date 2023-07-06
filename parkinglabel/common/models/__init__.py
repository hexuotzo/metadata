# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import *
from django.utils.translation import ugettext_lazy as _


class TrimCharField(models.CharField):
    '''
    CharField that ignores leading
        and trailing spaces in data
    '''

    def get_prep_value(self, value):
        return super(TrimCharField, self).get_prep_value(value).strip()

    def pre_save(self, model_instance, add):
        return super(TrimCharField, self).pre_save(model_instance, add).strip()


class ItemInfo(models.Model):
    '''
    数据更新记录基类
    '''

    creator = models.ForeignKey(User,on_delete=models.SET_DEFAULT, default=None)
    create_time = models.DateTimeField('创建时间', auto_now=False, auto_now_add=True)
    update_time = models.DateTimeField('修改时间', auto_now=True, auto_now_add=False)

    class Meta:
        abstract = True

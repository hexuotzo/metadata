# -*- coding: utf-8 -*-

from django.db import models
from django.utils.safestring import mark_safe


class LabelLimitCartype(models.Model):
    label_name = models.CharField('标签中文名', max_length=50)
    e_name = models.CharField('标签名', max_length=50)
    application = models.CharField('应用场景', max_length=100, blank=True, null=True)
    car_plat = models.CharField('平台', max_length=30, blank=True, null=True)
    ps = models.CharField('马力区间', max_length=50, blank=True, null=True, default='',
        help_text=mark_safe('''
            格式说明:<br/>
            范围马力值: 100-200 <br/>
            单马力值:  400-401 <br/>
            单边界值: -100, 600- <br/>
            多个值用英文逗号分隔: 100-200, 300-301, 400- <br/>
            区间规则：左闭右开
        '''))
    car_model = models.CharField('驱动', max_length=30, blank=True, null=True)
    car_series = models.CharField('品系', max_length=30, blank=True, null=True)
    car_engine = models.CharField('发动机', max_length=50, blank=True, null=True)
    label_unit = models.CharField('标签计量单位', max_length=20, blank=True, null=True)
    upper_limit = models.FloatField('计算阈值上限', blank=True, null=True, default=None)
    lower_limit = models.FloatField('计算阈值下限', blank=True, null=True, default=None)
    limit_unit = models.CharField('阈值计量单位', max_length=20, blank=True, null=True)
    rules = models.TextField('计算规则', blank=True, null=True)
    update_time = models.DateTimeField('修改时间', auto_now=True, auto_now_add=False, blank=True, null=True)
    update_user = models.CharField('修改人', max_length=30, blank=True, null=True)

    class Meta:
        db_table = 'label_limit_cartype'
        verbose_name = '标签阈值车辆类型分组'
        verbose_name_plural = "标签阈值车辆类型分组"
        managed = False

    def __unicode__(self):
        return "%s" % self.label_name


class LabelIndustryMapping(models.Model):
    industry_id = models.CharField('行业编号', max_length=3, primary_key=True, help_text='xxx 形式')
    industry_cname = models.CharField('行业中文名', max_length=255)
    industry_ename = models.CharField('行业英文命名', max_length=255)
    industry_note = models.TextField('行业信息备注', blank=True, null=True)

    class Meta:
        db_table = 'industry_mapping'
        verbose_name = '行业字典'
        verbose_name_plural = "行业字典管理"
        managed = False

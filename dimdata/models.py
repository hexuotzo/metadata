# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.


class DimDate(models.Model):
    date = models.DateField('日期', unique=True, blank=True, null=True)
    year = models.CharField('年', max_length=4, blank=True, null=True)
    month = models.CharField('月', max_length=2, blank=True, null=True)
    day = models.CharField('日', max_length=2, blank=True, null=True)
    quarter = models.IntegerField('季度', blank=True, null=True)
    weekday = models.CharField('星期-数', max_length=20, blank=True, null=True)
    dayname = models.CharField('星期-英文', max_length=20, blank=True, null=True)
    monthname = models.CharField('月-英文', max_length=20, blank=True, null=True)
    dayofweek = models.IntegerField('星期中的第几天', blank=True, null=True)
    dayofyear = models.IntegerField('一年中的第几天', blank=True, null=True)
    isweekend = models.IntegerField('是否是周末', blank=True, null=True)
    holidaytype = models.IntegerField('节假日类型', blank=True, null=True)
    holiday_desc = models.CharField('节假日描述', max_length=20, blank=True, null=True)
    issumholiday = models.IntegerField('是否暑假', blank=True, null=True)
    iswinholiday = models.IntegerField('是否寒假', blank=True, null=True)
    isholiday = models.IntegerField('是否节假日', blank=True, null=True)
    isovermonth = models.IntegerField('节假日是否跨月', db_column='Isovermonth', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'dim_date'
        verbose_name = '日期字典表'
        verbose_name_plural = "日期字典表管理"


class DimArea(models.Model):
    prov = models.IntegerField('省编码', blank=True, null=True)
    provname = models.CharField('省名称', max_length=50, blank=True, null=True)
    provfirstletter = models.CharField('省首字母', max_length=10, blank=True, null=True)
    provcarcode = models.CharField('省车码', max_length=10, blank=True, null=True)
    provspell = models.CharField('省拼音', max_length=50, blank=True, null=True)
    city = models.IntegerField('市编码', blank=True, null=True)
    cityname = models.CharField('市名称', max_length=50, blank=True, null=True)
    cityfirstletter = models.CharField('市首字母', max_length=10, blank=True, null=True)
    citycarcode = models.CharField('市车码', max_length=10, blank=True, null=True)
    cityspell = models.CharField('市拼音', max_length=50, blank=True, null=True)
    area = models.IntegerField('区域编码', blank=True, null=True)
    areaname = models.CharField('区域名称', max_length=100, blank=True, null=True)
    areafirstletter = models.CharField('区域首字母', max_length=10, blank=True, null=True)
    areacarcode = models.CharField('区域车码', max_length=10, blank=True, null=True)
    areaspell = models.CharField('区域拼音', max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dim_area'
        unique_together = (('prov', 'city', 'area'),)
        verbose_name = '区域字典表'
        verbose_name_plural = "区域字典表管理"


class DimCarInfo(models.Model):
    vid = models.CharField('终端id', max_length=12, blank=True, null=True)
    vin = models.CharField('底盘号', max_length=50, blank=True, null=True)
    car_plat = models.CharField('品系', max_length=50, blank=True, null=True)
    car_cph = models.CharField('车牌号', max_length=50, blank=True, null=True)
    car_series = models.CharField('平台', max_length=50, blank=True, null=True)
    car_model = models.CharField('车型', max_length=50, blank=True, null=True)
    engine = models.CharField('引擎', max_length=50, blank=True, null=True)
    ps = models.CharField('马力', max_length=50, blank=True, null=True)
    sale_time = models.CharField('销售日期', max_length=10, blank=True, null=True)
    sale_status = models.IntegerField('销售状态', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dim_car_info'
        verbose_name = '车辆信息'
        verbose_name_plural = "车辆信息管理"


class DimRoadCategory(models.Model):
    platroadtype = models.IntegerField('道路种类id', blank=True, null=True)
    roadtype = models.IntegerField('道路类型码', unique=True, blank=True, null=True)
    roadname = models.CharField('道路类型名称', max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dim_road_category'
        verbose_name = '道路种类'
        verbose_name_plural = "道路种类管理"


class DimTimeSlot(models.Model):
    hour = models.CharField('小时', unique=True, max_length=2, blank=True, null=True)
    hour_tag = models.CharField('时段标识', max_length=50, blank=True, null=True)
    hour_desc = models.CharField('时段描述', max_length=50, blank=True, null=True)
    is_peak = models.IntegerField('是否高峰', blank=True, null=True)
    is_danger = models.IntegerField('是否危险', blank=True, null=True)
    hour_tag1 = models.CharField('时段标识1', max_length=50, blank=True, null=True) 
    hour_desc1 = models.CharField('时段描述1', max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dim_time_slot'
        verbose_name = '时段路况'
        verbose_name_plural = "时段路况管理"


class DimWeatherType(models.Model):
    cond_code = models.CharField('天气码', unique=True, max_length=20, blank=True, null=True)
    cond_name = models.CharField('天气名称', max_length=50, blank=True, null=True)
    cond_engname = models.CharField('天气英文名称', max_length=50, blank=True, null=True)
    cond_type = models.CharField('天气标识', max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dim_weather_type'
        verbose_name = '天气类型'
        verbose_name_plural = "天气类型管理"
        
    
class DimCarPlat(models.Model):
    chname = models.CharField('中文名', max_length=100, blank=True, null=True)
    enname = models.CharField('英文名', max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'dim_car_plat'
        verbose_name = '车辆平台'
        verbose_name_plural = "车辆平台管理"


class DimCarBrand(models.Model):
    chname = models.CharField('中文名', max_length=100, blank=True, null=True)
    enname = models.CharField('英文名', max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'dim_car_series'
        verbose_name = '车辆品系'
        verbose_name_plural = "车辆品系管理"


class DimVelocitylimit(models.Model):
    type_id = models.IntegerField('限速类型id')
    lower_limit = models.IntegerField('限速下限km/h')
    upper_limit = models.IntegerField('限速上限km/h')

    class Meta:
        db_table = 'dim_velocitylimit'
        verbose_name = '限速字典表'
        verbose_name_plural = "限速字典表管理"


class DimTrafficState(models.Model):
    plattrafficstate = models.IntegerField('是否拥堵')
    trafficstate = models.IntegerField('拥堵状态码')
    trafficstatename = models.CharField('拥堵描述', max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'dim_traffic_state'
        verbose_name = '拥堵状态表'
        verbose_name_plural = "拥堵状态表管理"


class DimDangerousRoadCategory(models.Model):
    dangeroustype = models.IntegerField('危险道路种类id')
    dangeroustypename = models.CharField('危险道路类型名称', max_length=100)

    class Meta:
        db_table = 'dim_dangerous_road_category'
        verbose_name = '危险道路类型表'
        verbose_name_plural = "危险道路类型表管理"


class DimJobTag(models.Model):
    project_name = models.CharField('项目名称', max_length=100)
    job_name = models.CharField('标记名称', max_length=100)
    mail_list = models.TextField('邮件接收人')
    editor = models.CharField('任务负责人', max_length=100)
    mail_send_interval = models.FloatField('邮件发送时间间隔')
    update_time = models.DateTimeField('更新时间', auto_now=True, auto_now_add=False, blank=True, null=True)
    created = models.DateTimeField('创建时间', auto_now=False, auto_now_add=True, blank=True, null=True)

    class Meta:
        db_table = 'dim_job_tag'
        verbose_name = '任务字典表'
        verbose_name_plural = "任务字典表管理"
        unique_together = (('project_name', 'job_name'),)

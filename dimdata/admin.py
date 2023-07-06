# -*- coding:utf-8 -*-

from django.contrib import admin

from dimdata.models import (DimDate, DimArea, DimCarInfo, 
    DimCarPlat, DimCarBrand,
    DimRoadCategory, DimTimeSlot, DimWeatherType,
    DimVelocitylimit, DimTrafficState,
    DimDangerousRoadCategory, DimJobTag)


class DimDateAdmin(admin.ModelAdmin):
    list_display = ['date', 'quarter', 'dayname', 'monthname', 'isweekend', 'holiday_desc']
    search_fields = ['holiday_desc']
    list_filter = ['date', 'weekday', 'isweekend', 'isholiday', 'holidaytype']

admin.site.register(DimDate, DimDateAdmin)


class DimAreaAdmin(admin.ModelAdmin):
    list_display = ['provname', 'provcarcode', 'cityname', 'areaname']
    search_fields = ['prov', 'provname', 'provspell', 'city', 'cityname', 'cityspell', 'areaname', 'area', 'areaspell']
    list_filter = ['provfirstletter', 'cityfirstletter', 'areafirstletter']

admin.site.register(DimArea, DimAreaAdmin)


class DimCarInfoAdmin(admin.ModelAdmin):
    list_display = ['vid', 'vin', 'car_plat','car_cph', 'car_series', 'car_model', 'engine', 'ps', 'sale_time', 'sale_status']
    search_fields = ['vid', 'vin', 'car_plat','car_cph', 'car_series', 'car_model', 'engine']
    list_filter = ['car_series', 'car_plat', 'car_model', 'engine']

admin.site.register(DimCarInfo, DimCarInfoAdmin)


class DimRoadCategoryAdmin(admin.ModelAdmin):
    list_display = ['platroadtype', 'roadtype', 'roadname']
    search_fields = ['platroadtype', 'roadtype', 'roadname']

admin.site.register(DimRoadCategory, DimRoadCategoryAdmin)


class DimTimeSlotAdmin(admin.ModelAdmin):
    list_display = ['hour', 'hour_tag', 'hour_desc', 'is_peak', 'is_danger', 'hour_tag1', 'hour_desc1']
    search_fields = ['hour_desc', 'hour', 'hour_tag', 'hour_tag1', 'hour_desc1']
    list_filter = ['hour', 'hour_tag', 'is_peak', 'is_danger', 'hour_desc1']

admin.site.register(DimTimeSlot, DimTimeSlotAdmin)


class DimWeatherTypeAdmin(admin.ModelAdmin):
    list_display = ['cond_code', 'cond_name', 'cond_engname', 'cond_type']
    search_fields = ['cond_code', 'cond_name', 'cond_engname', 'cond_type']
    list_filter = ['cond_type']

admin.site.register(DimWeatherType, DimWeatherTypeAdmin)


class DimCarPlatAdmin(admin.ModelAdmin):
    list_display = ['chname', 'enname']
    search_fields = ['chname', 'enname']

admin.site.register(DimCarPlat, DimCarPlatAdmin)


class DimCarBrandAdmin(admin.ModelAdmin):
    list_display = ['chname', 'enname']
    search_fields = ['chname', 'enname']

admin.site.register(DimCarBrand, DimCarBrandAdmin)


class DimVelocitylimitAdmin(admin.ModelAdmin):
    list_display = ['type_id', 'lower_limit', 'upper_limit']
    search_fields = ['type_id', 'lower_limit', 'upper_limit']

admin.site.register(DimVelocitylimit, DimVelocitylimitAdmin)


class DimTrafficStateAdmin(admin.ModelAdmin):
    list_display = ['plattrafficstate', 'trafficstate', 'trafficstatename']
    search_fields = ['plattrafficstate', 'trafficstate', 'trafficstatename']

admin.site.register(DimTrafficState, DimTrafficStateAdmin)


class DimDangerousRoadCategoryAdmin(admin.ModelAdmin):
    list_display = ['dangeroustype', 'dangeroustypename']
    search_fields = ['dangeroustype', 'dangeroustypename']

admin.site.register(DimDangerousRoadCategory, DimDangerousRoadCategoryAdmin)


class DimJobTagAdmin(admin.ModelAdmin):
    list_display = ['project_name', 'job_name', 'editor', 'mail_send_interval', 'update_time', 'created']
    search_fields = ['project_name', 'job_name', 'editor', 'update_time', 'created', 'mail_list']

admin.site.register(DimJobTag, DimJobTagAdmin)

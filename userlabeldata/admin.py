# -*- coding: utf-8 -*-

from django.contrib import admin

from userlabeldata.models import LabelLimitCartype, LabelIndustryMapping

class LabelLimitCartypeAdmin(admin.ModelAdmin):
    
    list_display = ['label_name', 'e_name', 'application', 'car_plat', 'ps', 'car_model', 'car_series', 'car_engine', 'lower_limit', 'upper_limit']
    search_fields = ['label_name', 'e_name', 'application', 'car_plat', 'ps', 'car_model', 'car_series', 'car_engine']
    list_filter = ['car_plat', 'car_model', 'car_series', ]

    def save_model(self, request, obj, form, change):
        obj.update_user = request.user.username
        obj.save()

admin.site.register(LabelLimitCartype, LabelLimitCartypeAdmin)


class LabelIndustryMappingAdmin(admin.ModelAdmin):
    list_display = ['industry_id', 'industry_cname', 'industry_ename']
    search_fields = ['industry_id', 'industry_cname', 'industry_ename']

admin.site.register(LabelIndustryMapping, LabelIndustryMappingAdmin)
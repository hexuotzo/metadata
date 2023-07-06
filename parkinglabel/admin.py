# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from parkinglabel.models import *


# admin.site.register(FirstCategory)
# admin.site.register(SecondCategory)
# admin.site.register(ThirdCategory)

class ParkingTagCustomValueInline(admin.TabularInline):
    model = ParkingLabelElementCustomValue
    fields = ("label_value", "label_desc")


class ParkingTagExtendInline(admin.StackedInline):
    extra = 1
    model = ParkingLabelBaseInfoExtend
    fields = ["label_desc", "label_stat", "validdays", "valtype", "freq"]


class ParkingProjectFilter(SimpleListFilter):
    title = "状态"
    parameter_name = 'stat'

    # 注意: 这个方法显示的是搜索栏里面的数据
    def lookups(self, request, model_admin):
        # 当登录用户为管理员返回的数据
        return CATEGORY_STAT

    # 这个方法是点了搜索之后，根据搜索栏里的参数来返回对应的数据
    def queryset(self, request, queryset):
        obj = ParkingTags.objects
        f = {}

        if request.GET.get("label_lv1_name"):
            f['label_lv1_name'] = request.GET.get("label_lv1_name")

        if request.GET.get("v2name"):
            f['label_lv2_id'] = request.GET.get("v2name")
        if request.GET.get("stat"):
            pn = request.GET.get("stat")
            f['parkinglabelbaseinfoextend__label_stat'] = pn
        qs = obj.filter(**f).all()
        return qs


class ParkingLabelV2Filter(SimpleListFilter):
    title = "二级标签中文名称"
    parameter_name = 'v2name'

    # 注意: 这个方法显示的是搜索栏里面的数据
    def lookups(self, request, model_admin):
        # 当登录用户为管理员返回的数据
        names = ParkingTags.objects.distinct().order_by("label_lv1_name").values("label_lv2_name", "label_lv1_name",
                                                                          "label_lv2_id")

        list_data = []
        for val in names:
            list_data.append((val['label_lv2_id'], val['label_lv1_name'] + '-' + val['label_lv2_name']))

        return list_data

    # 这个方法是点了搜索之后，根据搜索栏里的参数来返回对应的数据
    def queryset(self, request, queryset):
        obj = ParkingTags.objects
        f = {}

        if request.GET.get("label_lv1_name"):
            f['label_lv1_name'] = request.GET.get("label_lv1_name")

        if request.GET.get("v2name"):
            f['label_lv2_id'] = request.GET.get("v2name")

        return obj.filter(**f)


class ParkingTagAdmin(admin.ModelAdmin):
    search_fields = ['label_id', 'label_name', 'label_lv1_name', 'label_lv1_id', 'label_lv2_name',
                     'label_lv2_id__full_tid']
    list_filter = ['label_lv1_name', ParkingLabelV2Filter, ParkingProjectFilter, 'label_class', 'create_time', 'update_time']
    # fields = ('label_name', 'label_name_en','label_id','label_lv1_id','label_lv1_name','label_lv1_name_en','label_lv2_id','label_lv2_name','label_lv2_name_en')
    # readonly_fields = ('label_id','label_lv1_id','label_lv1_name','label_lv1_name_en','label_lv2_id','label_lv2_name','label_lv2_name_en')
    # list_display = ['label_id','label_name','label_name_en','create_time','update_time','label_lv1_id','label_lv1_name','label_lv1_name_en','label_lv2_id','label_lv2_name','label_lv2_name_en']

    fields = ('label_name', 'label_lv1_name', 'label_class', 'label_lv1_id', 'label_lv2_name', 'label_lv2_id')
    readonly_fields = ('label_id', 'label_lv1_name', 'label_lv1_id', 'label_lv2_name')
    list_display = ['label_id', 'label_name', 'label_class', 'label_lv1_name', 'label_lv1_id', 'label_lv2_name',
                    'get_label_lv2_id', 'get_label_stat', 'create_time', 'update_time']
    inlines = [ParkingTagExtendInline, ParkingTagCustomValueInline]

    # stat_change = True

    def add_view(self, request, form_url='', extra_context=None):
        self.fields = ('label_name', 'label_lv1_name', 'label_class', 'label_lv1_id', 'label_lv2_name',
                       'label_lv2_id')  # 将自定义的字段注册到编辑页中
        self.readonly_fields = (
            'label_id', 'label_lv1_name', 'label_lv1_id', 'label_lv2_name')

        ParkingTagExtendInline.fields = ("label_desc", "label_stat", "validdays", "valtype", "freq")
        ParkingTagExtendInline.readonly_fields = []
        ParkingTagCustomValueInline.fields = ("label_value", "label_desc")
        ParkingTagCustomValueInline.readonly_fields = []
        return super(ParkingTagAdmin, self).add_view(request)

    # 重写编辑页, 继承父类方法
    def change_view(self, request, object_id, form_url='', extra_context=None):
        sql = " select ext.id,ext.label_stat from label_base_info as label left join label_base_info_extend as ext on label.label_id=ext.label_id where label.id={}".format(
            object_id)
        stat_data = ParkingLabelBaseInfoExtend.objects.raw(sql)

        if len(stat_data) > 0 and stat_data[0].label_stat == '1':
            self.readonly_fields = self.fields
            ParkingTagExtendInline.readonly_fields = ParkingTagExtendInline.fields
            ParkingTagCustomValueInline.readonly_fields = ParkingTagCustomValueInline.fields
            # self.stat_change = False
        else:
            self.fields = ('label_name', 'label_lv1_name', 'label_class', 'label_lv1_id', 'label_lv2_name',
                           'label_lv2_id')  # 将自定义的字段注册到编辑页中
            self.readonly_fields = (
                'label_id', 'label_lv1_name', 'label_lv1_id', 'label_lv2_name')

            ParkingTagExtendInline.fields = ("label_desc", "label_stat", "validdays", "valtype", "freq")
            ParkingTagExtendInline.readonly_fields = []
            ParkingTagCustomValueInline.fields = ("label_value", "label_desc")
            ParkingTagCustomValueInline.readonly_fields = []
            # self.stat_change = True

        return super(ParkingTagAdmin, self).change_view(request, object_id)

    # def has_change_permission(self, request, obj=None):
    #     return self.stat_change

    def get_label_stat(self, obj):
        return obj.parkinglabelbaseinfoextend.get_label_stat_display()

    get_label_stat.short_description = '状态'

    # def get_label_belong(self,obj):
    #     return obj.label_lv2_id.first_category.get_belong_display()
    #
    # get_label_belong.short_description = '标签主体'

    def get_filter_label_v2_name(self, obj):
        return obj.label_lv2_id.first_category.name + '-' + obj.label_lv2_id.name

    get_filter_label_v2_name.short_description = '二级标签中文名称'

    def get_label_lv1_id(self, obj):
        return "%03d" % obj.label_lv2_id.first_category.id

    get_label_lv1_id.short_description = '一级标签id'

    def get_label_lv1_name(self, obj):
        return obj.label_lv2_id.first_category.name

    get_label_lv1_name.short_description = '一级标签中文名称'

    def get_label_lv1_name_en(self, obj):
        return obj.label_lv2_id.first_category.ename

    get_label_lv1_name_en.short_description = '一级标签英文名称'

    def get_label_lv2_id(self, obj):
        return obj.label_lv2_id.full_tid

    get_label_lv2_id.short_description = '二级标签id'

    def get_label_lv2_name(self, obj):
        return obj.label_lv2_id.name

    get_label_lv2_name.short_description = '二级标签中文名称'

    def get_label_lv2_name_en(self, obj):
        return obj.label_lv2_id.ename

    get_label_lv2_name_en.short_description = '二级标签英文名称'

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.creator = request.user
        obj.save()
        if not hasattr(obj, 'parkinglabelbaseinfoextend'):
            obj.parkinglabelbaseinfoextend = ParkingLabelBaseInfoExtend(label_id=obj)
            obj.parkinglabelbaseinfoextend.save()

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.save()
        formset.save_m2m()

admin.site.register(ParkingTags, ParkingTagAdmin)


class ParkingFirstCategoryAdmin(admin.ModelAdmin):
    search_fields = [
        'name',
        'ename',
        'stat',
    ]
    list_display = ['name', 'ename', 'belong', 'desc', 'online_count', 'stat']
    fields = ('name', 'ename', 'belong', 'desc', 'stat')

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.creator = request.user
        obj.save()

    def online_count(self, obj):
        return ParkingTags.objects.filter(parkinglabelbaseinfoextend__label_stat=1, label_lv1_id="%03d" % obj.id).count()

    online_count.short_description = "上线标签个数"


admin.site.register(ParkingFirstCategory, ParkingFirstCategoryAdmin)


class ParkingSecondCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'ename', 'stat', 'get_first_belong', 'first_category', 'tid', 'full_tid']

    search_fields = ['first_category',
                     'tid',
                     'full_tid',
                     'name',
                     'ename',
                     'stat',
                     ]
    fields = ('first_category', 'name', 'ename', 'desc', 'stat')

    def get_first_category(self, obj):
        return obj.name

    def get_first_belong(self, obj):
        return obj.first_category.get_belong_display()

    get_first_belong.short_description = "标签主体"

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.creator = request.user
        obj.save()

    get_first_category.short_description = '一级分类名称'


admin.site.register(ParkingSecondCategory, ParkingSecondCategoryAdmin)


# admin.site.register(TagsItems)


@admin.register(ParkingLabelElementCustomValue)
class ParkingLabelElementCustomValueAdmin(admin.ModelAdmin):
    list_display = ("label_id", "label_value", "label_desc", "create_time", "update_time")
    fields = ("label_id", "label_value", "label_desc")
    search_fields = ("label_value", "label_desc")

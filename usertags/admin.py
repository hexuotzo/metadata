# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from usertags.models import *


# admin.site.register(FirstCategory)
# admin.site.register(SecondCategory)
# admin.site.register(ThirdCategory)

class TagCustomValueInline(admin.TabularInline):
    model = LabelElementCustomValue
    fields = ("label_value", "label_desc")


class TagExtendInline(admin.StackedInline):
    extra = 1
    model = LabelBaseInfoExtend
    fields = ["label_desc", "label_stat", "validdays", "valtype", "freq"]


class ProjectFilter(SimpleListFilter):
    title = "状态"
    parameter_name = 'stat'

    # 注意: 这个方法显示的是搜索栏里面的数据
    def lookups(self, request, model_admin):
        # 当登录用户为管理员返回的数据
        return CATEGORY_STAT

    # 这个方法是点了搜索之后，根据搜索栏里的参数来返回对应的数据
    def queryset(self, request, queryset):
        obj = Tags.objects
        f = {}

        if request.GET.get("label_lv1_name"):
            f['label_lv1_name'] = request.GET.get("label_lv1_name")

        if request.GET.get("v2name"):
            f['label_lv2_id'] = request.GET.get("v2name")
        if request.GET.get("stat"):
            pn = request.GET.get("stat")
            f['labelbaseinfoextend__label_stat'] = pn
        qs = obj.filter(**f).all()
        return qs


class LabelV2Filter(SimpleListFilter):
    title = "二级标签中文名称"
    parameter_name = 'v2name'

    # 注意: 这个方法显示的是搜索栏里面的数据
    def lookups(self, request, model_admin):
        # 当登录用户为管理员返回的数据
        names = Tags.objects.distinct().order_by("label_lv1_name").values("label_lv2_name", "label_lv1_name",
                                                                          "label_lv2_id")

        list_data = []
        for val in names:
            list_data.append((val['label_lv2_id'], val['label_lv1_name'] + '-' + val['label_lv2_name']))

        return list_data

    # 这个方法是点了搜索之后，根据搜索栏里的参数来返回对应的数据
    def queryset(self, request, queryset):
        obj = Tags.objects
        f = {}

        if request.GET.get("label_lv1_name"):
            f['label_lv1_name'] = request.GET.get("label_lv1_name")

        if request.GET.get("v2name"):
            f['label_lv2_id'] = request.GET.get("v2name")

        return obj.filter(**f)


class TagAdmin(admin.ModelAdmin):
    search_fields = ['label_id', 'label_name', 'label_lv1_name', 'label_lv1_id', 'label_lv2_name',
                     'label_lv2_id__full_tid']
    list_filter = ['label_lv1_name', LabelV2Filter, ProjectFilter, 'label_class', 'create_time', 'update_time']
    # fields = ('label_name', 'label_name_en','label_id','label_lv1_id','label_lv1_name','label_lv1_name_en','label_lv2_id','label_lv2_name','label_lv2_name_en')
    # readonly_fields = ('label_id','label_lv1_id','label_lv1_name','label_lv1_name_en','label_lv2_id','label_lv2_name','label_lv2_name_en')
    # list_display = ['label_id','label_name','label_name_en','create_time','update_time','label_lv1_id','label_lv1_name','label_lv1_name_en','label_lv2_id','label_lv2_name','label_lv2_name_en']

    fields = ('label_name', 'label_lv1_name', 'label_class', 'label_lv1_id', 'label_lv2_name', 'label_lv2_id')
    readonly_fields = ('label_id', 'label_lv1_name', 'label_lv1_id', 'label_lv2_name')
    list_display = ['label_id', 'label_name', 'label_class', 'label_lv1_name', 'label_lv1_id', 'label_lv2_name',
                    'get_label_lv2_id', 'get_label_stat', 'create_time', 'update_time']
    inlines = [TagExtendInline, TagCustomValueInline]

    # stat_change = True

    def add_view(self, request, form_url='', extra_context=None):
        self.fields = ('label_name', 'label_lv1_name', 'label_class', 'label_lv1_id', 'label_lv2_name',
                       'label_lv2_id')  # 将自定义的字段注册到编辑页中
        self.readonly_fields = (
            'label_id', 'label_lv1_name', 'label_lv1_id', 'label_lv2_name')

        TagExtendInline.fields = ("label_desc", "label_stat", "validdays", "valtype", "freq")
        TagExtendInline.readonly_fields = []
        TagCustomValueInline.fields = ("label_value", "label_desc")
        TagCustomValueInline.readonly_fields = []
        return super(TagAdmin, self).add_view(request)

    # 重写编辑页, 继承父类方法
    def change_view(self, request, object_id, form_url='', extra_context=None):
        sql = " select ext.id,ext.label_stat from label_base_info as label left join label_base_info_extend as ext on label.label_id=ext.label_id where label.id={}".format(
            object_id)
        stat_data = LabelBaseInfoExtend.objects.raw(sql)

        if len(stat_data) > 0 and stat_data[0].label_stat == '1':
            self.readonly_fields = self.fields
            TagExtendInline.readonly_fields = TagExtendInline.fields
            TagCustomValueInline.readonly_fields = TagCustomValueInline.fields
            # self.stat_change = False
        else:
            self.fields = ('label_name', 'label_lv1_name', 'label_class', 'label_lv1_id', 'label_lv2_name',
                           'label_lv2_id')  # 将自定义的字段注册到编辑页中
            self.readonly_fields = (
                'label_id', 'label_lv1_name', 'label_lv1_id', 'label_lv2_name')

            TagExtendInline.fields = ("label_desc", "label_stat", "validdays", "valtype", "freq")
            TagExtendInline.readonly_fields = []
            TagCustomValueInline.fields = ("label_value", "label_desc")
            TagCustomValueInline.readonly_fields = []
            # self.stat_change = True

        return super(TagAdmin, self).change_view(request, object_id)

    # def has_change_permission(self, request, obj=None):
    #     return self.stat_change

    def get_label_stat(self, obj):
        return obj.labelbaseinfoextend.get_label_stat_display()

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
        if not hasattr(obj, 'labelbaseinfoextend'):
            obj.labelbaseinfoextend = LabelBaseInfoExtend(label_id=obj)
            obj.labelbaseinfoextend.save()

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.save()
        formset.save_m2m()

admin.site.register(Tags, TagAdmin)


class FirstCategoryAdmin(admin.ModelAdmin):
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
        return Tags.objects.filter(labelbaseinfoextend__label_stat=1, label_lv1_id="%03d" % obj.id).count()

    online_count.short_description = "上线标签个数"


admin.site.register(FirstCategory, FirstCategoryAdmin)


class SecondCategoryAdmin(admin.ModelAdmin):
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


admin.site.register(SecondCategory, SecondCategoryAdmin)


# admin.site.register(TagsItems)


@admin.register(LabelElementValueRel)
class LabelElementValueRelAdmin(admin.ModelAdmin):
    list_display = (
    "label_id", "label_name", "label_class", "label_value", "label_value_ch", "element_id", "element_name",
    "element_value", "element_value_ch", "create_time", "update_time",)

    fields = ("label_id", "label_name", "label_class", "label_value", "label_value_ch", "element_id", "element_name",
              "element_value", "element_value_ch")

    search_fields = ("label_id", "label_name", "label_value_ch", "element_value", "element_value_ch", "label_class")


@admin.register(LabelElementCustomValue)
class LabelElementCustomValueAdmin(admin.ModelAdmin):
    list_display = ("label_id", "label_value", "label_desc", "create_time", "update_time")
    fields = ("label_id", "label_value", "label_desc")
    search_fields = ("label_value", "label_desc")

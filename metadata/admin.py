# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.db.models import ManyToManyField, TextField
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Count
from django.forms.models import model_to_dict
from django.contrib.admin import AdminSite
import datetime
import json
from metadata.models import (AppBuriedPoint, MonitorMakefileTag, MdTableInfoRecord,
                             MdIndexInfo, MdIndexInfoLog, FieldInfo0020, FieldInfo0020Log,
                             MdIndexParent, MdThreshold, MdTsktagInfo, DimSrc, PccDepotName, PccProblemDetail,
                             PccUpgradeDetail,
                             PccVehicleInfo, HiveTableInfo, HiveTableMaintain, HiveTableColumnInfo, HiveSearch,
                             HiveSearchIndex, Detail,
                             HiveSearchLog, MakefileTagRelations, HiveTableCapacity, QualityRule, RuleExecuteLog,
                             TableStorage, TableStandard, FieldStandard, TableExample, QualityTrend, Dict, WordSummary,
                             HiveTableExtend, StorageRanking, UserStorage, HiveOrgInfo, HiveOwnerOrg, UserOrgTable)

from metadata.views import t_search
from metadata.utils import exportExcel
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

admin.sites.AdminSite.site_title = '元数据管理平台'
admin.sites.AdminSite.site_header = '元数据管理平台'
admin.sites.AdminSite.site_url = '/admin/'


class AppBuriedPointAdmin(admin.ModelAdmin):
    list_display = ['labelid', 'lablename', 'pagename', 'action', 'modname', 'appname']
    search_fields = ['labelid', 'lablename', 'modid', 'modname', 'action', 'pageid', 'pagename', 'appid', 'appname']
    list_filter = ['appname', 'action', 'modname', ]


admin.site.register(AppBuriedPoint, AppBuriedPointAdmin)


class MonitorMakefileTagAdmin(admin.ModelAdmin):
    list_display = ['tagchn', 'tageng', 'finishtime', 'cycle']
    search_fields = ['tagchn', 'tageng', 'finishtime', 'cycle']


admin.site.register(MonitorMakefileTag, MonitorMakefileTagAdmin)


class MdTableInfoRecordAdmin(admin.ModelAdmin):
    list_display = ['table_eng', 'table_chi', 'source', 'database_name', 'show_tag', 'update_time']
    search_fields = ['source', 'database_name', 'table_eng', 'table_chi']
    list_filter = ['source', 'database_name', 'show_tag', 'update_time']


admin.site.register(MdTableInfoRecord, MdTableInfoRecordAdmin)


# class MdIndexInfoRelationshipInline(admin.TabularInline):

#     model = RelMdTableTable
#     fk_name = 'p_table_id'
#     extra = 1
#     max_num = 100
#     can_delete = True
#     verbose_name_plural = '父指标配置'


class MdIndexParentInline(admin.TabularInline):
    model = MdIndexParent
    extra = 15
    can_delete = True
    fk_name = 'md_index'
    verbose_name_plural = '父指标配置'


class MdIndexInfoAdmin(admin.ModelAdmin):
    list_display = ['index_name', 'index_desc', 'index_definition', 'index_unit', 'data_type', 'update_editor',
                    'edit_log']
    search_fields = ['create_editor', 'index_name', 'index_desc', 'index_owner', 'index_definition', 'update_editor',
                     'source_table']
    list_filter = ['create_time', 'update_time', 'index_owner', 'index_unit']
    readonly_fields = ('update_time', 'create_time')
    inlines = [MdIndexParentInline]

    class Media:
        css = {
            "all": ("/static/css/select2-bootstrap.css",
                    "/static/css/select2.css")
        }
        js = (  # "/static/js/select2.min.js",
            # "/static/js/select2_locale_zh-CN.js",
            "/static/js/select2.mdindex.js",)

    def edit_log(self, obj):
        uri = "/admin/metadata/mdindexinfolog/?q="
        key = obj.index_name
        return mark_safe('<a target=_blank href="%s%s">修改记录</a>' % (uri, key))

    edit_log.short_description = '操作'

    def save_model(self, request, obj, form, change):

        if obj.id:
            old_obj = MdIndexInfo.objects.get(pk=obj.id)

            MdIndexInfoLog.objects.create(
                index_name=old_obj.index_name,
                index_desc=old_obj.index_desc,
                source_table=old_obj.source_table,
                index_unit=old_obj.index_unit,
                data_type=old_obj.data_type,
                index_definition=old_obj.index_definition,
                index_rule=old_obj.index_rule,
                parent_index='',
                index_owner=old_obj.index_owner,
                update_editor=old_obj.update_editor)

        if not obj.id:
            obj.create_editor = request.user.username
        obj.update_editor = request.user.username
        obj.save()


admin.site.register(MdIndexInfo, MdIndexInfoAdmin)


class MdIndexInfoAdminLog(admin.ModelAdmin):
    list_display = ['index_name', 'index_desc', 'source_table', 'index_definition', 'index_unit', 'data_type',
                    'index_rule', 'parent_index', 'index_owner', 'update_editor', 'update_time']
    search_fields = ['=index_name']

    list_display_links = None

    def has_add_permission(self, request):
        # 禁用添加按钮
        return False

    def has_delete_permission(self, request, obj=None):
        # 禁用删除按钮
        return False

    def get_actions(self, request):
        # 在actions中去掉‘删除’操作
        actions = super(MdIndexInfoAdminLog, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


admin.site.register(MdIndexInfoLog, MdIndexInfoAdminLog)


class FieldInfoAdmin0020(admin.ModelAdmin):
    list_display = ['field_name_en', 'field_name_ch', 'file_protoc', 'field_unit', 'field_type', 'threshold',
                    'threshold_zh', 'is_monitor', 'field_explain', 'available', 'field_orig', 'operator', 'create_time',
                    'edit_time', 'edit_log']
    search_fields = ['field_name_en', 'field_name_ch', 'field_unit', 'field_type', 'threshold', 'threshold_zh',
                     'field_explain', 'available', 'file_protoc']
    list_filter = ['create_time', 'edit_time', 'file_protoc', 'is_monitor']

    def edit_log(self, obj):
        uri = "/admin/metadata/fieldinfo0020log/?q="
        key = "%s+%s" % (obj.field_name_en, obj.field_orig)
        return mark_safe('<a target=_blank href="%s%s">修改记录</a>' % (uri, key))

    edit_log.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.operator = request.user.username
        obj.save()

        FieldInfo0020Log.objects.create(
            field_name_en=obj.field_name_en,
            field_name_ch=obj.field_name_ch,
            field_unit=obj.field_unit,
            field_type=obj.field_type,
            # field_min=obj.field_min,
            # field_max=obj.field_max,
            threshold=obj.threshold,
            threshold_zh=obj.threshold_zh,
            is_monitor=obj.is_monitor,
            field_explain=obj.field_explain,
            field_orig=obj.field_orig,
            available=obj.available,
            file_protoc=obj.file_protoc,
            operator=obj.operator)


admin.site.register(FieldInfo0020, FieldInfoAdmin0020)


class FieldInfoAdmin0020Log(admin.ModelAdmin):
    list_display = ['field_name_en', 'field_name_ch', 'field_unit', 'field_type', 'threshold', 'threshold_zh',
                    'is_monitor', 'field_explain', 'field_orig', 'operator', 'create_time']
    search_fields = ['=field_name_en', '=field_orig']
    list_filter = ['create_time']

    list_display_links = None  # 禁用编辑链接

    def has_add_permission(self, request):
        # 禁用添加按钮
        return False

    def has_delete_permission(self, request, obj=None):
        # 禁用删除按钮
        return False

    def get_actions(self, request):
        # 在actions中去掉‘删除’操作
        actions = super(FieldInfoAdmin0020Log, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


admin.site.register(FieldInfo0020Log, FieldInfoAdmin0020Log)


class MdThresholdAdmin(admin.ModelAdmin):
    list_display = ['name', 'column_name', 'val_min', 'val_max', 'default_val', 'desc']
    search_fields = ['name', 'column_name']


admin.site.register(MdThreshold, MdThresholdAdmin)


class MdTsktagInfoAdmin(admin.ModelAdmin):
    list_display = ['task_tag', 'task_type', 'task_name', 'task_desc', 'task_owner', 'task_runtime', 'is_online',
                    'online_time', 'downline_time', 'update_editor', 'create_time']
    list_filter = ['task_tag', 'task_type', 'task_owner', 'is_online']
    readonly_fields = ['online_time', 'downline_time']

    def save_model(self, request, obj, form, change):
        obj.update_user = request.user.username
        if 'is_online' in form.changed_data:
            if obj.is_online == 1:
                obj.online_time = datetime.datetime.now()
            elif obj.is_online == 0:
                obj.downline_time = datetime.datetime.now()
        obj.save()


admin.site.register(MdTsktagInfo, MdTsktagInfoAdmin)


class PccDepotNameAdmin(admin.ModelAdmin):
    list_display = ['depot_name']
    search_fields = ['depot_name']

    class Media:
        js = (  # "/static/js/select2.min.js",
            # "/static/js/select2_locale_zh-CN.js",
            "/static/js/pcc.js",)


admin.site.register(PccDepotName, PccDepotNameAdmin)


class PccProblemDetailAdmin(admin.ModelAdmin):
    list_display = ['device_type', 'behind_vid', 'front_vid', 'chassis_number', 'problem_describe', 'problem_solution',
                    'status', 'other_remark']
    search_fields = ['chassis_number', 'behind_vid', 'front_vid']

    class Media:
        js = (  # "/static/js/select2.min.js",
            # "/static/js/select2_locale_zh-CN.js",
            "/static/js/pcc.js",)


admin.site.register(PccProblemDetail, PccProblemDetailAdmin)


class PccUpgradeDetailAdmin(admin.ModelAdmin):
    list_display = ['upgrade_device', 'behind_vid', 'front_vid', 'chassis_number', 'upgrade_time', 'upgrade_version',
                    'other_remark']
    search_fields = ['chassis_number', 'behind_vid', 'front_vid']

    class Media:
        js = (  # "/static/js/select2.min.js",
            # "/static/js/select2_locale_zh-CN.js",
            "/static/js/pcc.js",)


admin.site.register(PccUpgradeDetail, PccUpgradeDetailAdmin)


class PccVehicleInfoAdmin(admin.ModelAdmin, exportExcel):
    list_display = ('depot', 'device_type', 'install_type', 'car_number', 'engine_model', 'trans_model', 'trans_type',
                    'front_sim', 'behind_sim', 'front_vid', 'behind_vid', 'at_sn', 'at_id', 'car_model',
                    'chassis_number',
                    'install_time', 'device_remove_status', 'device_remove_time', 'install_verion', 'car_owner',
                    'driver_name',
                    'driver_phone', 'driver_habit', 'speed_range', 'other_remark')
    search_fields = ['chassis_number', 'behind_vid', 'front_vid']
    # fields = ('depot', 'device_type', 'install_type', 'car_number', 'engine_model', 'trans_model','trans_type',
    #                 'front_sim', 'behind_sim', 'front_vid', 'behind_vid','at_sn','at_id', 'car_model', 'chassis_number',
    #                 'install_time', 'device_remove_status', 'device_remove_time', 'install_verion', 'car_owner', 'driver_name',
    #                 'driver_phone', 'driver_habit', 'speed_range', 'other_remark')
    # actions = ['download_excel']
    special_fields = {
        'device_type': 'get_device_type_display',
        'install_type': 'get_install_type_display',
        'device_remove_status': 'get_device_remove_status_display',
        'driver_habit': 'get_driver_habit_display'
    }

    class Media:
        js = (  # "/static/js/select2.min.js",
            # "/static/js/select2_locale_zh-CN.js",
            "/static/js/pcc.js",)


admin.site.register(PccVehicleInfo, PccVehicleInfoAdmin)


class DimSrcAdmin(admin.ModelAdmin):
    list_display = ['src_chname', 'src', 'depotLogo', 'create_time', 'update_time']
    list_filter = ['create_time', 'update_time']
    search_fields = ['src', 'src_chname', 'depotLogo']


admin.site.register(DimSrc, DimSrcAdmin)


class HiveTableInfoAdmin(admin.ModelAdmin):
    """
    hive元数据管理
    """
    list_display = ["link_info", "db_name", "tbl_owner", "is_online", "tbl_comment", "edit_log", "show_column"]
    search_fields = ["tbl_name", "db_name", "tbl_owner"]
    list_filter = ["db_name", "tbl_owner", "is_online"]
    readonly_fields = ["tbl_id", "tbl_name", "db_id", "db_name", "tbl_type", "tbl_owner", "create_time", "is_online",
                       "offline_time", "update_time", "location", "partition", "tbl_comment", ]
    actions_on_top = False

    list_display_links = None

    # inlines = [HiveTableColumnInline]

    def link_info(self, obj):
        uri = "/admin/metadata/detail/?db_name=%s&table_name=%s" % (obj.db_name, obj.tbl_name)

        return mark_safe('<a target=_blank href="%s">%s</a>' % (uri, obj.tbl_name))

    link_info.short_description = '表名称'

    def edit_log(self, obj):
        # Publisher.objects.filter(name="xx", country="xx")
        maintainObj = HiveTableMaintain.objects.get(db_name=obj.db_name, table_name=obj.tbl_name)

        uri = "/admin/metadata/hivetablemaintain/%s/change/" % (maintainObj.id)

        return mark_safe('<a target=_blank href="%s">修改表注释</a>' % (uri))

    edit_log.short_description = '操作'

    def show_column(self, obj):
        uri = "/admin/metadata/hivetablecolumninfo/?id=%s" % (obj.tbl_id)

        return mark_safe('<a target=_blank href="%s">编辑字段</a>' % (uri))

    show_column.short_description = ''

    def has_add_permission(self, request):
        # 禁用添加按钮
        return False

    def has_delete_permission(self, request, obj=None):
        # 禁用删除按钮
        return False

    def change_view(self, request, object_id, extra_context=None):
        extra_context = {'show_save_and_add_another': False, 'show_save_and_continue': False, 'show_save': False,
                         'readonly': True}

        return super(HiveTableInfoAdmin, self).change_view(request, object_id, extra_context=extra_context)


admin.site.register(HiveTableInfo, HiveTableInfoAdmin)


class HiveTableMaintainAdmin(admin.ModelAdmin):
    """
    hive表注释管理
    """
    list_display = ["table_name", "db_name", "table_desc_maintain", "create_time"]
    search_fields = ["table_name", "db_name"]
    list_filter = ["db_name", "table_name"]
    readonly_fields = ["db_name", "table_name", "id", "create_time"]
    actions_on_top = False

    def has_add_permission(self, request):
        # 禁用添加按钮
        return False

    def has_delete_permission(self, request, obj=None):
        # 禁用删除按钮
        return False

    def change_view(self, request, object_id, extra_context=None):
        extra_context = {'show_save_and_add_another': False, 'show_save_and_continue': False, 'show_save': True,
                         'readonly': True}

        return super(HiveTableMaintainAdmin, self).change_view(request, object_id, extra_context=extra_context)


admin.site.register(HiveTableMaintain, HiveTableMaintainAdmin)


class HiveSearchAdmin(admin.ModelAdmin):
    """
    数据字典
    """
    change_form_template = 'admin/metadata/t_search.html'

    def changelist_view(self, request, object_id=None, extra_content={}):
        searchKey = ''
        if len(request.GET) > 0:
            searchKey = request.GET['search_key'].strip()

        if searchKey:
            sql = '''
                SELECT * 
                from (
                    select id,db_id,db_name,table_id,table_name,column_names,table_content,column_content,is_online,table_sort_priority,
                    case when db_name in ('dw_warehouse','dwd','dws','dim') then 20
                         when db_name in ('app','label','hbase') then 10
                         when db_name in ('test') then 0
                         else 5 end as floor_sort
                    from hive_search_index
                ) t
                where is_online=1 and (table_name like '%%{searchKey}%%' or table_content like '%%{searchKey}%%'
                or column_names like '%%{searchKey}%%' or column_content like '%%{searchKey}%%')
                order by floor_sort desc, table_sort_priority desc 
                limit 100
            '''.format(searchKey=searchKey)
        else:
            sql = '''
                select * from (
                SELECT
                id,db_id,db_name,table_id,table_name,column_names,table_content,column_content,table_sort_priority,
                case when db_name in ('dw_warehouse','dwd','dws','dim') then 20
                         when db_name in ('app','label','hbase') then 10
                         when db_name in ('test') then 0
                         else 5 end as floor_sort
                from 
                hive_search_index
                where  is_online=1
                ) t order by floor_sort desc, table_sort_priority desc
                limit 100
            '''.format(searchKey=searchKey)

        # return HttpResponse(sql)
        tableResult = HiveSearchIndex.objects.raw(sql)
        resultDict = []
        key = 0
        searchIndex = HiveSearchIndex()
        if tableResult:
            for result in tableResult:
                key = key + 1
                column_content = searchIndex.getSubstrString(result.column_content, searchKey)
                # column_content = result.column_content
                column_names = searchIndex.getSubstrString(result.column_names, searchKey)
                # column_names = result.column_names

                newDict = {
                    'url': '/admin/metadata/detail/?id=%s' % (result.id),
                    'id': result.id,
                    'db_name': result.db_name,
                    'table_name': result.table_name.replace(searchKey, "<font color='red'>%s</font>" % (searchKey)),
                    'table_content': result.table_content.replace(searchKey,
                                                                  "<font color='red'>%s</font>" % (searchKey)),
                    'column_content': column_content.replace(searchKey, "<font color='red'>%s</font>" % (searchKey)),
                    'column_names': column_names.replace(searchKey, "<font color='red'>%s</font>" % (searchKey)),
                }
                resultDict.append(newDict)
        else:
            pass

        paginator = Paginator(resultDict, 10)  # 每页25条
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)  # contacts为Page对象！
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)

        extra_content['tableResult'] = resultDict
        extra_content['searchKey'] = searchKey
        extra_content['contacts'] = contacts

        return super(HiveSearchAdmin, self).change_view(request, object_id, extra_context=extra_content)


admin.site.register(HiveSearch, HiveSearchAdmin)


class DetailAdmin(admin.ModelAdmin):
    change_form_template = 'admin/metadata/t_detail.html'

    def changelist_view(self, request, object_id=None, extra_content={}):
        id = 0
        # return HttpResponse(request.GET)
        if 'id' in request.GET:
            id = request.GET['id']
        if id:
            searchIndexInfo = HiveSearchIndex.objects.get(pk=id)
        else:
            # db_name = request.GET['db_name'].strip().lower()
            # tbl_name = request.GET['table_name'].strip().lower()
            # searchIndexInfo = HiveSearchIndex.objects.filter(db_name=db_name, table_name=tbl_name, is_online=1)

            try:
                db_name = request.GET['db_name'].strip().lower()
                tbl_name = request.GET['table_name'].strip().lower()
                searchIndexInfo = HiveSearchIndex.objects.get(db_name=db_name, table_name=tbl_name, is_online=1)
            except:
                return HttpResponse('库名或表名不存在')

        tableInfo = HiveTableInfo.objects.get(tbl_id=searchIndexInfo.table_id)

        sql = '''select 
                    t2.id,
                t1.table_name,
                t1.column_name,
                t1.column_type,
                t1.column_desc,
                t2.column_idx+1 as column_idx,
                t2.column_desc_maintain
                from hive_table_column_info t1 
                inner join 
                hive_column_maintain t2 
                on t1.db_name=t2.db_name and t1.table_name=t2.table_name and t1.integer_idx=t2.column_idx
                where t1.tbl_id='%s' order by t2.column_idx
                    ''' % (searchIndexInfo.table_id)
        columnResult = HiveTableColumnInfo.objects.raw(sql)

        maintainInfo = HiveTableMaintain.objects.get(db_name=searchIndexInfo.db_name,
                                                     table_name=searchIndexInfo.table_name)

        try:
            tableExtend = HiveTableExtend.objects.get(tbl_id=searchIndexInfo.table_id)
        except:
            tableExtend = {}

        sql = '''
        select id, storage/(1024*1024) as storage,records,last_ddl_time,
        FROM_UNIXTIME(last_ddl_time,'%%Y-%%m-%%d %%H:%%i') as last_ddl_date,
        calculate_date  from hive_table_capacity
        where tbl_id='{table_id}' and storage_type='1' order by calculate_date desc limit 10 
        '''.format(table_id=searchIndexInfo.table_id)
        tableCapacity = HiveTableCapacity.objects.raw(sql)
        if not tableCapacity:
            sql = '''
                    select id, storage/(1024*1024) as storage,records,last_ddl_time,
                    FROM_UNIXTIME(last_ddl_time,'%%Y-%%m-%%d %%H:%%i') as last_ddl_date,
                    calculate_date  from hive_table_capacity
                    where tbl_id='{table_id}' and storage_type='2' order by calculate_date desc limit 10 
                    '''.format(table_id=searchIndexInfo.table_id)
            tableCapacity = HiveTableCapacity.objects.raw(sql)

        lineDataX = []
        lineDataY = []
        lineDataRow = []
        for capacity in tableCapacity:
            lineDataX.append(str(capacity.calculate_date))
            # formatStorage = TableStorage.readable_file_size(float(capacity.storage),2)
            lineDataY.append(str(capacity.storage))
            lineDataRow.append(str(capacity.records))

        sql = '''
                SELECT
                lower(tag_rely) as id,
                lower(tag_rely) as label,
                'success' as status,
                lower(tag) as target
                from 
                makefile_tag_relations_test
                where tag='{table_name}'
                group by tag,tag_rely
                union all 
                select 
                lower('{table_name}') as id,
                lower('{table_name}') as label,
                'success' as status,
                '' as target
            '''.format(table_name=searchIndexInfo.table_name)

        # return HttpResponse(sql)
        tagResult = MakefileTagRelations.objects.raw(sql)
        tarDict = {}
        key = 0
        for value in tagResult:
            key = key + 1
            newDict = {
                'id': value.id,
                'label': value.label,
                'status': value.status,
                'target': value.target,
            }
            tarDict[key] = newDict

        replyJson = json.dumps(tarDict)
        current_user = request.user
        # 插入记录数据
        addDict = {
            'index_id': id,
            'db_name': searchIndexInfo.db_name,
            'table_name': searchIndexInfo.table_name,
            'author_id': current_user.id,
            'create_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        HiveSearchLog.objects.create(**addDict)
        try:
            exampleInfo = TableExample.objects.get(tbl_id=searchIndexInfo.table_id)
        except Exception:
            exampleInfo = []

        column_data_new = []
        column_data_field = []
        if exampleInfo:
            column_data_new = json.loads(exampleInfo.column_data)

            if column_data_new:
                for data in column_data_new:
                    columnData = data
                column_data_field = columnData.keys()
            else:
                column_data_field = exampleInfo.column_field.split(',')

        extra_content['indexInfo'] = searchIndexInfo
        extra_content['tableInfo'] = tableInfo
        extra_content['tableCapacity'] = tableCapacity
        extra_content['columnResult'] = columnResult
        extra_content['maintainInfo'] = maintainInfo
        extra_content['dependArr'] = replyJson
        extra_content['lineDataX'] = ','.join(lineDataX)
        extra_content['lineDataY'] = ','.join(lineDataY)
        extra_content['lineDataRow'] = ','.join(lineDataRow)
        extra_content['exampleInfo'] = exampleInfo
        extra_content['exampleData'] = column_data_new
        extra_content['exampleField'] = column_data_field
        extra_content['tableExtend'] = tableExtend

        return super(DetailAdmin, self).change_view(request, object_id, extra_context=extra_content)


admin.site.register(Detail, DetailAdmin)


# hive表字段信息展示及维护
class HiveTableColumnInfoAdmin(admin.ModelAdmin):
    change_form_template = 'admin/metadata/table_column_list.html'

    def changelist_view(self, request, object_id=None, extra_content={}):
        tbl_id = request.GET['id']

        sql = '''select 
            t2.id,
        t1.table_name,
        t1.column_name,
        t1.column_type,
        t1.column_desc,
        t2.column_idx+1 as column_idx,
        t2.column_desc_maintain
        from hive_table_column_info t1 
        inner join 
        hive_column_maintain t2 
        on t1.db_name=t2.db_name and t1.table_name=t2.table_name and t1.integer_idx=t2.column_idx
        where t1.tbl_id='%s' order by t2.column_idx
            ''' % (tbl_id)
        results = HiveTableColumnInfo.objects.raw(sql)

        tableInfo = HiveTableInfo.objects.get(pk=tbl_id)

        extra_content['results'] = results
        extra_content['tbl_id'] = tbl_id
        extra_content['table_info'] = tableInfo

        return super(HiveTableColumnInfoAdmin, self).change_view(request, object_id, extra_context=extra_content)


admin.site.register(HiveTableColumnInfo, HiveTableColumnInfoAdmin)


# 数据治理规则
class QualityRuleAdmin(admin.ModelAdmin):
    """
    数据质量规则管理
    """
    list_display = ["id", "rule_name", "rule_type", "table_name", "column_name", "get_sampling_code", "check_type",
                    "check_mode", "get_compare_mode_name", "excepted_value", "percent_min", "create_time", "edit_log"]
    search_fields = ["rule_name", "table_name"]
    list_filter = ["rule_type", "table_name"]
    list_per_page = 15
    # readonly_fields = ["db_name", "table_name","id","create_time" ]
    # actions_on_top = False
    add_form_template = 'admin/metadata/quality_add.html'
    change_form_template = 'admin/metadata/quality_edit.html'
    actions = ['delete_selected']

    # list_display_links = None
    def edit_log(self, obj):
        uri = "/admin/metadata/ruleexecutelog/?q="
        key = obj.id
        return mark_safe(
            '<a class="btn btn-info margin" style="color: #fff;" target=_blank href="%s%s">执行记录</a><a class="btn bg-orange margin execute_now" style="color: #fff;" data-attr="%s" href="javascript:void(0);">立即执行</a>' % (
            uri, key, key))

    edit_log.short_description = '操作'

    def get_sampling_code(self, obj):
        return QualityRule.get_sampling_mode_name(obj.sampling_mode)

    get_sampling_code.short_description = '采样方式'

    def get_compare_mode_name(self, obj):
        return QualityRule.get_compare_mode_name(obj.compare_mode)

    get_compare_mode_name.short_description = '比较方式'

    # 删除规则
    def delete_selected(modeladmin, request, queryset):
        c = 0
        for i in queryset:
            i.delete()
            c += 1
        msg = '成功删除了{}个规则'.format(c)
        modeladmin.message_user(request, msg)

    delete_selected.short_description = '删除已选项'

    def add_view(self, request, form_url='', extra_context={}):
        db_result = HiveTableInfo.objects.values("db_name").annotate(counts=Count('tbl_id'))
        extra_context['db_all'] = db_result

        if request.POST:
            postData = request.POST
            current_user = request.user
            addDict = {
                'rule_name': postData['rule_name'],
                'rule_type': postData['rule_type'],
                'db_name': postData['db_name'],
                'table_name': postData['table_name'],
                'column_name': postData['column_name'],
                'custom_sql': postData['custom_sql'],
                'sampling_mode': postData['sampling_mode'],
                'filter_condition': postData['filter_condition'],
                'check_type': postData['check_type'],
                'check_mode': postData['check_mode'],
                'compare_mode': postData['compare_mode'],
                'excepted_value': postData['excepted_value'],
                'percent_min': postData['percent_min'],
                'rule_desc': postData['rule_desc'],
                'status': 'on',
                'warning_mode': postData['warning_mode'],
                'warning_receiver': postData['warning_receiver'],
                'execute_type': postData['execute_type'],
                'execute_hour': postData['execute_hour'],
                'create_user': current_user.username,
                'create_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            QualityRule.objects.create(**addDict)
            with open('/tmp/debug.log', 'w') as f:
                f.write(json.dumps(addDict))

            return HttpResponseRedirect("/admin/metadata/qualityrule")

        return super(QualityRuleAdmin, self).add_view(request, extra_context=extra_context)

    # 编辑
    def change_view(self, request, object_id, extra_context=None):
        extra_context = {'show_save_and_add_another': False, 'show_save_and_continue': False, 'show_save': True,
                         'readonly': True}
        extra_context['object_id'] = object_id
        quality_info = QualityRule.objects.get(pk=object_id)

        quality_info.compare_mode = QualityRule.get_compare_mode_name(quality_info.compare_mode)
        extra_context['quality_info'] = quality_info

        if request.POST:
            postData = request.POST
            current_user = request.user

            objectQ = QualityRule.objects.get(pk=postData['id'])

            objectQ.rule_name = postData['rule_name']
            objectQ.filter_condition = postData['filter_condition']
            objectQ.custom_sql = postData['custom_sql']
            objectQ.excepted_value = postData['excepted_value']
            objectQ.percent_min = postData['percent_min']
            objectQ.rule_desc = postData['rule_desc']
            objectQ.warning_receiver = postData['warning_receiver']
            objectQ.status = postData['status']
            objectQ.execute_type = postData['execute_type']
            objectQ.execute_hour = postData['execute_hour']
            objectQ.save()

            return HttpResponseRedirect("/admin/metadata/qualityrule")

        return super(QualityRuleAdmin, self).change_view(request, object_id, extra_context=extra_context)

    def save_model(self, request, obj, form, change):

        with open('/tmp/debug.log', 'w') as f:
            f.write(obj)

        if form.is_valid():

            super(QualityRuleAdmin, self).save_model(request, obj, form, change)
        else:
            return HttpResponse('not valid')


admin.site.register(QualityRule, QualityRuleAdmin)


# 规则执行日志
class RuleExecuteLogdmin(admin.ModelAdmin):
    list_display = ['id', 'rule_id', 'get_rule_name', 'status', 'start_time', 'end_time', 'execute_seconds',
                    'execute_sql', 'error_msg']
    list_filter = ['status']
    search_fields = ['rule_id', 'status']

    # 禁用action选项
    actions_on_top = False

    # 禁用编辑链接
    list_display_links = None

    def has_add_permission(self, request):
        # 禁用添加按钮
        return False

    def get_rule_name(self, obj):
        ruleInfo = QualityRule.objects.get(pk=obj.rule_id)
        return ruleInfo.rule_name

    get_rule_name.short_description = '规则名称'


admin.site.register(RuleExecuteLog, RuleExecuteLogdmin)


# hive空间存储情况
class TableStoragedAdmin(admin.ModelAdmin):
    list_display = ['id', 'total_size', 'used_size']

    change_form_template = 'admin/metadata/table_storage.html'

    def changelist_view(self, request, object_id=None, extra_content={}):
        # Entry.objects.order_by('headline')[0]
        storageInfo = TableStorage.objects.order_by('-calculate_date')[0]

        storageInfoTen = TableStorage.objects.order_by('-calculate_date')[0:30]

        lineDataX = []
        lineDataY = []
        for storage in storageInfoTen:
            lineDataX.append(str(storage.calculate_date))
            # 处理单位不一致的情况
            if storage.used_size.find('P') >= 0:
                tmpStorage = storage.used_size.replace('P', '')
                tmpTStorage = float(tmpStorage) * 1024
                lineDataY.append(str(tmpTStorage))
            else:
                lineDataY.append(str(storage.used_size.replace('T', '')))
        # 获取昨日新增存储，近一周平均日增存储，近一月平均日增存储
        sql = '''select 
            t1.id,
            t1.now_day,
            (t1.onedaysago_storage-t1.twodaysago_storage) as yesterday_add,
            (t1.onedaysago_storage-t2.oneweekago_storage)/7 as oneweek_add,
            (t1.onedaysago_storage-t3.onemonthago_storage)/30 as onemonth_add
            from (
                select 
                    id,
                    1 as now_day,
                    sum(case when calculate_date=date(DATE_SUB(now(),INTERVAL 1 day)) then total_storage else 0 end ) as onedaysago_storage,
                    sum(case when calculate_date=date(DATE_SUB(now(),INTERVAL 2 day)) then total_storage else 0 end ) as twodaysago_storage
                from (
                    select 
                    id,
                    1 as now_day,
                    calculate_date,
                    sum(storage) as total_storage
                    from hive_table_capacity
                    where storage_type=2
                    group by calculate_date order by calculate_date desc limit 10
                ) t
            ) t1 left join (
                select 
                    1 as now_day,
                    avg(total_storage) as oneweekago_storage
                    from (
                    select 
                    calculate_date,
                    sum(storage) as total_storage
                    from hive_table_capacity
                    where storage_type=2 and calculate_date>=date(DATE_SUB(now(),INTERVAL 8 day)) and calculate_date<date(DATE_SUB(now(),INTERVAL 1 day))
                    group by calculate_date
                ) oneweek
            ) t2 on t1.now_day=t2.now_day left join (
                select 
                    1 as now_day,
                    avg(total_storage) as onemonthago_storage
                    from (
                    select 
                    calculate_date,
                    sum(storage) as total_storage
                    from hive_table_capacity
                    where storage_type=2 and calculate_date>=date(DATE_SUB(now(),INTERVAL 31 day)) and calculate_date<date(DATE_SUB(now(),INTERVAL 1 day))
                    group by calculate_date
                ) onemonth
            ) t3 on t1.now_day=t3.now_day
        '''
        incStorage = HiveTableCapacity.objects.raw(sql)[0]
        incStorage.yesterday_add = TableStorage.readable_file_size(float(incStorage.yesterday_add), 2)
        incStorage.oneweek_add = TableStorage.readable_file_size(float(incStorage.oneweek_add if incStorage.oneweek_add else 0), 2)
        incStorage.onemonth_add = TableStorage.readable_file_size(float(incStorage.onemonth_add), 2)

        # return HttpResponse(incStorage.yesterday_add)

        extra_content['storage'] = storageInfo
        extra_content['incStorage'] = incStorage
        extra_content['lineDataX'] = ','.join(lineDataX)
        extra_content['lineDataY'] = ','.join(lineDataY)

        return super(TableStoragedAdmin, self).change_view(request, object_id, extra_context=extra_content)


admin.site.register(TableStorage, TableStoragedAdmin)


# 数据表规范
class TableStandardAdmin(admin.ModelAdmin):
    change_form_template = 'admin/metadata/table_standard.html'

    def changelist_view(self, request, object_id=None, extra_content={}):
        return super(TableStandardAdmin, self).change_view(request, object_id, extra_context=extra_content)


admin.site.register(TableStandard, TableStandardAdmin)


# 数据字段规范
class FieldStandardAdmin(admin.ModelAdmin):
    change_form_template = 'admin/metadata/field_standard.html'

    def changelist_view(self, request, object_id=None, extra_content={}):
        return super(FieldStandardAdmin, self).change_view(request, object_id, extra_context=extra_content)


admin.site.register(FieldStandard, FieldStandardAdmin)


# 词根汇总
class WordSummaryAdmin(admin.ModelAdmin):
    change_form_template = 'admin/metadata/word_summary.html'

    def changelist_view(self, request, object_id=None, extra_content={}):
        return super(WordSummaryAdmin, self).change_view(request, object_id, extra_context=extra_content)


admin.site.register(WordSummary, WordSummaryAdmin)


# 质量预警趋势
class QualityTrendAdmin(admin.ModelAdmin):
    change_form_template = 'admin/metadata/quality_trend.html'

    def changelist_view(self, request, object_id=None, extra_content={}):
        start = datetime.datetime.now().strftime("%Y-%m-%d")

        ruleAll = QualityRule.objects.all().count()
        ruleOn = QualityRule.objects.filter(status='on').count()
        warningAll = RuleExecuteLog.objects.filter(status=3, create_time__gt=start).count()
        # storageInfoTen = TableStorage.objects.order_by('-calculate_date')[0:30]

        sql = '''select
                    id,
                    date(create_time) as calculate_date ,
                    count(distinct rule_id) as total,
                    count(distinct case when status=3 then rule_id else null end ) as warning_total
                    from hive_rule_execute_log
                    where create_time>=DATE_SUB(now(), INTERVAL 15 day)
                    group by date(create_time) order by calculate_date desc
                    '''
        results = RuleExecuteLog.objects.raw(sql)

        lineDataX = []
        lineDataY = []
        lineDataY2 = []
        for storage in results:
            lineDataX.append(str(storage.calculate_date))
            lineDataY.append(str(storage.total))
            lineDataY2.append(str(storage.warning_total))

        extra_content['storage'] = {
            'all': ruleAll,
            'on': ruleOn,
            'warning': warningAll
        }
        extra_content['lineDataX'] = ','.join(lineDataX)
        extra_content['lineDataY'] = ','.join(lineDataY)
        extra_content['lineDataY2'] = ','.join(lineDataY2)

        return super(QualityTrendAdmin, self).change_view(request, object_id, extra_context=extra_content)


admin.site.register(QualityTrend, QualityTrendAdmin)


class DictAdmin(admin.ModelAdmin):
    change_form_template = 'admin/metadata/dict.html'

    def changelist_view(self, request, object_id=None, extra_content={}):
        yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

        sql = '''select 
                t1.tag_rely as table_name,
                t1.cnt,
                si.id,
                si.table_content,
                concat('/admin/metadata/detail/?id=',si.id) as url
                from (
                select 
                lower(tag_rely) as tag_rely,
                count(id) cnt
                from makefile_tag_relations_test where source!='azkaban' and tag_rely!='NULL' 
                group by tag_rely order by cnt desc limit 5
                ) t1 left join hive_search_index si on t1.tag_rely=si.table_name and si.is_online=1 and si.db_name!='test'
                 order by t1.cnt desc
            '''
        replyInfo = RuleExecuteLog.objects.raw(sql)

        sql = '''SELECT
            table_name,
            id,
            table_content,
            concat('/admin/metadata/detail/?id=',id) as url,
            table_sort_priority
            from hive_search_index where is_online=1 and db_name!='test' order by table_sort_priority desc limit 5
        '''
        hotInfo = HiveSearchIndex.objects.raw(sql)

        sql = '''select 
            c.tbl_id,
            c.storage,
            t.db_name,
            t.tbl_name as table_name,
            i.id,
            i.table_content,
            concat('/admin/metadata/detail/?id=',i.id) as url
            from (
            select
            tbl_id,
            storage
            from hive_table_capacity where calculate_date='%s' and storage_type=2 order by STORAGE desc limit 5
            ) c left join hive_table_info t on c.tbl_id=t.tbl_id
            left join hive_search_index i on t.tbl_id=i.table_id order by c.storage desc
        ''' % (yesterday)

        diskInfo = HiveTableCapacity.objects.raw(sql)

        extra_content['replyInfo'] = replyInfo
        extra_content['hotInfo'] = hotInfo
        extra_content['diskInfo'] = diskInfo

        return super(DictAdmin, self).change_view(request, object_id, extra_context=extra_content)

admin.site.register(Dict, DictAdmin)


class StorageRankingAdmin(admin.ModelAdmin):
    change_form_template = 'admin/metadata/storage_ranking.html'

    def changelist_view(self, request, object_id=None, extra_content={}):
        yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        thirtyday = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')

        sql = '''
        select 
        t.id,
        t.tbl_id,
        t.total_storage,
        i.db_name,
        i.tbl_name,
        t.tb
        from (
        select id, tbl_id, sum(storage) as total_storage,sum(storage)/(1024*1024*1024*1024) as tb
        from hive_table_capacity
        where storage_type=2 and calculate_date='{yesterday}' group by tbl_id
        ) t left join hive_table_info i on t.tbl_id=i.tbl_id 
        order by t.total_storage desc limit 15
        '''.format(yesterday=yesterday)

        rankInfo = HiveTableCapacity.objects.raw(sql)
        rankList = []
        i = 0
        for value in rankInfo:
            i = i + 1
            value.key = i
            value.format_storage = TableStorage.readable_file_size(float(value.total_storage), 2)
            rankList.append(value)

        sql = '''
            select 
            tbl_id,
            count(tbl_id) cnt,
            count( case when date(create_time)=date(date_sub(now(),INTERVAL 1 day)) then tbl_id else null end) as yesterday_cnt
            from 
            hive_table_info
            where is_online=1
        '''

        tableTotal = HiveTableInfo.objects.raw(sql)

        # return HttpResponse(tableTotal)
        tableDict = {}
        for table in tableTotal:
            tableDict['cnt'] = table.cnt
            tableDict['yesterday_cnt'] = table.yesterday_cnt

        oneMonthDay = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
        sql = '''
            select 
            tbl_id,
            date(create_time) create_date,
            count(tbl_id) cnt
            from hive_table_info
            where create_time>='%s 00:00:00'
            and is_online=1
            group by date(create_time) order by create_date desc
        ''' % (oneMonthDay)

        addTableInfo = HiveTableInfo.objects.raw(sql)

        tableDataX = []
        tableDataY = []
        for storage in addTableInfo:
            tableDataX.append(str(storage.create_date))
            tableDataY.append(str(storage.cnt))

        # 存储趋势
        tenSql = '''
        select 
        t.tbl_id,
        c.id,
        c.calculate_date,
        sum(c.total_storage) as tb,
        sum(c.top10_storage) as top10_tb
        from 
        hive_table_info t 
        left join (
        select c.id,c.calculate_date, c.tbl_id, sum(c.storage) as total_storage,
                sum(case when top10.tbl_id is not null then c.storage else 0 end) as top10_storage
                from hive_table_capacity c left join (
                    select tbl_id, sum(storage) as total_storage
                    from hive_table_capacity
                    where storage_type=2 and calculate_date='{yesterday}' 
                    group by tbl_id order by total_storage desc limit 10
                ) top10 on c.tbl_id=top10.tbl_id
                where storage_type=2 and calculate_date>='{thirtyday}' group by calculate_date, tbl_id
        ) c on t.tbl_id=c.tbl_id where t.is_online=1 and c.id is not null
        group by c.calculate_date order by c.calculate_date desc
        '''.format(yesterday=yesterday, thirtyday=thirtyday)
        storageInfoTen = TableStorage.objects.raw(tenSql)

        lineDataX = []
        lineDataY = []
        lineDataZ = []
        storageUnit = ''
        for storage in storageInfoTen:
            lineDataX.append(str(storage.calculate_date))
            formatStorageTb = TableStorage.readable_file_size_list(storage.tb)
            lineDataY.append(str(formatStorageTb[0]))
            formatStorageTop = TableStorage.readable_file_size_list(storage.top10_tb)
            lineDataZ.append(str(formatStorageTop[0]))

            storageUnit = formatStorageTb[1]

        extra_content['lineDataX'] = ','.join(lineDataX)
        extra_content['lineDataY'] = ','.join(lineDataY)
        extra_content['lineDataZ'] = ','.join(lineDataZ)

        extra_content['tableDataX'] = ','.join(tableDataX)
        extra_content['tableDataY'] = ','.join(tableDataY)

        extra_content['table_dict'] = tableDict
        extra_content['rank_list'] = rankList
        extra_content['unit'] = storageUnit

        return super(StorageRankingAdmin, self).change_view(request, object_id, extra_context=extra_content)

admin.site.register(StorageRanking, StorageRankingAdmin)


class HiveTableCapacityAdmin(admin.ModelAdmin):
    list_display = ['tbl_id', 'get_table_name', 'get_format_storage', ]
    # search_fields = ['tbl_id']

    list_per_page = 50

    list_display_links = None

    def has_add_permission(self, request):
        # 禁用添加按钮
        return False

    def has_delete_permission(self, request, obj=None):
        # 禁用删除按钮
        return False

    def get_queryset(self, request):
        yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        return HiveTableCapacity.objects.all().filter(calculate_date=yesterday, storage_type=2).order_by('-storage')

    def get_table_name(self, obj):
        tableInfo = HiveTableInfo.objects.get(pk=obj.tbl_id)

        return "%s.%s" % (tableInfo.db_name, tableInfo.tbl_name)

    def get_format_storage(self, obj):
        return TableStorage.readable_file_size(obj.storage, 2)

    get_format_storage.short_description = '占用空间'

    get_table_name.short_description = '表名称'


admin.site.register(HiveTableCapacity, HiveTableCapacityAdmin)

# 用户资产信息
class UserStorageAdmin(admin.ModelAdmin):
    change_form_template = 'admin/metadata/user_storage.html'

    def changelist_view(self, request, object_id=None, extra_content={}):
        yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        fiftendaysAgo = (datetime.datetime.now() - datetime.timedelta(days=15)).strftime('%Y-%m-%d')

        tbl_owner = request.GET['tbl_owner'].strip() if 'tbl_owner' in request.GET else 'all'
        if tbl_owner != 'all':
            ownerWhereStr = " and tbl_owner= '%s'" % (tbl_owner)
        else:
            ownerWhereStr = ""

        org_id = int(request.GET['org_id']) if 'org_id' in request.GET else -1
        if org_id != -1:
            orgWhere = " and org_id= '%s'" % (org_id)
        else:
            orgWhere = ""

        orgInfo = HiveOrgInfo.objects.all()

        # 选择集群用户
        if ownerWhereStr:
            sql = '''
                    select 
                    tbl_id,
                    count(tbl_id) cnt,
                    count( case when date(create_time)=date(date_sub(now(),INTERVAL 1 day)) then tbl_id else null end) as yesterday_cnt
                    from 
                    hive_table_info
                    where is_online=1 {ownerWhereStr}
                    '''.format(ownerWhereStr=ownerWhereStr)
        else:
            # 选择组织
            if orgWhere:
                sql = '''
                select 
                tbl_id,
                count(tbl_id) cnt,
                count( case when date(t.create_time)=date(date_sub(now(),INTERVAL 1 day)) then tbl_id else null end) as yesterday_cnt
                from 
                hive_table_info t
                left join hive_owner_org oo on t.tbl_owner=oo.owner_name
                where is_online= 1 {orgWhere}
                '''.format(orgWhere=orgWhere)
            # 集群用户和组织都为空
            else:
                sql = '''
                select 
                    tbl_id,
                    count(tbl_id) cnt,
                    count( case when date(create_time)=date(date_sub(now(),INTERVAL 1 day)) then tbl_id else null end) as yesterday_cnt
                    from 
                    hive_table_info
                    where is_online=1
                '''
        # return HttpResponse(sql)
        tableTotal = HiveTableInfo.objects.raw(sql)

        tableDict = {}
        for table in tableTotal:
            tableDict['cnt'] = table.cnt
            tableDict['yesterday_cnt'] = table.yesterday_cnt

        # 获取所有的owner
        ownerSql = '''
        select id,owner_name as tbl_owner,org_id
        from hive_owner_org
        where 1=1 {ownerWhere}
        '''.format(ownerWhere=orgWhere)
        ownerInfo = HiveOwnerOrg.objects.raw(ownerSql)

        # 获取空间大小
        if ownerWhereStr:
            capacitySql = '''
                select 
                t.tbl_id,
                c.calculate_date,
                sum(c.total_storage) as total_storage
                from 
                hive_table_info t 
                left join (
                select id,calculate_date, tbl_id, sum(storage) as total_storage
                        from hive_table_capacity
                        where storage_type=2 and calculate_date>='{fiftendays}' group by calculate_date, tbl_id
                ) c on t.tbl_id=c.tbl_id where t.is_online=1 and c.calculate_date is not null {whereStr} 
                group by c.calculate_date order by c.calculate_date desc
            '''.format(whereStr=ownerWhereStr, fiftendays=fiftendaysAgo)
        else:
            if orgWhere:
                capacitySql = '''
                    select 
                    t.tbl_id,
                    c.calculate_date,
                    sum(c.total_storage) as total_storage
                    from 
                    hive_table_info t 
                    left join (
                    select id,calculate_date, tbl_id, sum(storage) as total_storage
                            from hive_table_capacity
                            where storage_type=2 and calculate_date>='{fiftendays}' group by calculate_date, tbl_id
                    ) c on t.tbl_id=c.tbl_id 
                    left join hive_owner_org oo on t.tbl_owner=oo.owner_name
                    where t.is_online=1 and c.calculate_date is not null {orgWhere}
                    group by c.calculate_date order by c.calculate_date desc
                '''.format(orgWhere=orgWhere, fiftendays=fiftendaysAgo)
            else:
                capacitySql = '''
                    select 
                    t.tbl_id,
                    c.calculate_date,
                    sum(c.total_storage) as total_storage
                    from 
                    hive_table_info t 
                    left join (
                    select id,calculate_date, tbl_id, sum(storage) as total_storage
                            from hive_table_capacity
                            where storage_type=2 and calculate_date>='{fiftendays}' group by calculate_date, tbl_id
                    ) c on t.tbl_id=c.tbl_id where t.is_online=1 and c.calculate_date is not null 
                    group by c.calculate_date order by c.calculate_date desc
                '''.format(fiftendays=fiftendaysAgo)

        # return HttpResponse(capacitySql)
        storageInfo = HiveTableInfo.objects.raw(capacitySql)

        lineDataX = []
        lineDataY = []
        storageUnit = ''
        flag = 1
        totalStorage = ''
        for storage in storageInfo:
            lineDataX.append(str(storage.calculate_date))
            formatStorage = TableStorage.readable_file_size_list(storage.total_storage)
            storageUnit = formatStorage[1]
            lineDataY.append(str(formatStorage[0]))
            if flag == 1:
                totalStorage = "%s %s" % (str(formatStorage[0]), formatStorage[1])
            flag = flag + 1

        extra_content['lineDataX'] = ','.join(lineDataX)
        extra_content['lineDataY'] = ','.join(lineDataY)
        extra_content['unit'] = storageUnit

        extra_content['table_total'] = tableDict
        extra_content['owner_info'] = ownerInfo
        extra_content['tbl_owner'] = tbl_owner
        extra_content['org_id'] = org_id
        extra_content['user_storage'] = totalStorage
        extra_content['org_info'] = orgInfo

        return super(UserStorageAdmin, self).change_view(request, object_id, extra_context=extra_content)

admin.site.register(UserStorage, UserStorageAdmin)


class HiveOrgInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'create_time', 'update_time']
    search_fields = ['name']

    list_per_page = 50

admin.site.register(HiveOrgInfo, HiveOrgInfoAdmin)


class HiveOwnerOrgAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner_name', 'org_id', 'create_time', 'update_time']
    search_fields = ['owner_name']

    list_per_page = 50


admin.site.register(HiveOwnerOrg, HiveOwnerOrgAdmin)


class UserOrgTableAdmin(admin.ModelAdmin):
    change_form_template = 'admin/metadata/user_org_table.html'

    def getPageRange(self, paginator, page):
        page = int(page)
        # 页数小于6
        newPageinator = []
        if paginator.num_pages <= 6:
            newPageinator = range(1, 6)
        else:
            # 判断当前页的位置
            if page <= 2:
                newPageinator = range(1, 6)
            elif page >= int(paginator.num_pages) - 1:
                newPageinator = range(int(paginator.num_pages) - 6, int(paginator.num_pages))
            else:
                newPageinator = [page - 2, page - 1, page, page + 1, page + 2]

        return newPageinator

    def changelist_view(self, request, object_id=None, extra_content={}):
        yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

        tbl_owner = request.GET['tbl_owner'].strip() if 'tbl_owner' in request.GET else 'all'
        if tbl_owner != 'all':
            ownerWhereStr = " and tbl_owner= '%s'" % (tbl_owner)
        else:
            ownerWhereStr = ""

        table_name = request.GET['table_name'].strip() if 'table_name' in request.GET else ''
        if table_name != '':
            tableWhereStr = " and tbl_name like '%%{table_name}%%' ".format(table_name=table_name)
        else:
            tableWhereStr = ""

        sql = '''select c.id, c.tbl_id, sum(c.storage) as total_storage,i.db_name,i.tbl_name,tbl_owner
from hive_table_capacity c
left join hive_table_info i on c.tbl_id=i.tbl_id
where c.storage_type=2 and c.calculate_date='{yesterday}' {ownerWhere} {tableWhereStr}
group by c.tbl_id order by total_storage desc '''.format(ownerWhere=ownerWhereStr, tableWhereStr=tableWhereStr,
                                                         yesterday=yesterday)
        contact_list = HiveTableCapacity.objects.raw(sql)

        for contact in contact_list:
            formatStorage = TableStorage.readable_file_size(float(contact.total_storage), 2)
            contact.format_storage = formatStorage

        paginator = Paginator(contact_list, 20)  # Show 25 contacts per page
        totalCount = paginator.count

        page = request.GET.get('page') if request.GET.get('page') else 1

        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = paginator.page(paginator.num_pages)

        # return HttpResponse(contacts.count)

        # 获取所有的owner
        ownerSql = '''
        select id,owner_name as tbl_owner,org_id
        from hive_owner_org
        where 1=1 
        '''
        ownerInfo = HiveOwnerOrg.objects.raw(ownerSql)

        # return HttpResponse(paginator.page_range)

        extra_content['owner_info'] = ownerInfo
        extra_content['storage_info'] = contacts
        extra_content['tbl_owner'] = tbl_owner
        extra_content['table_name'] = table_name
        extra_content['totalCount'] = totalCount
        extra_content['paginator'] = paginator
        extra_content['page'] = int(page)
        extra_content['page_range'] = self.getPageRange(paginator, page)

        return super(UserOrgTableAdmin, self).change_view(request, object_id, extra_context=extra_content)


admin.site.register(UserOrgTable, UserOrgTableAdmin)
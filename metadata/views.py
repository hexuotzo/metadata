# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from io import BytesIO
import json
import xlwt
import datetime
from django.forms import model_to_dict
from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.db.models import Sum, Q, Count
from django.urls import reverse
from django.http import HttpResponseRedirect
import logging
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

from metadata.models import MdColumnBasicInfo,PccVehicleInfo,PccUpgradeDetail,PccProblemDetail,PccDepotName,HiveTableColumnInfo,HiveColumnMaintain,HiveTableInfo,MakefileTagRelations
from metadata.models import HiveSearchIndex,HiveTableMaintain,HiveSearchLog,RuleExecuteLog

def search_basic_column_info(request):
    key = request.GET.get('q')

    items = MdColumnBasicInfo.objects.filter(
        Q(column_id__contains=key)|Q(column_name__contains=key)|Q(table_name__contains=key))
    items = items.filter(online_status='在线')[:100]


    res = []

    for i in items:
        res.append({'id': i.format_tablecolumn(), 'name': i.format_tablecolumn()})

    return JsonResponse({
        'items': res,
        'total_page': 1,
    })


def download_excel(request,data, field, data_field, name):
    # 设置HTTPResponse的类型
    response = HttpResponse(content_type='application/vnd.ms-excel')

    content_type = u'attachment;filename=%s.xls' % name
    if request.META['HTTP_USER_AGENT'].find('Windows') > -1:
        content_type = content_type.encode('cp936', 'ignore')
    else:
        content_type = content_type.encode('utf-8', 'ignore')
    response['Content-Disposition'] = content_type

    # 创建一个文件对象
    wb = xlwt.Workbook(encoding='utf8')
    # 创建一个sheet对象
    sheet = wb.add_sheet('sheet0')

    # 写入文件标题
    i = 0
    for k in field:
        sheet.write(0, i, k)
        i += 1
    # 写入数据
    j = 1

    for val in data:
        k = 0
        for attr in data_field:
            sheet.write(j, k, val[attr])
            k += 1
        j += 1
    # 写出到IO
    output = BytesIO()
    wb.save(output)
    # 重新定位到开始
    output.seek(0)

    response.write(output.getvalue())
    return response


def pcc_vehicle_export_excel(request):
    """
    导出PCC车辆信息
    :param request:
    :return:
    """
    field = ["车厂", "设备类型", "安装类型", "车牌号", "发动机型号", "变速箱型号", "变速箱类型", "前装sim卡号", "后装sim卡号", "前装vid", "后装vid",
             "AdasisTbox-SN", "AdasisTbox-ID ", "车型",
             "底盘号", "安装时间", "设备是否拆除", "拆除时间", "安装版本号", "车辆归属人", "归属人名字", "归属人联系方式", "驾驶员的驾驶习惯", "车速浮动区间", "其他备注"]
    data = PccVehicleInfo.objects.all()
    excel_data = []
    for val in data:
        list_data = {
            "depot": val.depot.depot_name,
            "device_type": val.get_device_type_display(),
            "install_type": val.get_install_type_display(),
            "car_number": val.car_number,
            "engine_model": val.engine_model,
            "trans_model": val.trans_model,
            "trans_type": val.get_trans_type_display(),
            "front_sim": val.front_sim,
            "behind_sim": val.behind_sim,
            "front_vid": val.front_vid,
            "behind_vid": val.behind_vid,
            "at_sn": val.at_sn,
            "at_id": val.at_id,
            "car_model": val.car_model,
            "car_owner": val.get_car_owner_display(),
            "chassis_number": val.chassis_number,
            "install_time": None if val.install_time is None else val.install_time.strftime("%Y-%m-%d %H:%M:%S"),
            "device_remove_status": val.get_device_remove_status_display(),
            "device_remove_time": None if val.device_remove_time is None else val.device_remove_time.strftime("%Y-%m-%d %H:%M:%S"),
            "install_verion": val.install_verion,
            "driver_name": val.driver_name,
            "driver_phone": val.driver_phone,
            "driver_habit": val.get_driver_habit_display(),
            "speed_range": val.speed_range,
            "other_remark": val.other_remark,
        }
        excel_data.append(list_data)

    data_field = ['depot', 'device_type', 'install_type', 'car_number', 'engine_model', 'trans_model', 'trans_type',
                  'front_sim', 'behind_sim', 'front_vid', 'behind_vid', 'at_sn', 'at_id', 'car_model', 'chassis_number',
                  'install_time', 'device_remove_status', 'device_remove_time', 'install_verion', 'car_owner',
                  'driver_name',
                  'driver_phone', 'driver_habit', 'speed_range', 'other_remark']
    return download_excel(request,excel_data, field, data_field, u'pcc车辆信息')


def pcc_upgrade_export_excel(request):
    """
    导出PCC更新明细
    :param request:
    :return:
    """
    field = ["升级设备", "后装vid", "前装vid", "底盘号", "升级时间", "升级版本", "其他备注"]
    data = PccUpgradeDetail.objects.all()
    excel_data = []
    for val in data:
        list_data = {
            "upgrade_device": val.get_upgrade_device_display(),
            "behind_vid": val.behind_vid,
            "front_vid": val.front_vid,
            "chassis_number": val.chassis_number,
            "upgrade_time": None if val.upgrade_time is None else val.upgrade_time.strftime("%Y-%m-%d %H:%M:%S"),
            "upgrade_version": val.upgrade_version,
            "other_remark": val.other_remark
        }
        excel_data.append(list_data)
    data_field = ["upgrade_device", "behind_vid", "front_vid", "chassis_number", "upgrade_time", "upgrade_version",
                  "other_remark"]
    return download_excel(request,excel_data, field, data_field, u'pcc升级明细')


def pcc_problem_export_excel(request):
    """
    导出PCC问题明细
    :param request:
    :return:
    """
    field = ["问题设备", "问题车辆后装vid", "问题车辆前装vid", "问题车辆底盘号", "问题描述", "解决办法", "状态"]
    data = PccProblemDetail.objects.all()
    excel_data = []
    for val in data:
        list_data = {
            "device_type": val.get_device_type_display(),
            "behind_vid": val.behind_vid,
            "front_vid": val.front_vid,
            "chassis_number": val.chassis_number,
            "problem_describe": val.problem_describe,
            "problem_solution": val.problem_solution,
            "status": val.get_status_display()
        }
        excel_data.append(list_data)
    data_field = ["device_type", "behind_vid", "front_vid", "chassis_number", "problem_describe", "problem_solution",
                  "status"]
    return download_excel(request,excel_data, field, data_field, u'pcc问题明细')


def pcc_depot_export_excel(request):
    """
    导出PCC车厂明细
    :param request:
    :return:
    """
    field = ["车厂"]
    data = PccDepotName.objects.all()
    excel_data = []
    for val in data:
        list_data = {
            "depot_name": val.depot_name,
        }
        excel_data.append(list_data)
    data_field = ["depot_name"]
    return download_excel(request,excel_data, field, data_field, u'pcc车厂列表')

def column_list(request):
    tbl_id = request.GET['id']
    sql = '''select 
    t2.id,
t1.table_name,
t1.column_name,
t1.column_type,
t1.column_desc,
t2.column_idx,
t2.column_desc_maintain
from hive_table_column_info t1 
inner join 
hive_column_maintain t2 
on t1.db_name=t2.db_name and t1.table_name=t2.table_name and t1.integer_idx=t2.column_idx
where t1.tbl_id='%s' order by t2.column_idx
    ''' % (tbl_id)
    results = HiveTableColumnInfo.objects.raw(sql)

    tableInfo = HiveTableInfo.objects.get(pk=tbl_id)

    # results = Contact.objects.all()
    # for i in results:
    #     print(i['age'])
    return render(request,"admin/column_list.html",{"results":results,"tbl_id":tbl_id,"table_info":tableInfo})

def column_edit(request):

    id = request.POST.getlist('idArr[]')
    column = request.POST.getlist('columnArr[]')
    tbl_id = request.POST['tbl_id']

    idStr = ''
    for i, val in enumerate(id):
        if column[i] is not None or column[i] != '':
            result = HiveColumnMaintain.objects.filter(pk=id[i]).update(column_desc_maintain=column[i])
            #idStr += str(id[i]) +':' + str(column[i]) + ','
    #更新字典表里面的值
    columnStr = ','.join(column)
    HiveSearchIndex.objects.filter(table_id=tbl_id).update(column_content=columnStr)

    #messages.info("/admin/metadata/hivetablecolumninfo/?id=%s" % (tbl_id), "修改成功")
    #HttpResponse("<script>alert('ok');</script>")
    return HttpResponseRedirect("/admin/metadata/hivetablecolumninfo/?id=%s" % (tbl_id))

# 表的依赖关系
def table_dependency(request):
    sql = '''
        SELECT
        tag_rely as id,
        tag_rely as label,
        'success' as status,
        tag as target
        from 
        makefile_tag_relations_test
        where tag='{table_name}'
        group by tag,tag_rely
        union all 
        select 
        '{table_name}' as id,
        '{table_name}' as label,
        'success' as status,
        '' as target
    ''' .format(table_name='dwd_lc_trackdwStatus_phi')
    tagResult = MakefileTagRelations.objects.raw(sql)
    tarDict = {}
    key=0
    for value in tagResult:
        key=key+1
        newDict = {
            'id' : value.id,
            'label' : value.label,
            'status' : value.status,
            'target' : value.target,
        }
        tarDict[key] = newDict

    replyJson = json.dumps(tarDict)

    return render(request,"admin/table_dependency.html",{'dependArr':replyJson})

# 表的依赖关系
def t_search(request):
    searchKey = ''
    if len(request.GET) >0 :
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
            SELECT
            id,db_id,db_name,table_id,table_name,column_names,table_content,column_content
            from 
            hive_search_index
            where  is_online=1
            order by table_sort_priority desc 
            limit 100
        '''.format(searchKey=searchKey)

    #return HttpResponse(sql)
    tableResult = HiveSearchIndex.objects.raw(sql)
    resultDict = []
    key = 0
    searchIndex = HiveSearchIndex()
    if tableResult:
        for result in tableResult:
            key = key + 1
            column_content = searchIndex.getSubstrString(result.column_content,searchKey)
            #column_content = result.column_content
            column_names = searchIndex.getSubstrString(result.column_names,searchKey)
            #column_names = result.column_names

            newDict = {
                'url': '/hive/detail?id=%s' % (result.id),
                'id':result.id,
                'db_name': result.db_name,
                'table_name': result.table_name.replace(searchKey,"<font color='red'>%s</font>"%(searchKey)),
                'table_content' : result.table_content.replace(searchKey,"<font color='red'>%s</font>"%(searchKey)),
                'column_content' : column_content.replace(searchKey,"<font color='red'>%s</font>"%(searchKey)),
                'column_names' : column_names.replace(searchKey,"<font color='red'>%s</font>"%(searchKey)),
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

    return render(request,"admin/t_search_new.html",{'tableResult':resultDict,'searchKey':searchKey,'contacts':contacts})

# hive 表详情
def t_detail(request):

    id = 0
    #return HttpResponse(request.GET)
    if 'id' in request.GET:
        id = request.GET['id']
    if id:
        searchIndexInfo = HiveSearchIndex.objects.get(pk=id)
    else:
        try:
            db_name = request.GET['db_name'].strip().lower()
            tbl_name = request.GET['table_name'].strip().lower()
            searchIndexInfo = HiveSearchIndex.objects.get(db_name=db_name,table_name=tbl_name,is_online=1)
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

    maintainInfo = HiveTableMaintain.objects.get(db_name=searchIndexInfo.db_name, table_name=searchIndexInfo.table_name)

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
    ''' .format(table_name=searchIndexInfo.table_name)

    #return HttpResponse(sql)
    tagResult = MakefileTagRelations.objects.raw(sql)
    tarDict = {}
    key=0
    for value in tagResult:
        key=key+1
        newDict = {
            'id' : value.id,
            'label' : value.label,
            'status' : value.status,
            'target' : value.target,
        }
        tarDict[key] = newDict

    replyJson = json.dumps(tarDict)

    # 插入记录数据
    addDict = {
        'index_id' : id,
        'db_name' : searchIndexInfo.db_name,
        'table_name' : searchIndexInfo.table_name,
        'author_id' : 0,
        'create_time' : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    HiveSearchLog.objects.create(**addDict)
    #return HttpResponse(tableInfo)
    return render(request,"admin/t_detail.html",{'indexInfo':searchIndexInfo,'tableInfo':tableInfo,'columnResult':columnResult,'maintainInfo':maintainInfo,'dependArr':replyJson})

# ajax根据数据库名获取表名
def get_table_name(request):
    db_name = request.GET['db_name']
    table_result = HiveTableInfo.objects.filter(db_name=db_name)

    table_list = []

    for table in table_result:
        table_row = {}
        table_row['table_name'] = table.tbl_name
        table_row['table_id'] = table.tbl_id
        table_list.append(table_row)

    return JsonResponse({
        'success':'ok',
        'data':table_list
    })

# ajax 获取表的列名
def get_column_name(request):
    db_name = request.GET['db_name']
    table_name = request.GET['table_name']

    column_result = HiveTableColumnInfo.objects.filter(db_name=db_name,table_name=table_name).order_by('integer_idx')

    column_list = []
    for column in column_result:
        column_row = {}
        column_row['column_name'] = column.column_name
        column_row['column_id'] = column.column_id
        column_list.append(column_row)

    return JsonResponse({
        'success':'ok',
        'db_name':db_name,
        'table_name': table_name,
        'data':column_list
    })

def rule_execute_now(request):
    rule_id = request.POST['rule_id']

    #判断该条规则当天是否已经存在了
    ruleRow = RuleExecuteLog.objects.filter(rule_id=rule_id,status=0)
    if ruleRow:
        return JsonResponse({
            'success': 'ok',
            'msg': '规则已存在',
        })
    else:
        insertDict = {
                    'rule_id' : rule_id,
                    'status' : 0,
                    'error_msg' : '',
                    'start_time' : '1971-01-01 01:00:00',
                    'end_time' : '1971-01-01 01:00:00',
                    'execute_seconds' : 0,
                    'execute_sql' : '',
                    'create_time' : datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }

        RuleExecuteLog.objects.create(**insertDict)
        return JsonResponse({
            'success': 'ok',
            'msg': '已加入执行计划',
        })









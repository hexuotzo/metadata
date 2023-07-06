# -*- coding: utf-8 -*-

import json

from django.http.response import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from django.views.decorators.http import require_POST
from django.contrib.auth.models import Group
from django.db import IntegrityError
from django.contrib.auth.decorators import permission_required
from django.contrib.admin.models import ADDITION, CHANGE, DELETION

from common.logentry import logwrite
from usertags.models import (
    FirstCategory, SecondCategory, ThirdCategory,
    Tags, TagsItems, TagElasticsearchTask)
from usertags.utils import is_json
from usertags.params import CATEGORY_STAT
    

@require_POST
@permission_required('usertags.edit_category', raise_exception=True)
def cate1st_edit(request):
    if not request.user.is_authenticated():
        return JsonResponse({'code': 2, 'msg': '登陆信息过期, 请重新登陆'})

    k = request.POST.get('catepk')
    name = request.POST.get('catename')
    ename = request.POST.get('cateename')
    desc = request.POST.get('catedesc')
    
    if not name:
        return JsonResponse({'code': 3, 'msg': '名称不能为空'})
    
    if k:
        try:
            f = FirstCategory.objects.get(pk=int(k))
            log_action = CHANGE
        except ObjectDoesNotExist:
            f = FirstCategory()
            f.creator = request.user
            log_action = ADDITION
    else:
        f = FirstCategory()
        f.creator = request.user
        log_action = ADDITION

    f.name = name
    f.ename = ename
    f.desc = desc
    f.save()

    logwrite(request, 7, f, log_action)

    return JsonResponse({'code': 0, 'msg': '更新成功'})


@require_POST
@permission_required('usertags.edit_category', raise_exception=True)
def cate2st_edit(request):
    if not request.user.is_authenticated():
        return JsonResponse({'code': 2, 'msg': '登陆信息过期, 请重新登陆'})

    k = request.POST.get('catepk')
    firstcate = request.POST.get('firstcate')
    name = request.POST.get('catename')
    ename = request.POST.get('cateename')
    desc = request.POST.get('catedesc')
    
    if not name:
        return JsonResponse({'code': 3, 'msg': '名称不能为空'})
    
    if not k and not firstcate:
        return JsonResponse({'code': 5, 'msg': '一级类目不能为空'})
    
    if k:
        try:
            f = SecondCategory.objects.get(pk=int(k))
            log_action = CHANGE
        except ObjectDoesNotExist:
            return JsonResponse({'code': 6, 'msg': '二级类目数据错误, 查无此类目'})
    else:
        f = SecondCategory()
        f.creator = request.user
        log_action = ADDITION
        
        try:
            firstcategory = FirstCategory.objects.get(pk=int(firstcate))
        except ObjectDoesNotExist:
            return JsonResponse({'code': 7, 'msg': '一级类目数据错误, 查无此类目'})
        
        f.first_category = firstcategory
    
    f.name = name
    f.ename = ename
    f.desc = desc
    f.save()

    logwrite(request, 8, f, log_action)
    
    return JsonResponse({'code': 0, 'msg': '更新成功'})


@require_POST
@permission_required('is_superuser', raise_exception=True)
def cate2st_setstat(request):
    stat = request.POST.get('stat')
    k = request.POST.get('pk')

    if not request.user.is_authenticated():
        return JsonResponse({'code': 2, 'msg': '登陆信息过期, 请重新登陆'})

    try:
        f = SecondCategory.objects.get(pk=int(k))
    except ObjectDoesNotExist:
        return JsonResponse({'code': 6, 'msg': '数据异常,请刷新页面重试'})

    f.stat = stat
    f.save()

    logwrite(request, 7, f, CHANGE)

    return JsonResponse({'code': 0, 'msg': '更新成功'})


@require_POST
@permission_required('usertags.edit_category', raise_exception=True)
def cate3rd_edit(request):
    if not request.user.is_authenticated():
        return JsonResponse({'code': 2, 'msg': '登陆信息过期, 请重新登陆'})

    k = request.POST.get('catepk')
    secondcate = request.POST.get('secondcate')
    name = request.POST.get('catename')
    desc = request.POST.get('catedesc')

    if not name:
        return JsonResponse({'code': 3, 'msg': '名称不能为空'})

    if k:
        try:
            f = ThirdCategory.objects.get(pk=int(k))
            log_action = CHANGE
        except ObjectDoesNotExist:
            return JsonResponse({'code': 6, 'msg': '数据错误, 查无此类目'})
    else:
        if not secondcate:
            return JsonResponse({'code': 5, 'msg': '类目不能为空'})

        f = ThirdCategory()
        f.creator = request.user
        log_action = ADDITION

        try:
            secondcategory = SecondCategory.objects.get(pk=int(secondcate))
        except ObjectDoesNotExist:
            return JsonResponse({'code': 7, 'msg': '二级类目数据错误, 查无此类目'})

        f.second_category = secondcategory

    f.name = name
    f.desc = desc
    f.save()

    logwrite(request, 9, f, log_action)
    
    return JsonResponse({'code': 0, 'msg': '更新成功'})


@require_POST
@permission_required('is_superuser', raise_exception=True)
def cate3rd_setstat(request):
    stat = request.POST.get('stat')
    k = request.POST.get('pk')
    
    if not request.user.is_authenticated():
        return JsonResponse({'code': 2, 'msg': '登陆信息过期, 请重新登陆'})
    
    try:
        f = ThirdCategory.objects.get(pk=int(k))
    except ObjectDoesNotExist:
        return JsonResponse({'code': 6, 'msg': '数据异常,请刷新页面重试'})
    
    f.stat = stat
    f.save()

    logwrite(request, 9, f, CHANGE)

    return JsonResponse({'code': 0, 'msg': '更新成功'})
    
    
@require_POST
@permission_required('usertags.edit_usertags_tags', raise_exception=True)
def usertag_edit(request):
    if not request.user.is_authenticated():
        return JsonResponse({'code': 2, 'msg': '登陆信息过期, 请重新登陆'})

    k = request.POST.get('tagpk')
    category = request.POST.get('tagcate')
    name = request.POST.get('tagname')
    ename = request.POST.get('tagename')
    desc = request.POST.get('tagdesc')
    validate = request.POST.get('validate')
    valtype = request.POST.get('valtype')
    freq = request.POST.get('freq')
    groupauth = request.POST.get('group_auth', '[]')
    groupauth = [int(i) for i in json.loads(groupauth)]

    if not name:
        return JsonResponse({'code': 3, 'msg': '名称不允许为空'})
 
    if not validate:
        return JsonResponse({'code': 8, 'msg': '有效期不允许为空'})

    if not freq:
        return JsonResponse({'code': 9, 'msg': '更新频次不允许为空'})

    if not k and not valtype:
        return JsonResponse({'code': 10, 'msg': '标签值类型不允许为空'})

    if k:
        try:
            f = Tags.objects.get(pk=int(k))
            log_action = CHANGE
        except ObjectDoesNotExist:
            return JsonResponse({'code': 6, 'msg': '数据错误, 查无此类目'})
    else:
        if not category:
            return JsonResponse({'code': 5, 'msg': '类目不允许为空'})

        f = Tags()
        f.creator = request.user
        f.valtype = valtype
        log_action = ADDITION

        try:
            category = SecondCategory.objects.get(pk=int(category))
        except ObjectDoesNotExist:
            return JsonResponse({'code': 7, 'msg': '类目数据错误, 查无此类目'})

        f.category = category
        f.fcategory_id = category.first_category.pk

    f.name = name
    f.ename = ename
    f.desc = desc
    f.validdays = validate
    f.freq = freq
    try:
        f.save()
    except IntegrityError:
        return JsonResponse({'code': 8, 'msg': '标签英文名已存在, 不可重复'})

    # 设置角色权限
    for g in Group.objects.all():
        group_auth_tags = g.permusertags_set.get_or_create(group=g)[0]
        if g.id in groupauth:
            group_auth_tags.tags.add(f)
        else:
            group_auth_tags.tags.remove(f)
    
    logwrite(request, 11, f, log_action)

    return JsonResponse({'code': 0, 'msg': '更新成功'})


@require_POST
@permission_required('is_superuser', raise_exception=True)
def usertag_setstat(request):
    stat = request.POST.get('stat')
    k = request.POST.get('pk')

    if not request.user.is_authenticated():
        return JsonResponse({'code': 2, 'msg': '登陆信息过期, 请重新登陆'})

    try:
        f = Tags.objects.get(pk=int(k))
    except ObjectDoesNotExist:
        return JsonResponse({'code': 6, 'msg': '数据异常,请刷新页面重试'})

    f.stat = stat
    f.save()

    logwrite(request, 11, f, CHANGE)

    return JsonResponse({'code': 0, 'msg': '更新成功'})
    

@require_POST
@permission_required('usertags.edit_usertags_tagsitems', raise_exception=True)
def usertagitem_edit(request):
    if not request.user.is_authenticated():
        return JsonResponse({'code': 2, 'msg': '登陆信息过期, 请重新登陆'})

    k = request.POST.get('tagitemid')
    tagid = request.POST.get('tagid')
    name = request.POST.get('tagname')
    desc = request.POST.get('tagdesc')
    source_desc = request.POST.get('source_desc', '')
    define_desc = request.POST.get('define_desc', '')
    
    
    if not name:
        return JsonResponse({'code': 3, 'msg': '名称不能为空'})
    
    if not k and not tagid:
        return JsonResponse({'code': 4, 'msg': '数据异常,请刷新后重试'})
    
    if k:
        try:
            f = TagsItems.objects.get(pk=int(k))
            log_action = CHANGE
        except ObjectDoesNotExist:
            return JsonResponse({'code': 6, 'msg': '数据错误, 查无此类目'})
    else:
        f = TagsItems()
        f.creator = request.user
        log_action = ADDITION
        
        try:
            tagobj = Tags.objects.get(pk=int(tagid))
        except ObjectDoesNotExist:
            return JsonResponse({'code': 7, 'msg': '类目数据错误, 查无此类目'})

        f.tag = tagobj
    
    f.name = name
    f.desc = desc
    f.source_desc = source_desc
    f.define_desc = define_desc
    f.save()

    logwrite(request, 10, f, log_action)
    
    return JsonResponse({'code': 0, 'msg': '更新成功'})


@require_POST
@permission_required('is_superuser', raise_exception=True)
def usertagitem_setstat(request):
    stat = request.POST.get('stat')
    k = request.POST.get('pk')
    
    if not request.user.is_authenticated():
        return JsonResponse({'code': 2, 'msg': '登陆信息过期, 请重新登陆'})
    
    try:
        f = TagsItems.objects.get(pk=int(k))
    except ObjectDoesNotExist:
        return JsonResponse({'code': 6, 'msg': '数据异常,请刷新页面重试'})
    
    f.stat = stat
    f.save()

    logwrite(request, 10, f, CHANGE)

    return JsonResponse({'code': 0, 'msg': '更新成功'})
    

@require_POST
def usertag_anas_add(request):
    '''
    用户画像统计创建任务
    '''
    
    if not request.user.is_authenticated():
        return JsonResponse({'code': 2, 'msg': '登陆信息过期, 请重新登陆'})
        
    name = request.POST.get('name')
    client = request.POST.get('client')
    charttype = request.POST.get('charttype')
    querybd = request.POST.get('querybd')
    dimbd = request.POST.get('dimbd')
    
    if not name:
        return JsonResponse({'code': 3, 'msg': '任务名称不能为空'})
        
    if not client:
        return JsonResponse({'code': 4, 'msg': '客户端不能为空'})
    if not querybd or not is_json(querybd):
        return JsonResponse({'code': 5, 'msg': '筛选条件设置错误'})
    if not dimbd or not is_json(dimbd):
        return JsonResponse({'code': 6, 'msg': '分析维度设置错误'})

    t = TagElasticsearchTask()
    t.name = name
    t.client_id = client
    t.query = querybd
    t.dimention = dimbd
    t.charttype = charttype
    t.creator = request.user
    t.save()

    logwrite(request, 17, t, ADDITION)

    return JsonResponse({'code': 0, 'msg': 'success', 'itemid': t.pk})


@require_POST
def usertag_anas_setstat(request):
    stat = request.POST.get('stat')
    k = request.POST.get('pk')
    
    if not request.user.is_authenticated():
        return JsonResponse({'code': 2, 'msg': '登陆信息过期, 请重新登陆'})
    
    try:
        f = TagElasticsearchTask.objects.get(pk=int(k))
    except ObjectDoesNotExist:
        return JsonResponse({'code': 6, 'msg': '数据异常,请刷新页面重试'})
    
    f.stat = stat
    f.save()

    logwrite(request, 17, f, CHANGE)

    return JsonResponse({'code': 0, 'msg': '更新成功'})


def usercategory_tree(request):
    '''
    为linkage.js 提供三级联动分类目录
    '''
    floor = request.GET.get('fl', '2')
    f = FirstCategory.objects.all()
    resp = {}
    if floor == '2':
        for i in f:
            o = resp.setdefault(i.pk, 
                {'name': i.name, 'id': i.pk, 'cell': {}})
            for j in i.secondcategory_set.all():
                o['cell'][j.pk] = {'name': j.name, 'id': j.id}
    
    if floor == '3':
        for i in f:
            o = resp.setdefault(i.pk, 
                {'name': i.name, 'id': i.pk, 'cell': {}})
            for j in i.secondcategory_set.all():
                o['cell'][j.pk] = {'name': j.name, 'id': j.id, 'cell': {}}
                for k in j.thirdcategory_set.all():
                    o['cell'][j.pk]['cell'][k.pk] = {'name': k.name, 'id': k.id}
                    
    return JsonResponse(resp) 
    

@require_POST
def usertagitem_bytid(request):
    tagid = request.POST.get('tagid')
    
    if not request.user.is_authenticated():
        return JsonResponse({'code': 2, 'msg': '登陆信息过期, 请重新登陆'})
        
    if not tagid or not tagid.isdigit():
        return JsonResponse({'code': 3, 'msg': '非法标签id'})
    
    try:
        f = Tags.objects.get(full_tid=int(tagid))
    except ObjectDoesNotExist:
        return JsonResponse({'code': 3, 'msg': '非法标签id'})
    
    # 自定义型提供标签值列表, 字符串型提供模糊查询, 数字型提供范围查询
    if f.valtype == '2':
        items = TagsItems.objects.filter(tag__full_tid=int(tagid))
        res = [{'id':i.tid, 'name':i.name} for i in items]
    else:
        res = []
    return JsonResponse({'code': 0, 'msg': 'success', 'content': res, 'tagtype': f.valtype})

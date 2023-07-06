# -*- coding: utf-8 -*-

import os
import sys
import datetime
import copy

from django.conf import settings
from django.db.models import Q
from django.template import RequestContext
from django.http import (HttpResponseRedirect, 
                         HttpResponse, 
                         Http404, 
                         StreamingHttpResponse)
from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.core.mail import send_mail

from usertags.params import (
    CATEGORY_STAT, VALID_TIME, VALTYPES,
    TAG_FREQ, PERPAGE, TO_MAILLIST,
    USER_PROFILE_SIMPLE_ERROR_SUBJECT, USER_PROFILE_SIMPLE_ERROR_BODY,
    ELASTICSEARCH_TEMPLATE, CHART_TYPE, CHART_TYPE_DICT)
from usertags.models import (
    FirstCategory, SecondCategory, ThirdCategory,
    Tags, TagsItems, TagElasticsearchTask)



@login_required(login_url='/login/')
@permission_required('usertags.page_category', login_url='/login/', raise_exception=True)
def category_first(request):
    '''
    一级类目列表页
    '''

    titlebar = 'tags'

    page = request.GET.get('page', '')
    page = page.isdigit() and int(page) or 1

    catelist = FirstCategory.objects.order_by('-updatetime')
    catelist = Paginator(catelist, PERPAGE)
    catelist = catelist.page(page)

    return render(request, 
                  'usertags/category1.html', 
                  {'catelist': catelist,
                   'titlebar': titlebar})


@login_required(login_url='/login/')
@permission_required('usertags.view_category', login_url='/login/', raise_exception=True)
def category_first_view(request, itemid):
    '''
    一级类目查看页
    '''
    category = get_object_or_404(FirstCategory, pk=int(itemid))
    return render(request,
                  'usertags/category1_view.html',
                  {'category': category})


@login_required(login_url='/login/')
@permission_required('usertags.edit_category', login_url='/login/', raise_exception=True)
def category_first_edit(request, itemid=''):
    '''
    一级类目编辑页
    '''
    if itemid:
        category = get_object_or_404(FirstCategory, pk=int(itemid))
    else:
        category = None
    return render(request,
                  'usertags/category1_edit.html',
                  {'category': category,
                   'typelist': dict(CATEGORY_STAT)})


@login_required(login_url='/login/')
@permission_required('usertags.edit_category', login_url='/login/', raise_exception=True)
def category_first_add(request):
    return category_first_edit(request)


@login_required(login_url='/login/')
@permission_required('usertags.page_category', login_url='/login/', raise_exception=True)
def category_second(request):
    f = request.GET.get('f')
    st = request.GET.get('st')
    kw = request.GET.get('kw')

    page = request.GET.get('page', '')
    page = page.isdigit() and int(page) or 1

    titlebar = 'tags'

    catelist = SecondCategory.objects.all()

    if f:
        catelist = catelist.filter(first_category__pk=f)
    if st:
        catelist = catelist.filter(stat=st)
    if kw:
        catelist = catelist.filter(Q(name__contains=kw)|Q(full_tid=kw))

    catelist = catelist.order_by('-updatetime')

    catelist = Paginator(catelist, PERPAGE)
    catelist = catelist.page(page)

    firstcatelist = FirstCategory.objects.all()
    return render(request,
                  'usertags/category2.html',
                  {'catelist': catelist,
                   'firstcatelist': firstcatelist,
                   'titlebar': titlebar,
                   'typelist': dict(CATEGORY_STAT)})


@login_required(login_url='/login/')
@permission_required('usertags.view_category', login_url='/login/', raise_exception=True)
def category_second_view(request, itemid):
    '''
    二级类目查看页
    '''
    category = get_object_or_404(SecondCategory, pk=int(itemid))
    return render(request,
                  'usertags/category2_view.html',
                  {'category': category})


@login_required(login_url='/login/')
@permission_required('usertags.edit_category', login_url='/login/', raise_exception=True)
def category_second_edit(request, itemid=''):
    '''
    二级类目编辑页
    '''
    firstcatelist = FirstCategory.objects.all()

    if itemid:
        c = get_object_or_404(SecondCategory, pk=int(itemid))
    else:
        c = None
    return render(request,
                  'usertags/category2_edit.html',
                  {'category': c,
                   'firstcatelist': firstcatelist,
                   'typelist': dict(CATEGORY_STAT)})


@login_required(login_url='/login/')
@permission_required('usertags.edit_category', login_url='/login/', raise_exception=True)
def category_second_add(request):
    return category_second_edit(request)


@login_required(login_url='/login/')
@permission_required('usertags.page_category', login_url='/login/', raise_exception=True)
def category_third(request):
    f = request.GET.get('f')
    s = request.GET.get('s')
    st = request.GET.get('st')
    kw = request.GET.get('kw')

    titlebar = 'tags'

    page = request.GET.get('page', '')
    page = page.isdigit() and int(page) or 1

    catelist = ThirdCategory.objects.all()
    if f:
        catelist = catelist.filter(second_category__first_category__pk=f)
    if s:
        catelist = catelist.filter(second_category__pk=s)
    if st:
        catelist = catelist.filter(stat=st)
    if kw:
        catelist = catelist.filter(Q(name__contains=kw)|Q(full_tid=kw))
    
    catelist = catelist.order_by('-updatetime')

    catelist = Paginator(catelist, PERPAGE)
    catelist = catelist.page(page)

    return render(request,
                  'usertags/category3.html',
                  {'catelist': catelist,
                   'titlebar': titlebar,
                   'typelist': dict(CATEGORY_STAT)})


@login_required(login_url='/login/')
@permission_required('usertags.view_category', login_url='/login/', raise_exception=True)
def category_third_view(request, itemid):
    '''
    三级类目查看页
    '''
    c = get_object_or_404(ThirdCategory, pk=int(itemid))
    return render(request,
                  'usertags/category3_view.html',
                  {'category': c})


@login_required(login_url='/login/')
@permission_required('usertags.edit_category', login_url='/login/', raise_exception=True)
def category_third_edit(request, itemid=''):
    '''
    三级类目编辑页
    '''

    if itemid:
        c = get_object_or_404(ThirdCategory, pk=int(itemid))
    else:
        c = None
    return render(request,
                  'usertags/category3_edit.html',
                  {'category': c,
                  'typelist': dict(CATEGORY_STAT)})


@login_required(login_url='/login/')
@permission_required('usertags.edit_category', login_url='/login/', raise_exception=True)
def category_third_add(request):
    return category_third_edit(request)


@login_required(login_url='/login/')
@permission_required('usertags.page_usertags_tags', login_url='/login/', raise_exception=True)
def tags(request):
    f = request.GET.get('f')
    s = request.GET.get('s')
    # t = request.GET.get('t') # 三级类目弃用
    st = request.GET.get('st')
    kw = request.GET.get('kw')

    titlebar = 'tags'

    page = request.GET.get('page', '')
    page = page.isdigit() and int(page) or 1

    taglist = Tags.objects.all()
    if f:
        taglist = taglist.filter(category__first_category__pk=f)
    if s:
        taglist = taglist.filter(category__pk=s)
    if st:
        taglist = taglist.filter(stat=st)
    if kw:
        taglist = taglist.filter(Q(name__contains=kw)|Q(full_tid=kw)|Q(ename__contains=kw))

    taglist = taglist.order_by('-updatetime')
    taglist = Paginator(taglist, PERPAGE)
    taglist = taglist.page(page)

    return render(request,
                  'usertags/tags.html', 
                  {'taglist': taglist,
                   'titlebar': titlebar,
                   'typelist': dict(CATEGORY_STAT)})
 

@login_required(login_url='/login/')
@permission_required('usertags.view_usertags_tags', login_url='/login/', raise_exception=True)
def tags_view(request, itemid):
    '''
    单标签查看页
    '''
    c = get_object_or_404(Tags, pk=int(itemid))
    return render(request,
                  'usertags/tag_view.html', 
                  {'tag': c})


@login_required(login_url='/login/')
@permission_required('usertags.edit_usertags_tags', login_url='/login/', raise_exception=True)
def tags_edit(request, itemid=''):
    '''
    单标签编辑页
    '''

    if itemid:
        c = get_object_or_404(Tags, pk=int(itemid))
        for_group = [g.group for g in c.permusertags_set.all()]
    else:
        c = None
        for_group = []

    groups = Group.objects.all()

    return render(request,
                  'usertags/tag_edit.html', 
                  {'tag': c,
                   'groupall': groups,
                   'forgroup': for_group,
                   'typelist': dict(CATEGORY_STAT),
                   'valids': VALID_TIME,
                   'valtypes':VALTYPES,
                   'freq': TAG_FREQ})


@login_required(login_url='/login/')
@permission_required('usertags.edit_usertags_tags', login_url='/login/', raise_exception=True)
def tags_add(request):
    return tags_edit(request)


@login_required(login_url='/login/')
@permission_required('usertags.page_usertags_tagsitems', login_url='/login/', raise_exception=True)
def tagitems(request, tagid):

    titlebar = 'tags'

    page = request.GET.get('page', '')
    page = page.isdigit() and int(page) or 1

    tag = Tags.objects.get(pk=int(tagid))
    tagitemlist = TagsItems.objects.filter(tag=tag).exclude(stat='99')  # 删除不显示

    tagitemlist = tagitemlist.order_by('-stat', 'id')
    tagitemlist = Paginator(tagitemlist, PERPAGE)
    tagitemlist = tagitemlist.page(page)

    return render(request,
                  'usertags/tagitems.html', 
                  {'tagitemlist': tagitemlist,
                   'titlebar': titlebar,
                   'tag': tag})


@login_required(login_url='/login/')
@permission_required('usertags.view_usertags_tagsitems', login_url='/login/', raise_exception=True)
def tagitems_view(request, itemid):
    '''
    标签值查看页
    '''
    c = get_object_or_404(TagsItems, pk=int(itemid))
    return render(request,
                  'usertags/tagitems_view.html', 
                  {'item': c})


@login_required(login_url='/login/')
@permission_required('usertags.edit_usertags_tagsitems', login_url='/login/', raise_exception=True)
def tagitems_edit(request, itemid):
    '''
    标签值编辑页
    '''

    c = get_object_or_404(TagsItems, pk=int(itemid))
    return render(request,
                 'usertags/tagitems_edit.html',
                 {'tag': c,
                  'typelist': dict(CATEGORY_STAT)})


@login_required(login_url='/login/')
@permission_required('usertags.edit_usertags_tagsitems', login_url='/login/', raise_exception=True)
def tagitems_add(request, tagid):
    return render(request,
                  'usertags/tagitems_edit.html', 
                  {'tagid': tagid,
                   'typelist': dict(CATEGORY_STAT)})








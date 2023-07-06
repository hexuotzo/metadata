# -*- coding: utf-8 -*-

import json

from django.http.response import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth

from django.views.decorators.http import require_POST
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required
from django.contrib.admin.models import ADDITION, CHANGE, DELETION

from common.logentry import logwrite


@require_POST
def login(request):
    error_info = '登陆异常'
    
    username = request.POST.get('username', '')
    password = request.POST.get('passwd', '')
    remeberme = request.POST.get('remeberme', '')
    
    if request.user.is_authenticated():
        return JsonResponse({'code': 0})

    user = auth.authenticate(username=username,
        password=password)
    if user:
        auth.login(request, user)
        
        if remeberme == 'true':
            request.session.set_expiry(365 * 24 * 60 * 60)
            
        return JsonResponse({'code': 0})
    else:
        error_info = '用户名或密码错误'
    
    return JsonResponse({'code': 2, 'msg': error_info})


@require_POST
def changepwd(request):
    if not request.user.is_authenticated():
        return JsonResponse({'code': 1, 'msg': '登录信息已过期,请重新登录'})
    
    username = request.user.username
    oldpassword = request.POST.get('oldpwd')
    newpassword = request.POST.get('newpwd', '').strip() 
        
    user = auth.authenticate(username=username,
        password=oldpassword)
    
    if not user:
        return JsonResponse({'code': 2, 'msg': '原密码错误, 请重新输入'})
    if not newpassword:
        return JsonResponse({'code': 3, 'msg': '新密码不能为空, 请重新输入'})

    user.set_password(newpassword)
    user.save()
    return JsonResponse({'code': 0})

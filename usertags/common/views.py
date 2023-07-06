# -*- coding: utf-8 -*-

import os
import sys
import datetime

from django.conf import settings
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import (HttpResponseRedirect, 
    HttpResponse, 
    Http404, 
    StreamingHttpResponse)
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.decorators import login_required


def login(request):
    return render(request, 'login.html')
        

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('login'))


@login_required(login_url='/login/')
def changepwd(request):
    return render(request, 'changepwd.html')


@login_required(login_url='/login/')
def home(request):
    if request.user.has_perm('usertags.page_usertags_tags'):
        return HttpResponseRedirect(reverse('usertag'))
    if request.user.has_perm('usertags.page_category'):
        return HttpResponseRedirect(reverse('cate3rd')) 
    return render(request, 'home.html')

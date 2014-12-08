# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden
from surm.models import Group, JoinGroup, Resource, CreateGroupForm, AddResourceForm

def index(request):
    context = {
        'title': 'private-django-project',
    }
    return render(request, 'private_proj/index.html', context)


# django-registrationがログイン成功後/accounts/profile/にリダイレクト
# しようとさせているので無理矢理surmのindexにリダイレクトさせる．
def profile(request):
    return HttpResponseRedirect('/surm/')
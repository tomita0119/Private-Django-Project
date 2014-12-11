# -*- coding: utf-8 -*-
import urllib
import re
import json

from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse, Http404
from surm.models import Group, JoinGroup, Resource, ResourceUserView, ResourceUserFavorite, CreateGroupForm, AddResourceForm, GroupSettingsForm

def index(request):
    
    message = None
    
    if request.method == 'POST':
        if 'name' in request.POST:
            form = CreateGroupForm(request.POST)
            if form.is_valid():
                g = Group(name=form.cleaned_data['name'], creater=request.user, explain=form.cleaned_data['explain'])
                g.save()
                jg = JoinGroup(user=request.user, group=g)
                jg.save()
            else:
                return HttpResponseRedirect('/surm/cre_group/')
        if 'dlt_group_id' in request.POST:
            # グループ自体と，関連するデータを全て削除
            print request.POST['dlt_group_id']
            group = get_object_or_404(Group, pk=request.POST['dlt_group_id'])
            group_name = group.name
            
            dlt_resourceuserview = ResourceUserView.objects.filter(group=group)
            dlt_resourceuserview.delete()
            
            dlt_resource = Resource.objects.filter(group=group)
            dlt_resource.delete()
            
            dlt_joingroup = JoinGroup.objects.filter(group=group)
            dlt_joingroup.delete()
            
            group.delete()
            
            message = u'グループ ' +group_name+ u' を削除しました．'
    
    try:
        mygroups = Group.objects.filter(joingroup__user__exact=request.user)
        print mygroups
        context = {
            'title': 'index',
            'mygroups': mygroups,
            'message': message
        }
    except:
        context = {
            'title': 'index'
        }
    return render(request, 'surm/index.html', context)


def cre_group(request):
    form = CreateGroupForm()
    context = {
        'title': 'Create Group',
        'form': form
    }
    return render(request, 'surm/cre_group.html', context)


def group_index(request, group_id):
    
    group = get_object_or_404(Group, pk=group_id)
    join_users = User.objects.filter(joingroup__group__exact=group)
    
    # グループに参加していないユーザからのアクセスにはForbiddenを返す
    member_flg = False
    for join_user in join_users:
        if request.user == join_user:
            member_flg = True
            break
    if member_flg == False:
        return HttpResponseForbidden()
    
    # POSTされた値によって処理を変化
    if request.method == 'POST': # まずPOSTされたか判定
    
        if 'ajax' in request.POST: # ajaxがrequest.POST内にあれば以下の処理
            print 'ajax success'
            form = AddResourceForm()
            select_resource = get_object_or_404(Resource, pk=request.POST['ajax'])
            print select_resource
            select_resource.view += 1
            select_resource.save()
            new_user_resource_view = ResourceUserView.objects.get_or_create(group=group, resource=select_resource, user=request.user)
            
        elif 'url' in request.POST: # urlがrequest.POST内にあれば以下の処理
            form = AddResourceForm(request.POST)
            if form.is_valid(): # バリデート
                # ページタイトルはre，urllibを使ってURLから取得
                posted_url_info = urllib.urlopen(form.cleaned_data['url']).read()
                title = re.findall(r'<title>(.*)</title>', posted_url_info)
                new_resource = Resource(name=title[0].decode('utf-8'), url=form.cleaned_data['url'], creater=request.user, group=group, memo=form.cleaned_data['memo'])
                new_resource.save()
                form = AddResourceForm()
                
        elif 'add_user_id' in request.POST: # add_user_idがrequest.POST内にあれば以下の処理
            form = AddResourceForm()
            print request.POST['add_user_id']
            add_user = get_object_or_404(User, pk=request.POST['add_user_id'])
            new_join_user = JoinGroup(user=add_user, group=group)
            new_join_user.save()
            
        elif 'favorite_resource_id' in request.POST:
            print 'favorite resource'
            form = AddResourceForm()
            select_resource = get_object_or_404(Resource, pk=request.POST['favorite_resource_id'])
            new_resource_user_favorite = ResourceUserFavorite.objects.get_or_create(group=group, resource=select_resource, user=request.user)
            print new_resource_user_favorite[1]
            if new_resource_user_favorite[1] == True:
                response = json.dumps({'favorite_success': True})
            else:
                response = json.dumps({'favorite_success': False})
            return HttpResponse(response, mimetype='text/javascript')
            
        else: # それ以外(多分有り得ない)
            form = AddResourceForm()
    
    else: # POST値がない，普通のアクセスの場合
        form = AddResourceForm()
    
    resources = Resource.objects.filter(group=group).order_by('-created')
    read_users = ResourceUserView.objects.filter(group=group)
    favorite_resources_history = ResourceUserFavorite.objects.filter(group=group).order_by('-favorited')[:10]
    my_favorite_resources = ResourceUserFavorite.objects.filter(group=group, user=request.user).order_by('-favorited')
    
    context = {
        'title': group.name,
        'group': group,
        'resources': resources,
        'join_users': join_users,
        'form': form,
        'read_users': read_users,
        'favorite_resources_history': favorite_resources_history,
        'my_favorite_resources': my_favorite_resources,
    }
    
    return render(request, 'surm/group_index.html', context)


def add_group_member(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    all_users = User.objects.exclude(joingroup__group__exact=group)
    context = {
        'title': 'メンバー追加',
        'group': group,
        'all_users': all_users,
    }
    return render(request, 'surm/add_group_member.html', context)


def group_settings(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    if request.method == 'POST': # まずPOSTされたか判定
        if 'group_name' in request.POST:
            form = GroupSettingsForm(request.POST)
            if form.is_valid():
                if form.cleaned_data['group_name'] != '':
                    group.name = form.cleaned_data['group_name']
                if form.cleaned_data['explain'] != '':
                    group.explain = form.cleaned_data['explain']
                
                group.save()
    else:
        form = GroupSettingsForm()
    
    context = {
        'title': 'グループ設定',
        'group': group,
        'form': form
    }
    return render(request, 'surm/group_settings.html', context)

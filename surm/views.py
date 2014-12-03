# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden
from surm.models import Group, JoinGroup, Resource, CreateGroupForm, AddResourceForm

def index(request):
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            g = Group(name=form.cleaned_data['name'])
            g.save()
            jg = JoinGroup(user=request.user, group=g)
            jg.save()
        else:
            return HttpResponseRedirect('/surm/cre_group/')
    
    try:
        mygroups = Group.objects.filter(joingroup__user__exact=request.user)
        print mygroups
        context = {
            'title': 'index',
            'mygroups': mygroups,
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
    
    member_flg = False
    for join_user in join_users:
        if request.user == join_user:
            member_flg = True
            break
    if member_flg == False:
        return HttpResponseForbidden()
    
    if request.method == 'POST': # まずPOSTされたか判定
        if 'view_count' in request.POST: # view_countがrequest.POST内にあれば以下の処理
            form = AddResourceForm()
            select_resource = get_object_or_404(Resource, pk=request.POST['view_count'])
            print select_resource
            select_resource.view += 1
            select_resource.save()
        elif 'name' in request.POST: # view_countじゃない，つまりリソースの新規投稿の場合はこっちの処理
            form = AddResourceForm(request.POST)
            if form.is_valid():
                new_resource = Resource(name=form.cleaned_data['name'], url=form.cleaned_data['url'], creater=request.user, group=group, memo=form.cleaned_data['memo'])
                new_resource.save()
        elif 'add_user_id' in request.POST:
            form = AddResourceForm()
            print request.POST['add_user_id']
            add_user = get_object_or_404(User, pk=request.POST['add_user_id'])
            new_join_user = JoinGroup(user=add_user, group=group)
            new_join_user.save()
        else:
            form = AddResourceForm()
    else:
        form = AddResourceForm()
    
    resources = Resource.objects.filter(group=group).order_by('-created')
    
    context = {
        'title': group.name,
        'group': group,
        'resources': resources,
        'join_users': join_users,
        'form': form
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
    
    context = {
        'title': 'グループ設定',
    }
    return render(request, 'surm/group_settings.html', context)

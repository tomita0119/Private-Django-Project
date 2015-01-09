# -*- coding: utf-8 -*-
import urllib2
import re
import json

from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse, Http404
from surm.models import Group, JoinGroup, Resource, ResourceUserView, ResourceUserFavorite, Tag, TagResource, ActionHistory, Comment, CreateGroupForm, AddResourceForm, AddResourceExceptForm, GroupSettingsForm, CommentForm

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

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
                
                new_actionhistory = ActionHistory(user=request.user, group=g, kind='group_create')
                new_actionhistory.save()
                
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
            
            new_actionhistory = ActionHistory(user=request.user, group=group, kind='group_delete')
            new_actionhistory.save()
            
            message = u'グループ ' +group_name+ u' を削除しました．'
    
    try:
        mygroups = Group.objects.filter(joingroup__user__exact=request.user)
        my_actionhistories = ActionHistory.objects.filter(user=request.user).order_by('-acted')[:5]
        print mygroups
        print my_actionhistories
        context = {
            'title': 'index',
            'mygroups': mygroups,
            'my_actionhistories': my_actionhistories,
            'message': message,
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
    
    message = None
    
    group = get_object_or_404(Group, pk=group_id)
    join_users = User.objects.filter(joingroup__group__exact=group)
    
    comment_form_flg = False
    
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
            new_actionhistory = ActionHistory(user=request.user, group=group, kind='resource_view', resource=select_resource)
            new_actionhistory.save()
            
        elif 'name' in request.POST: # get_resourcetitle_errorからポストされた場合
            add_resource_except_form = AddResourceExceptForm(request.POST)
            if add_resource_except_form.is_valid():
            
                memos = re.split(r'\[(.*)\]', add_resource_except_form.cleaned_data['memo']) # 正規表現でタグ以降だけ抽出
                
                try: # メモにタグしか書かなかった場合，IndexErrorを吐くのでそのときは例外処理
                    new_resource = Resource(name=add_resource_except_form.cleaned_data['name'], url=add_resource_except_form.cleaned_data['url'], creater=request.user, memo=memos[2], group=group)
                except IndexError:
                    new_resource = Resource(name=add_resource_except_form.cleaned_data['name'], url=add_resource_except_form.cleaned_data['url'], creater=request.user, group=group)
                
                new_resource.save()
                
                new_actionhistory = ActionHistory(user=request.user, group=group, kind='resource_post', resource=new_resource)
                new_actionhistory.save()
            
            form = AddResourceForm()
            
        elif 'url' in request.POST: # urlがrequest.POST内にあれば以下の処理
            form = AddResourceForm(request.POST)
            if form.is_valid(): # バリデート
                # ページタイトルはre，urllibを使ってURLから取得
                posted_url_info = urllib2.urlopen(form.cleaned_data['url']).read()
                pattern = re.compile(r'<title>(.*)</title>', re.IGNORECASE)
                title = pattern.findall(posted_url_info)
                memos = re.split(r'\[(.*)\]', form.cleaned_data['memo']) # 正規表現でタグ以降だけ抽出
                if len(title) == 0: # titleに何も入ってない(リソースタイトルを取って来れなかった場合)
                    return redirect('surm.views.get_resourcetitle_error', group_id=group.id)
                try: # メモにタグしか書かなかった場合，IndexErrorを吐くのでそのときは例外処理
                    new_resource = Resource(name=title[0].decode('utf-8'), url=form.cleaned_data['url'], creater=request.user, group=group, memo=memos[2])
                except IndexError:
                    new_resource = Resource(name=title[0].decode('utf-8'), url=form.cleaned_data['url'], creater=request.user, group=group)
                new_resource.save()
                
                new_actionhistory = ActionHistory(user=request.user, group=group, kind='resource_post', resource=new_resource)
                new_actionhistory.save()
                
                # 入力されたタグをタグテーブルへ
                registered_tags = re.findall(r'\[(.*?)\]', form.cleaned_data['memo'])
                print registered_tags
                for registered_tag in registered_tags:
                    new_tag = Tag.objects.get_or_create(group=group, tag=registered_tag)
                    print new_tag[0]
                    #new_tag.save()
                    new_tag_resource = TagResource.objects.get_or_create(group=group, resource=new_resource, tag=new_tag[0])
                    #new_tag_resource.save()
                
                ## グループのメンバーにメール通知 ##
                ## !【todo】hitomita@is.kochi-u.ac.jp に送る設定になっているので，グループメンバーに送る様に直す 
                ## リソース削除された時等，よく使う事になるのでこの部分は関数化できない？
                
                # テンプレート読み込み
                plaintext = get_template('email.txt')
                
                # テンプレートに流し込む情報を整理
                sender = 'tomita.research@gmail.com'
                group = group
                user = request.user
                resource_name = title[0].decode('utf-8')
                
                # 送信先
                recipients = ['hitomita@is.kochi-u.ac.jp']
                subject = u'リソースが投稿されました'
                
                # テンプレートに整理した情報を流し込む
                d = Context({'group': group, 'user': user, 'resource_name': resource_name})
                textcontent = plaintext.render(d)
                
                # メール送信
                msg = EmailMultiAlternatives(subject, textcontent, sender, recipients)
                msg.send()
                
                form = AddResourceForm()
                
        elif 'add_user_id' in request.POST: # add_user_idがrequest.POST内にあれば以下の処理
            form = AddResourceForm()
            print request.POST['add_user_id']
            add_user = get_object_or_404(User, pk=request.POST['add_user_id'])
            new_join_user = JoinGroup(user=add_user, group=group)
            new_join_user.save()
            
            new_actionhistory = ActionHistory(user=add_user, group=group, kind='group_join')
            new_actionhistory.save()
            
        elif 'favorite_resource_id' in request.POST:
            print 'favorite resource'
            form = AddResourceForm()
            select_resource = get_object_or_404(Resource, pk=request.POST['favorite_resource_id'])
            new_resource_user_favorite = ResourceUserFavorite.objects.get_or_create(group=group, resource=select_resource, user=request.user)
            print new_resource_user_favorite[1]
            if new_resource_user_favorite[1] == True:
                new_actionhistory = ActionHistory(user=request.user, group=group, kind='resource_favorite', resource=select_resource)
                new_actionhistory.save()
                print 'favorite'
                response = json.dumps({'favorite_success': True})
            else:
                response = json.dumps({'favorite_success': False})
            return HttpResponse(response, mimetype='text/javascript')
            
        elif 'dlt_resource_id' in request.POST:
            
            # 【メモ】リレーションを貼ってるレコードもDJangoが自動で削除してくれるっぽい
            resource = get_object_or_404(Resource, pk=request.POST['dlt_resource_id'])
            resource.delete()
            
            new_actionhistory = ActionHistory(user=request.user, group=group, kind='resource_delete', resource=resource)
            new_actionhistory.save()
            
            message = u'リソースを削除しました'
            
            form = AddResourceForm()
        
        elif 'comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid(): # バリデート
                select_resource = get_object_or_404(Resource, pk=request.POST['resource_id'])
                new_comment = Comment(user=request.user, group=group, resource=select_resource, comment=comment_form.cleaned_data['comment'])
                new_comment.save()
                message = select_resource.name + u'にコメントを書き込みました'
                comment_form_flg = True
            form = AddResourceForm()
            
        else: # それ以外(多分有り得ない)
            form = AddResourceForm()
    
    else: # POST値がない，普通のアクセスの場合
        form = AddResourceForm()
    
    if comment_form_flg == False:
        comment_form = CommentForm()
    
    resources = Resource.objects.filter(group=group).order_by('-created')
    read_users = ResourceUserView.objects.filter(group=group)
    favorite_resources_history = ResourceUserFavorite.objects.filter(group=group).order_by('-favorited')[:5]
    my_favorite_resources = ResourceUserFavorite.objects.filter(group=group, user=request.user).order_by('-favorited')[:5]
    group_tags = Tag.objects.filter(group=group).order_by('tag')
    tag_resources = TagResource.objects.filter(group=group)
    comments = Comment.objects.filter(group=group).order_by('-commented')
    
    join_users_count_half = join_users.count() / 2
    
    recent_comments = comments[:5]
    
    context = {
        'title': group.name,
        'message': message,
        'group': group,
        'resources': resources,
        'join_users': join_users,
        'form': form,
        'read_users': read_users,
        'favorite_resources_history': favorite_resources_history,
        'my_favorite_resources': my_favorite_resources,
        'group_tags': group_tags,
        'tag_resources': tag_resources,
        'comment_form': comment_form,
        'comments': comments,
        'join_users_count_half': join_users_count_half,
        'recent_comments': recent_comments,
    }
    
    return render(request, 'surm/group_index.html', context)


def add_group_member(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    all_users = User.objects.exclude(joingroup__group__exact=group)
    context = {
        'title': 'Add Member',
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
                new_actionhistory = ActionHistory(user=request.user, group=group, kind='group_modify')
    else:
        form = GroupSettingsForm()
    
    context = {
        'title': 'Group Settings',
        'group': group,
        'form': form
    }
    return render(request, 'surm/group_settings.html', context)


def tag_filtering(request, group_id, tag_id):
    
    comment_form = CommentForm()
    
    group = get_object_or_404(Group, pk=group_id)
    join_users = User.objects.filter(joingroup__group__exact=group)
    group_tags = Tag.objects.filter(group=group).order_by('tag')
    my_favorite_resources = ResourceUserFavorite.objects.filter(group=group, user=request.user).order_by('-favorited')[:5]
    favorite_resources_history = ResourceUserFavorite.objects.filter(group=group).order_by('-favorited')[:5]
    
    tag = get_object_or_404(Tag, pk=tag_id)
    tag_resources = TagResource.objects.filter(group=group, tag=tag)
    
    resources = Resource.objects.filter(tagresource__group__exact=group, tagresource__tag__exact=tag).order_by('-created')
    print resources
    
    context = {
        'title': u'About 「' +tag.tag+ u'」',
        'group': group,
        'join_users': join_users,
        'group_tags': group_tags,
        'my_favorite_resources': my_favorite_resources,
        'favorite_resources_history': favorite_resources_history,
        'tag': tag,
        'tag_resources': tag_resources,
        'resources': resources,
        'comment_form': comment_form,
    }
    
    return render(request, 'surm/tag_filtering.html', context)


def my_favorite(request, group_id):
    
    message = None
    
    # left-content, right-contentで使うデータの取得
    group = get_object_or_404(Group, pk=group_id)
    join_users = User.objects.filter(joingroup__group__exact=group)
    group_tags = Tag.objects.filter(group=group).order_by('tag')
    my_favorite_resources = ResourceUserFavorite.objects.filter(group=group, user=request.user).order_by('-favorited')
    favorite_resources_history = ResourceUserFavorite.objects.filter(group=group).order_by('-favorited')[:5]
    
    if request.method == 'POST': # まずPOSTされたか判定
        if 'favorite_resource_id' in request.POST:
            select_resource = get_object_or_404(Resource, pk=request.POST['favorite_resource_id'])
            del_resource = ResourceUserFavorite.objects.filter(group=group, resource=select_resource, user=request.user)
            del_resource.delete()
            message = select_resource.name + u' を削除しました'
    
    context = {
        'title': 'MyFavorite',
        'group': group,
        'join_users': join_users,
        'group_tags': group_tags,
        'my_favorite_resources': my_favorite_resources,
        'favorite_resources_history': favorite_resources_history,
        'message': message,
    }
    return render(request, 'surm/my_favorite.html', context)


def get_resourcetitle_error(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    form = AddResourceExceptForm()
    context = {
        'title' : 'Get ResourceTitle Error',
        'group': group,
        'form': form,
    }
    return render(request, 'surm/get_resourcetitle_error.html', context)

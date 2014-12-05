# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django import forms

# グループ
class Group(models.Model):
    name = models.CharField('Name', max_length=100)
    created = models.DateTimeField('Created', auto_now_add=True)
    explain = models.CharField('Explain', max_length=100, null=True, blank=True)
    creater = models.ForeignKey(User)

# 参加しているグループ
class JoinGroup(models.Model):
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)

# リソース
class Resource(models.Model):
    name = models.CharField('Name', max_length=100)
    url = models.URLField('URL', max_length=100)
    creater = models.ForeignKey(User)
    created = models.DateTimeField('Created', auto_now_add=True)
    group = models.ForeignKey(Group)
    memo = models.TextField('Memo', null=True, blank=True)
    view = models.IntegerField('View', default=0)

# どのグループのどのリソースがどのユーザに閲覧されたかを記録
class ResourceUserView(models.Model):
    group = models.ForeignKey(Group)
    resource = models.ForeignKey(Resource)
    user = models.ForeignKey(User)

# ------------ フォーム ------------ #

# グループ追加のフォーム
class CreateGroupForm(forms.Form):
    name = forms.CharField(max_length=100)
    explain = forms.CharField(required=False, max_length=100, widget=forms.Textarea)

# リソース追加のフォーム
class AddResourceForm(forms.Form):
    name = forms.CharField(max_length=100)
    url = forms.URLField(max_length=100)
    memo = forms.CharField(required=False, max_length=200, widget=forms.Textarea)

# グループ設定のフォーム
class GroupSettingsForm(forms.Form):
    group_name = forms.CharField(required=False, max_length=100)
    explain = forms.CharField(required=False, max_length=100, widget=forms.Textarea)

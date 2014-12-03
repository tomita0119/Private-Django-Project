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

# ------------ フォーム ------------ #

# グループ追加のフォーム
class CreateGroupForm(forms.Form):
    name = forms.CharField(max_length=100)

# リソース追加のフォーム
class AddResourceForm(forms.Form):
    name = forms.CharField(max_length=100)
    url = forms.URLField(max_length=100)
    memo = forms.CharField(required=False, max_length=200, widget=forms.Textarea)

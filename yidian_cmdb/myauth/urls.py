# -*- coding:utf8 -*-
# Author: Chenxc
# Email: chenxiaochen@yidian-inc.com
# Date: 2016-07-27
from django.conf.urls import url
from views import (
    CurrentUserDashboardView, UserListView, UserCreationView, UserUpdateView, UserPasswordResetView, UserDeletionView,
    GroupListView, GroupCreationView, GroupUpdateView, GroupDeletionView
)


urlpatterns = [
    # 用户列表
    url(r'user/$', UserListView.as_view(), name='myauth-user-list'),
    # 创建用户
    url(r'user/creation/$', UserCreationView.as_view(), name='myauth-user-creation'),
    # 更新用户信息
    url(r'user/update/(?P<user_id>\d+)/$', UserUpdateView.as_view(), name='myauth-user-update'),
    # 为用户重置密码
    url(r'user/update/(?P<user_id>\d+)/password-reset/$', UserPasswordResetView.as_view(),
        name='myauth-user_password-reset'),
    # 登录用户信息
    url('current-user/dashboard/$', CurrentUserDashboardView.as_view(), name='myauth-current_user-dashboard'),
    # 删除用户
    url(r'user/deletion/(?P<user_id>\d+)/$', UserDeletionView.as_view(), name='myauth-user-deletion'),
    # 用户组列表
    url(r'groups/$', GroupListView.as_view(), name='myauth-group-list'),
    # 创建用户组
    url(r'group/creation/$', GroupCreationView.as_view(), name='myauth-group-creation'),
    # 更新用户组
    url(r'group/update/(?P<group_id>\d+)/$', GroupUpdateView.as_view(), name='myauth-group-update'),
    # 删除用户组
    url(r'group/deletion/(?P<group_id>\d+)/$', GroupDeletionView.as_view(), name='myauth-group-deletion'),
]

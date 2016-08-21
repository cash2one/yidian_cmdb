# -*- coding:utf8 -*-
# Author: Chenxc
# Email: chenxiaochen@yidian-inc.com
# Date: 2016-07-27

"""yidian_cmdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from django.contrib.auth import views as auth_views
from myauth.forms import MyAuthenticationForm, UserPwdUpdateForm


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('myauth.urls')),
    url(r'^asset/', include('asset.urls')),

]

# 使用 Django auth 提供的登录、注销视图
urlpatterns += [
    # 平台登录
    url(r'^login/$', auth_views.login, {'template_name': 'login.html', "authentication_form": MyAuthenticationForm},
        name='myauth-user-login'),
    # 用户注销
    url(r'^logout/$', auth_views.logout_then_login, name='myauth-user-logout'),
    # 用户密码修改
    url(r'^user/pwd-change/$', auth_views.password_change,
        {'template_name': 'myauth/user_password_update.html', 'password_change_form': UserPwdUpdateForm,
         'post_change_redirect': auth_views.logout_then_login}, name='myauth-pwd-update'),
]

# REST framework's login and logout views
urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

# 项目接口 urls
urlpatterns += [
    # 资产接口
    url(r'^api/asset/', include('asset.rest_urls')),
]


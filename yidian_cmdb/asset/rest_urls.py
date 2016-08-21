# -*- coding:utf8 -*-
# Author: Chenxc
# Email: chenxiaochen@yidian-inc.com
# Date: 2016-08-10
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from restful_views import IdcList, CabinetList, HostList


urlpatterns = [
    url(r'^idc/$', IdcList.as_view()),
    url(r'cabinet/$', CabinetList.as_view()),
    url(r'host/$', HostList.as_view()),
]

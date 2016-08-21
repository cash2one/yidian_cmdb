# -*- coding:utf8 -*-
# Author: Chenxc
# Email: chenxiaochen@yidian-inc.com
# Date: 2016-07-28
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class MyPermissionRequiredMixin(PermissionRequiredMixin):
    """
    统一设置项目中认证部分的行为
    """
    raise_exception = True

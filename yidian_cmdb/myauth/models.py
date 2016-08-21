# -*- coding:utf8 -*-
# Author: Chenxc
# Email: chenxiaochen@yidian-inc.com
# Date: 2016-07-28
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    """
    针对项目自定义用户模型
    """
    job_number = models.CharField(verbose_name=u'工号', max_length=128, blank=True)
    phone_number = models.CharField(verbose_name=u'手机号', max_length=128, blank=True)
    dingding = models.CharField(verbose_name=u'钉钉', max_length=128, blank=True)

    def __unicode__(self):
        return self.username

    class Meta(AbstractUser.Meta):
        permissions = (
            ("read_myuser", "Can read %s" % _('user')),
        )

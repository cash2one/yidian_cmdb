# -*- coding:utf8 -*-
# Author: Chenxc
# Email: chenxiaochen@yidian-inc.com
# Date: 2016-07-27
from __future__ import unicode_literals
from django.db import models
import os
from datetime import timedelta, datetime
from yidian_cmdb.settings import MEDIA_ROOT


class TimeStampedModel(models.Model):
    """
    提供时间戳字段
    """
    created = models.DateTimeField(verbose_name=u"创建时间", auto_now_add=True)
    changed = models.DateTimeField(verbose_name=u"更新时间", auto_now=True)

    class Meta:
        abstract = True


class RemarkModel(models.Model):
    """
    提供备注字段
    """
    remark = models.TextField(verbose_name=u'备注', blank=True)

    class Meta:
        abstract = True


class AppBaseModel(RemarkModel, TimeStampedModel):
    """
    提供应用所有模型所需的公共字段
    """
    class Meta:
        abstract = True


class Manufacturer(AppBaseModel):
    """
    厂商
    """
    name = models.CharField(verbose_name=u'厂商名称', max_length=128)
    sale = models.CharField(verbose_name=u'销售接口人', max_length=128, blank=True)
    sale_contact = models.CharField(verbose_name=u'销售接口人联系信息', max_length=128, blank=True)
    service = models.CharField(verbose_name=u'售后接口人', max_length=128, blank=True)
    service_contact = models.CharField(verbose_name=u'售后接口人联系信息', max_length=128, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'厂商'
        verbose_name_plural = u'厂商'
        permissions = (
            ("read_manufacturer", "Can read %s" % verbose_name_plural),
        )


class ProductBaseModel(AppBaseModel):
    """
    产品基础属性
    """
    manufacturer = models.ForeignKey(Manufacturer, verbose_name=u'所属厂商',
                                     related_name="%(app_label)s_%(class)s_related")
    model = models.CharField(verbose_name=u'型号', max_length=128)
    u = models.PositiveIntegerField(verbose_name=u'物理U数', default=1)
    tag = models.CharField(verbose_name=u'分类标签', max_length=128, blank=True,
                           help_text=u'填写标签,用于区分同型号特配机型')

    def __unicode__(self):
        return '%s(%s)' % (self.model, self.tag)


class ServerProduct(ProductBaseModel):
    """
    服务器产品
    """
    _DISK_TYPE_CHOICES = (
        ('0', 'HDD'),
        ('1', 'SSD'),
        ('2', 'SSD+HDD')
    )
    _NIC_TYPE_CHOICES = (
        ('0', u'电口'),
        ('1', u'光口'),
        ('2', u'电口+光口'),
    )
    cpu_model = models.CharField(verbose_name=u'处理器型号', max_length=128)
    cpu_count = models.PositiveIntegerField(verbose_name=u'处理器物理个数', default=1)
    mem_size = models.FloatField(verbose_name=u'内存大小 单位:G')
    mem_count = models.PositiveIntegerField(verbose_name=u'内存条数', default=1)
    disk_type = models.CharField(verbose_name=u'磁盘类型', max_length=1, choices=_DISK_TYPE_CHOICES, default=0)
    ssd_disk_count = models.PositiveIntegerField(verbose_name=u'固态硬盘块数', default=0)
    hdd_disk_count = models.PositiveIntegerField(verbose_name=u'机械硬盘块数', default=0)
    nic_type = models.CharField(verbose_name=u'网卡类型', max_length=1, choices=_NIC_TYPE_CHOICES, default=0)
    dk_nic_count = models.PositiveIntegerField(verbose_name=u'电口网卡块数', default=0)
    gk_nic_count = models.PositiveIntegerField(verbose_name=u'光口网卡块数', default=0)

    class Meta:
        verbose_name = u'服务器产品出厂配置'
        verbose_name_plural = u'服务器产品出厂配置'
        permissions = (
            ("read_serverproduct", "Can read %s" % verbose_name_plural),
        )


class Idc(AppBaseModel):
    """
    IDC 机房
    """
    _IDC_STATUS = (
        ('0', u'在线'),
        ('1', u'下线'),
    )
    name = models.CharField(verbose_name=u'机房名称', max_length=128)
    address = models.CharField(verbose_name=u"地址", max_length=128)
    contacts = models.CharField(verbose_name=u'联系人', max_length=128, blank=True)
    contact_info = models.CharField(verbose_name=u'联系人电话', max_length=128, blank=True)
    ctc_bandwidth = models.FloatField(verbose_name=u'电信带宽／Gbps', default=0)
    cnc_bandwidth = models.FloatField(verbose_name=u'联通带宽／Gbps', default=0)
    bgp_bandwidth = models.FloatField(verbose_name=u'BGP带宽／Gbps', default=0)
    status = models.CharField(verbose_name=u'状态', max_length=1, choices=_IDC_STATUS, default=0)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'机房'
        verbose_name_plural = u'机房'
        permissions = (
            ("read_idc", "Can read %s" % verbose_name_plural),
        )


class Cabinet(AppBaseModel):
    """
    Cabinets model
    """
    _STANDBY_POWER = (
        ('0', u'支持'),
        ('1', u'不支持'),
    )
    idc = models.ForeignKey(Idc, verbose_name=u"所属机房", related_name='cabinets')
    name = models.CharField(verbose_name=u'机柜名称', max_length=128)
    standby_power = models.CharField(verbose_name=u'是否双路电', max_length=1, choices=_STANDBY_POWER, default='0')
    u = models.PositiveIntegerField(verbose_name=u'机柜u数', default=42)
    voltage = models.PositiveIntegerField(verbose_name=u'供电电压／V', default=0)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'机柜'
        verbose_name_plural = u'机柜'
        permissions = (
            ("read_cabinet", "Can read %s" % verbose_name_plural),
        )


class Node(AppBaseModel):
    """
    业务树节点模型
    """
    parent = models.ForeignKey('self', verbose_name=u'父节点', related_name='child_nodes', blank=True, null=True)
    node_name = models.CharField(verbose_name=u'节点名称', max_length=128, unique=True)
    verbose_name = models.CharField(verbose_name=u'冗长名称', max_length=256)
    absolute_path = models.CharField(verbose_name=u'路径跟踪', max_length=1024, help_text='root||node||node1||node1.1')

    def __unicode__(self):
        return '%s (%s)' % (self.verbose_name, self.absolute_path)

    class Meta:
        verbose_name = u'公司业务树节点'
        verbose_name_plural = u'公司业务树节点'
        permissions = (
            ("read_node", "Can read %s" % verbose_name_plural),
        )


class Host(AppBaseModel):
    """
    服务器资源
    """
    _STATUS_CHOICES = (
        ('0', u'空闲'),
        ('1', u'已分配'),
        ('2', u'故障'),
        ('3', u'报废')
    )
    cabinet = models.ForeignKey(Cabinet, verbose_name=u'所处机柜', related_name='cabinet_to_hosts', blank=True, null=True,
                                on_delete=models.SET_NULL)
    product = models.ForeignKey(ServerProduct, verbose_name=u"产品型号", related_name='serverproduct_to_hosts',
                                blank=True, null=True)
    nodes = models.ManyToManyField(Node, verbose_name=u'挂载业务节点', related_name='node_to_nodes', blank=True)
    cabinet_index = models.PositiveIntegerField(verbose_name=u'机柜位索引', blank=True, null=True,
                                                help_text=u'默认机柜从上至下(0, 1, 2……)计数')
    an = models.CharField(verbose_name=u'资产码', max_length=128, blank=True, unique=True)
    sn = models.CharField(verbose_name=u'服务码', max_length=128, unique=True)
    host_name = models.CharField(verbose_name=u'主机名', max_length=128, blank=True)
    os = models.CharField(verbose_name=u'操作系统', max_length=128, blank=True)
    management_ip = models.GenericIPAddressField(verbose_name=u'远程管理卡IP', blank=True, null=True)
    online_date = models.DateTimeField(verbose_name=u"上架日期", blank=True, null=True)
    status = models.CharField(verbose_name=u'服务器状态', max_length=1, choices=_STATUS_CHOICES)

    def __unicode__(self):
        return self.sn

    @property
    def expire_date(self):
        if self.online_date:
            # 保质期默认 (3年)1095天
            return self.online_date + timedelta(days=1095)

    class Meta:
        verbose_name = u'服务器'
        verbose_name_plural = u'服务器'
        permissions = (
            ("read_asset", "Can read %s" % verbose_name_plural),
        )


class Nic(AppBaseModel):
    """
    服务器网卡
    """
    _NIC_TYPE_CHOICES = (
        ('0', u'电口'),
        ('1', u'光口'),
    )
    host = models.ForeignKey(Host, verbose_name=u'主机', related_name='nics')
    sn = models.CharField(verbose_name=u'服务码', max_length=128, blank=True)
    nic_type = models.CharField(verbose_name=u'网卡类型', max_length=1, choices=_NIC_TYPE_CHOICES, blank=True, null=True)
    nic_speed = models.PositiveIntegerField(verbose_name=u'网卡速率/Mbps', blank=True, null=True)
    nic_name = models.CharField(verbose_name=u'网卡名称', max_length=128, blank=True)
    mac = models.CharField(verbose_name=u'mac地址', max_length=128, blank=True)
    ipv4 = models.GenericIPAddressField(verbose_name=u'ipv4地址', blank=True, null=True)
    netmask = models.CharField(verbose_name=u'子网掩码', max_length=128, blank=True)
    ipv6 = models.GenericIPAddressField(verbose_name=u'ipv6地址', blank=True, null=True)
    other_ip = models.TextField(verbose_name=u'虚拟IPs(ip间逗号隔开)', blank=True)

    def __unicode__(self):
        return self.sn

    class Meta:
        verbose_name = u'主机网卡'
        verbose_name_plural = u'主机网卡'
        permissions = (
            ("read_asset", "Can read %s" % verbose_name_plural),
        )


def upload_file_save_path(instance, filename):
    """
    重命名上传文件文件名

        命名规则: 在文件名中加入格式化时间戳
    """
    # filename = filename.encode('utf-8')

    filename_split_list = filename.split('.')

    timestamp_format = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    original_prefix = filename_split_list[0]
    suffix = filename_split_list[1]
    new_filename = '{original_prefix}_{timestamp_format}.{suffix}'.format(original_prefix=original_prefix,
                                                                          timestamp_format=timestamp_format, suffix=suffix)
    path = os.path.join(MEDIA_ROOT, 'host_batch_creation_excel/%(filename)s' % {'filename': new_filename})
    return path


class UploadExcel(models.Model):
    """
    用于处理批量创建CMDB记录时上传的EXCEL
    """
    upload_excel = models.FileField(verbose_name=u'批量创建模版', upload_to=upload_file_save_path, max_length=128)

    def __unicode__(self):
        return self.id

    class Meta:
        verbose_name = u'批量创建模版'
        verbose_name_plural = u'批量创建模版'
        permissions = (
            ("read_asset", "Can read %s" % verbose_name_plural),
        )

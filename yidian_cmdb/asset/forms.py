# -*- coding:utf8 -*-
# Author: Chenxc
# Email: chenxiaochen@yidian-inc.com
# Date: 2016-07-29
from django import forms
from django.forms.models import inlineformset_factory
from models import Manufacturer, ServerProduct, Idc, Cabinet, Node, Host, UploadExcel


class ManufacturerForm(forms.ModelForm):
    """
    厂商表单
    """
    class Meta:
        model = Manufacturer
        fields = [
            'name', 'sale', 'sale_contact', 'service', 'service_contact', 'remark'
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'sale': forms.TextInput(attrs={'class': 'form-control'}),
            'sale_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'service': forms.TextInput(attrs={'class': 'form-control'}),
            'service_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'remark': forms.Textarea(attrs={'class': 'form-control'}),
        }


class ServerProductForm(forms.ModelForm):
    """
    服务器产品表单
    """
    class Meta:
        model = ServerProduct
        fields = [
            'manufacturer', 'model', 'u', 'cpu_model', 'cpu_count', 'mem_size', 'mem_count', 'disk_type',
            'ssd_disk_count', 'hdd_disk_count', 'nic_type', 'dk_nic_count', 'gk_nic_count', 'tag',
            'remark'
        ]
        widgets = {
            'manufacturer': forms.Select(attrs={'class': 'form-control select2', 'style': "width: 100%;"}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'u': forms.NumberInput(attrs={'class': 'form-control'}),
            'cpu_model': forms.TextInput(attrs={'class': 'form-control'}),
            'cpu_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'mem_size': forms.NumberInput(attrs={'class': 'form-control'}),
            'mem_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'disk_type': forms.Select(attrs={'class': 'form-control'}),
            'ssd_disk_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'hdd_disk_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'nic_type': forms.Select(attrs={'class': 'form-control'}),
            'dk_nic_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'gk_nic_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'tag': forms.TextInput(attrs={'class': 'form-control'}),
            'remark': forms.Textarea(attrs={'class': 'form-control'})
        }


class IdcForm(forms.ModelForm):
    """
    Idc form
    """
    class Meta:
        model = Idc
        fields = [
            'name', 'address', 'contacts', 'contact_info', 'ctc_bandwidth', 'cnc_bandwidth', 'bgp_bandwidth', 'status',
            'remark'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'contacts': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_info': forms.TextInput(attrs={'class': 'form-control'}),
            'ctc_bandwidth': forms.NumberInput(attrs={'class': 'form-control'}),
            'cnc_bandwidth': forms.NumberInput(attrs={'class': 'form-control'}),
            'bgp_bandwidth': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'},),
            'remark': forms.Textarea(attrs={'class': 'form-control'})
         }


class CabinetForm(forms.ModelForm):
    """
    机柜表单
    """
    class Meta:
        model = Cabinet
        fields = [
            'name', 'standby_power', 'u', 'voltage', 'remark'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'standby_power': forms.Select(attrs={'class': 'form-control', 'id': 'disabledSelect'}),
            'u': forms.NumberInput(attrs={'class': 'form-control'}),
            'voltage': forms.NumberInput(attrs={'class': 'form-control'}),
            'remark': forms.Textarea(attrs={'class': 'form-control'})
        }


class NodeForm(forms.ModelForm):
    """
    业务树节点表单
    """
    class Meta:
        model = Node
        fields = [
            'parent', 'node_name', 'verbose_name', 'absolute_path', 'remark'
        ]
        widgets = {
            'parent': forms.Select(attrs={'class': 'form-control'}),
            'node_name': forms.TextInput(attrs={'class': 'form-control'}),
            'verbose_name': forms.TextInput(attrs={'class': 'form-control'}),
            'absolute_path': forms.TextInput(attrs={'class': 'form-control'}),
            'remark': forms.Textarea(attrs={'class': 'form-control'})
        }


class HostForm(forms.ModelForm):
    """
    主机表单
    """
    class Meta:
        model = Host
        fields = [
            'an', 'sn', 'host_name', 'product', 'cabinet', 'cabinet_index', 'os', 'management_ip', 'nodes',
            'online_date', 'status', 'remark'
        ]
        widgets = {
            'an': forms.TextInput(attrs={'class': 'form-control'}),
            'sn': forms.TextInput(attrs={'class': 'form-control'}),
            'host_name': forms.TextInput(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control select2', 'style': "width: 100%;"}),
            'cabinet': forms.Select(attrs={'class': 'form-control select2', 'style': "width: 100%;"}),
            'cabinet_index': forms.NumberInput(attrs={'class': 'form-control'}),
            'os': forms.TextInput(attrs={'class': 'form-control'}),
            'management_ip': forms.TextInput(attrs={'class': 'form-control', 'data-inputmask': "'alias': 'ip'",
                                                    'data-mask': ''}),
            'nodes': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'online_date': forms.TextInput(attrs={'class': 'form-control pull-right'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'remark': forms.Textarea(attrs={'class': 'form-control'})
        }


class HostBatchCreationForm(forms.ModelForm):
    """
    主机批量添加表单
    """
    class Meta:
        model = UploadExcel
        fields = '__all__'


class HostFilterForm(forms.ModelForm):
    """
    主机过滤表单
    """
    class Meta:
        model = Host
        fields = ['product', 'cabinet', 'status']
        widgets = {
            'product': forms.Select(
                attrs={'class': 'form-control select2', 'style': "width: 100%;", "onchange": "change_info()"}
            ),
            'cabinet': forms.Select(
                attrs={'class': 'form-control select2', 'style': "width: 100%;", "onchange": "change_info()"}
            ),
            'status': forms.Select(
                attrs={'class': 'form-control select2', 'style': "width: 100%;", "onchange": "change_info()"}
            ),
        }


InLineSubNodeFormset = inlineformset_factory(Node, Node, exclude=['parent'], can_delete=True,
                                             widgets={'node_name': forms.TextInput(attrs={'class': 'form-control'}),
                                                      'verbose_name': forms.TextInput(attrs={'class': 'form-control'}),
                                                      'absolute_path': forms.TextInput(attrs={'class': 'form-control'}),
                                                      'remark': forms.Textarea(attrs={'class': 'form-control'})
                                                      })

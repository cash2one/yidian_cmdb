# -*- coding:utf8 -*-
# Author: Chenxc
# Email: chenxiaochen@yidian-inc.com
# Date: 2016-07-27
from django.http.response import HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from utils.mixins import MyPermissionRequiredMixin
from models import Manufacturer, ServerProduct, Idc, Cabinet, Node, Host, Nic
from forms import (
    ManufacturerForm, ServerProductForm, IdcForm, CabinetForm, NodeForm, HostForm, HostBatchCreationForm, HostFilterForm
)
from django.db.models import Count
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
import json
import xlrd


class ManufacturerListView(MyPermissionRequiredMixin, ListView):
    """
    经销商列表
    """
    permission_required = 'asset.read_manufacturer'

    model = Manufacturer
    ordering = '-created'
    template_name = 'asset/manufacturer.html'


class ManufacturerCreationView(MyPermissionRequiredMixin, CreateView):
    """
    创建厂商
    """
    permission_required = 'asset.add_manufacturer'

    model = Manufacturer
    form_class = ManufacturerForm
    template_name = 'asset/manufacturer_creation.html'
    success_url = reverse_lazy('asset-manufacturer-list')


class ManufacturerUpdateView(MyPermissionRequiredMixin, UpdateView):
    """
    创建厂商
    """
    permission_required = 'asset.change_manufacturer'

    model = Manufacturer
    form_class = ManufacturerForm
    pk_url_kwarg = 'manufacturer_id'
    template_name = 'asset/manufacturer_update.html'
    success_url = reverse_lazy('asset-manufacturer-list')


class ManufacturerDeletionView(MyPermissionRequiredMixin, DeleteView):
    """
    创建厂商
    """
    permission_required = 'asset.delete_manufacturer'

    model = Manufacturer
    pk_url_kwarg = 'manufacturer_id'
    success_url = reverse_lazy('asset-manufacturer-list')


class ServerProductListView(MyPermissionRequiredMixin, ListView):
    """
    服务器产品列表
    """
    permission_required = 'asset.read_serverproduct'

    model = ServerProduct
    ordering = '-created'
    template_name = 'asset/server_products.html'


class ServerProductCreationView(MyPermissionRequiredMixin, CreateView):
    """
    创建服务器产品
    """
    permission_required = 'asset.add_serverproduct'

    model = ServerProduct
    form_class = ServerProductForm
    template_name = 'asset/server_product_creation.html'
    success_url = reverse_lazy('asset-server_product-list')


class ServerProductUpdateView(MyPermissionRequiredMixin, UpdateView):
    """
    更新服务器产品
    """
    permission_required = 'asset.change_serverproduct'

    model = ServerProduct
    form_class = ServerProductForm
    pk_url_kwarg = 'server_product_id'
    template_name = 'asset/server_product_update.html'
    success_url = reverse_lazy('asset-server_product-list')


class ServerProductDeletionView(MyPermissionRequiredMixin, DeleteView):
    """
    删除服务器产品
    """
    permission_required = 'asset.delete_serverproduct'

    model = ServerProduct
    pk_url_kwarg = 'server_product_id'
    success_url = reverse_lazy('asset-server_product-list')


class IdcListView(MyPermissionRequiredMixin, ListView):
    """
    Idcs
    """
    permission_required = 'asset.read_idc'

    model = Idc
    queryset = Idc.objects.annotate(cabinet_total=Count('cabinets'))
    ordering = '-created'
    template_name = 'asset/idcs.html'


class IdcDetailView(MyPermissionRequiredMixin, DetailView):
    """
    idc 机房详情页面
    """
    permission_required = 'asset.read_idc'

    model = Idc
    pk_url_kwarg = 'idc_id'
    template_name = 'asset/idc_detail.html'


class IdcCreationView(MyPermissionRequiredMixin, CreateView):
    """
    创建IDC
    """
    permission_required = 'asset.add_idc'

    model = Idc
    form_class = IdcForm
    template_name = 'asset/idc_creation.html'
    success_url = reverse_lazy('asset-idc-list')


class IdcUpdateView(MyPermissionRequiredMixin, UpdateView):
    """
    更新IDC
    """
    permission_required = 'asset.change_idc'

    model = Idc
    form_class = IdcForm
    pk_url_kwarg = 'idc_id'
    template_name = 'asset/idc_update.html'
    success_url = reverse_lazy('asset-idc-list')


class IdcDeletionView(MyPermissionRequiredMixin, DeleteView):
    """
    删除机房
    """
    permission_required = 'asset.delete_idc'

    model = Idc
    pk_url_kwarg = 'idc_id'
    success_url = reverse_lazy('asset-idc-list')


class CabinetCreationView(MyPermissionRequiredMixin, CreateView):
    """
    创建机柜
    """
    permission_required = 'asset.add_cabinet'

    model = Cabinet
    form_class = CabinetForm
    template_name = 'asset/cabinet_creation.html'

    def get_success_url(self):
        return reverse_lazy('asset-idc-detail', kwargs={'idc_id': self.kwargs['idc_id']})

    def form_valid(self, form):
        idc = get_object_or_404(Idc, pk=self.kwargs['idc_id'])
        form.instance.idc = idc
        return super(CabinetCreationView, self).form_valid(form)


class CabinetUpdateView(MyPermissionRequiredMixin, UpdateView):
    """
    更新机柜
    """
    permission_required = 'asset.change_cabinet'

    model = Cabinet
    form_class = CabinetForm
    pk_url_kwarg = 'cabinet_id'
    template_name = 'asset/cabinet_update.html'

    def get_success_url(self):
        return reverse_lazy('asset-idc-detail', kwargs={'idc_id': self.kwargs['idc_id']})


class CabinetDeletionView(MyPermissionRequiredMixin, DeleteView):
    """
    删除机柜
    """
    permission_required = 'asset.delete_cabinet'

    model = Cabinet
    pk_url_kwarg = 'cabinet_id'

    def get_success_url(self):
        return reverse_lazy('asset-idc-detail', kwargs={'idc_id': self.kwargs['idc_id']})


class NodeListView(MyPermissionRequiredMixin, ListView):
    """
    业务节点列表
    """
    permission_required = 'asset.read_node'

    model = Node
    ordering = '-created'
    template_name = 'asset/nodes.html'

    def get_context_data(self, **kwargs):
        """
        添加 jstree 渲染数据
        """
        node_list = []
        for node in self.object_list:
            node_data_dict = {}

            if not node.parent:
                node_data_dict['parent'] = "#"
            else:
                node_data_dict['parent'] = str(node.parent.id)

            node_data_dict['id'] = str(node.id)
            node_data_dict['icon'] = "fa fa-folder fa-fw"
            node_data_dict['text'] = '%s' % node.verbose_name

            node_list.append(node_data_dict)

        nodes_json = json.dumps(node_list)
        context = super(NodeListView, self).get_context_data(**kwargs)
        context.setdefault('nodes_json', nodes_json)

        return context


class NodeCreationView(MyPermissionRequiredMixin, CreateView):
    """
    创建业务树节点
    """
    permission_required = 'asset.add_node'

    model = Node
    form_class = NodeForm
    template_name = 'asset/node_creation.html'
    success_url = reverse_lazy('asset-node-list')


class NodeUpdateView(MyPermissionRequiredMixin, UpdateView):
    """
    更新业务树节点
    """
    permission_required = 'asset.change_node'

    model = Node
    form_class = NodeForm
    pk_url_kwarg = 'node_id'
    template_name = 'asset/node_update.html'
    success_url = reverse_lazy('asset-node-list')


class NodeDeletionView(MyPermissionRequiredMixin, DeleteView):
    """
    删除业务节点
    """
    permission_required = 'asset.delete_node'

    model = Node
    pk_url_kwarg = 'node_id'
    success_url = reverse_lazy('asset-node-list')


class HostListView(MyPermissionRequiredMixin, ListView):
    """
    主机列表
    """
    permission_required = 'asset.read_host'

    model = Host
    ordering = '-created'
    template_name = 'asset/hosts.html'

    def get_getreq_qp(self):
        """
        获取GET请求的查询参数
        """
        filter_fields = ['product', 'cabinet', 'status']
        qp = {}
        for key in filter_fields:
            value = self.request.GET.get(key)
            if value:
                qp[key] = value
        return qp

    def get_queryset(self):
        queryset = super(HostListView, self).get_queryset()

        qp = self.get_getreq_qp()
        if qp:
            queryset = queryset.filter(**qp)

        return queryset

    def get_context_data(self, **kwargs):
        """
        """
        context = super(HostListView, self).get_context_data(**kwargs)
        qp = self.get_getreq_qp()

        context.setdefault('host_filter_form', HostFilterForm(initial=qp or {}))
        return context


class HostDetailView(MyPermissionRequiredMixin, DetailView):
    """
    主机详情
    """
    permission_required = 'asset.read_host'

    model = Host
    pk_url_kwarg = 'host_id'
    template_name = 'asset/host_detail.html'


class HostCreationView(MyPermissionRequiredMixin, TemplateView):
    """
    创建主机
    """
    permission_required = 'asset.add_host'

    single_host_creation_form_class = HostForm
    batch_host_creation_form_class = HostBatchCreationForm
    template_name = 'asset/host_creation.html'
    success_url = reverse_lazy('asset-host-list')

    def get(self, request, *args, **kwargs):
        kwargs.setdefault("single_host_creation_form", self.single_host_creation_form_class())
        kwargs.setdefault("batch_host_creation_form", self.batch_host_creation_form_class())
        return super(HostCreationView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form_args = {
            'data': self.request.POST,
            'files': self.request.FILES
        }

        if "submit_single" in request.POST:
            form = self.single_host_creation_form_class(**form_args)
            if not form.is_valid():
                return self.get(request, single_host_creation_form=form)
            form.save()
            return HttpResponseRedirect(self.success_url)

        elif "submit_batch" in request.POST:
            form = self.batch_host_creation_form_class(**form_args)
            if not form.is_valid():
                return self.get(request, batch_host_creation_form=form)

            instance = form.save()

            # 处理 Excel 批量添加主机
            excel = xlrd.open_workbook(instance.upload_excel.url)
            first_sheet = excel.sheet_by_index(0)

            for row_num in range(first_sheet.nrows):
                if row_num == 0:
                    continue
                row_content_list = first_sheet.row_values(row_num)

                an = row_content_list[0]
                sn = row_content_list[1]
                host_name = row_content_list[2]
                os = row_content_list[3]
                idc_name = row_content_list[4]
                cabinet_name = row_content_list[5]

                if row_content_list[6]:
                    cabinet_index = int(row_content_list[6])
                else:
                    cabinet_index = None

                nic_name = row_content_list[7]

                ipv4 = None
                if row_content_list[8]:
                    ipv4 = row_content_list[8]

                management_ip = None
                if row_content_list[9]:
                    management_ip = row_content_list[9]

                cabinet = None
                if idc_name and cabinet_name:
                    idc = get_object_or_404(Idc, name=idc_name)
                    cabinet = get_object_or_404(idc.cabinets.all(), name=cabinet_name)
                try:
                    host = Host.objects.create(
                        an=an, sn=sn, host_name=host_name, os=os, cabinet=cabinet, cabinet_index=cabinet_index,
                        management_ip=management_ip
                    )
                except IntegrityError:
                    form.add_error(None, u'批量添加主机失败!!!上传文件内容可能不符合规范或有重复数据被提交!!!')
                    return self.get(request, batch_host_creation_form=form)

                if host and nic_name or ipv4:
                    Nic.objects.create(host, nic_name=nic_name, ipv4=ipv4)

            return HttpResponseRedirect(self.success_url)
        return super(HostCreationView, self).get(request)


class HostUpdateView(MyPermissionRequiredMixin, UpdateView):
    """
    更新主机
    """
    permission_required = 'asset.change_host'

    model = Host
    form_class = HostForm
    pk_url_kwarg = 'host_id'
    template_name = 'asset/host_update.html'
    success_url = reverse_lazy('asset-host-list')


class HostDeletionView(MyPermissionRequiredMixin, DeleteView):
    """
    删除主机
    """
    permission_required = 'asset.delete_host'

    model = Host
    pk_url_kwarg = 'host_id'
    success_url = reverse_lazy('asset-host-list')


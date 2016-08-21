# -*- coding:utf8 -*-
# Author: Chenxc
# Email: chenxiaochen@yidian-inc.com
# Date: 2016-07-27
from django.conf.urls import url
from views import (
    ManufacturerListView, ManufacturerCreationView, ManufacturerUpdateView, ManufacturerDeletionView,
    ServerProductListView, ServerProductCreationView, ServerProductUpdateView, ServerProductDeletionView, IdcListView,
    IdcDetailView, IdcCreationView, IdcUpdateView, IdcDeletionView, CabinetCreationView, CabinetUpdateView,
    CabinetDeletionView, NodeListView, NodeCreationView, NodeUpdateView, NodeDeletionView, HostListView, HostDetailView,
    HostCreationView, HostUpdateView, HostDeletionView
)


urlpatterns = [
    # 厂商列表
    url(r'manufacturers/$', ManufacturerListView.as_view(), name='asset-manufacturer-list'),
    # 创建厂商
    url(r'manufacturer/creation/$', ManufacturerCreationView.as_view(), name='asset-manufacturer-creation'),
    # # 更新厂商
    url(r'manufacturer/update/(?P<manufacturer_id>\d+)/$', ManufacturerUpdateView.as_view(),
        name='asset-manufacturer-update'),
    # 删除厂商
    url(r'manufacturer/deletion/(?P<manufacturer_id>\d+)/$', ManufacturerDeletionView.as_view(),
        name='asset-manufacturer-deletion'),
    # 服务器产品列表
    url(r'server-product/$', ServerProductListView.as_view(), name='asset-server_product-list'),
    # 创建服务器产品
    url(r'server-product/creation/$', ServerProductCreationView.as_view(), name='asset-server_product-creation'),
    # 更新服务器产品
    url(r'server-product/update/(?P<server_product_id>\d+)/$', ServerProductUpdateView.as_view(),
        name='asset-server_product-update'),
    # 删除服务器产品
    url(r'server-product/deletion/(?P<server_product_id>\d+)/$', ServerProductDeletionView.as_view(),
        name='asset-server_product-deletion'),
    # 机房列表
    url(r'idc/$', IdcListView.as_view(), name='asset-idc-list'),
    # 机房详情
    url(r'idc/detail/(?P<idc_id>\d+)/$', IdcDetailView.as_view(), name='asset-idc-detail'),
    # 创建机房
    url(r'idc/creation/$', IdcCreationView.as_view(), name='asset-idc-creation'),
    # 更新机房信息
    url(r'idc/update/(?P<idc_id>\d+)/$', IdcUpdateView.as_view(), name='asset-idc-update'),
    # 删除机房
    url(r'idc/deletion/(?P<idc_id>\d+)/$', IdcDeletionView.as_view(), name='asset-idc-deletion'),
    # 创建机房机柜
    url(r'idc/(?P<idc_id>\d+)/cabinet/creation/$', CabinetCreationView.as_view(), name='asset-cabinet-creation'),
    # 更新机房机柜
    url(r'idc/(?P<idc_id>\d+)/cabinet/update/(?P<cabinet_id>\d+)/$', CabinetUpdateView.as_view(),
        name='asset-cabinet-update'),
    # 删除机房机柜
    url(r'idc/(?P<idc_id>\d+)/cabinet/deletion/(?P<cabinet_id>\d+)/$', CabinetDeletionView.as_view(),
        name='asset-cabinet-deletion'),
    # 业务节点列表
    url(r'node/$', NodeListView.as_view(), name='asset-node-list'),
    # 创建业务节点
    url(r'node/creation/$', NodeCreationView.as_view(), name='asset-node-creation'),
    # 更新业务节点
    url(r'node/update/(?P<node_id>\d+)/$', NodeUpdateView.as_view(), name='asset-node-update'),
    # 删除业务节点
    url(r'node/deletion/(?P<node_id>\d+)/$', NodeDeletionView.as_view(), name='asset-node-deletion'),
    # 主机列表
    url(r'host/$', HostListView.as_view(), name='asset-host-list'),
    # 主机详情
    url(r'host/detail/(?P<host_id>\d+)/$', HostDetailView.as_view(), name='asset-host-detail'),
    # 创建主机
    url(r'host/creation/$', HostCreationView.as_view(), name='asset-host-creation'),
    # 更新主机
    url(r'host/update/(?P<host_id>\d+)/$', HostUpdateView.as_view(), name='asset-host-update'),
    # 删除主机
    url(r'host/deletion/(?P<host_id>\d+)/$', HostDeletionView.as_view(), name='asset-host-deletion'),
]

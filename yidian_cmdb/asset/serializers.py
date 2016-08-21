# -*- coding:utf8 -*-
# Author: Chenxc
# Email: chenxiaochen@yidian-inc.com
# Date: 2016-08-10
from rest_framework import serializers
from models import Idc, Cabinet, ServerProduct, Host, Nic


class IdcSerializer(serializers.ModelSerializer):
    """
    机房信息序列化
    """
    class Meta:
        model = Idc
        exclude = ('created', 'changed')


class CabinetSerializer(serializers.ModelSerializer):
    """
    机柜信息序列化
    """
    class Meta:
        model = Cabinet
        exclude = ('created', 'changed')


class NicSerializer(serializers.ModelSerializer):
    """
    主机网卡信息序列化
    """
    class Meta:
        model = Nic
        exclude = ('host', 'created', 'changed')


class HostSerializer(serializers.ModelSerializer):
    """
    主机信息序列化
    """
    nics = NicSerializer(many=True)

    class Meta:
        model = Host
        exclude = ('created', 'changed')

    def create(self, validated_data):
        nics_data = validated_data.pop('nics')

        host = super(HostSerializer, self).create(validated_data)

        if nics_data:
            for nic_data in nics_data:
                Nic.objects.create(host=host, **nic_data)
        return host


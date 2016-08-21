# -*- coding:utf8 -*-
# Author: Chenxc
# Email: chenxiaochen@yidian-inc.com
# Date: 2016-08-10
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from serializers import IdcSerializer, CabinetSerializer, HostSerializer
from models import Idc, Cabinet, Host


class BatchCreationMixin(object):
    """
    支持批量创建记录
    """
    def create(self, request, *args, **kwargs):
        """
        #checks if post request data is an array initializes serializer with many=True
        else executes default CreateModelMixin.create function
        """
        is_many = isinstance(request.data, list)
        if not is_many:
            return super(BatchCreationMixin, self).create(request, *args, **kwargs)
        else:
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class IdcList(BatchCreationMixin, generics.ListCreateAPIView):
    """
    返回 Idc 列表或者 创建 Idc
    """
    queryset = Idc.objects.all()
    serializer_class = IdcSerializer

    # def create(self, request, *args, **kwargs):
    #     """
    #     #checks if post request data is an array initializes serializer with many=True
    #     else executes default CreateModelMixin.create function
    #     """
    #     is_many = isinstance(request.data, list)
    #     if not is_many:
    #         return super(IdcList, self).create(request, *args, **kwargs)
    #     else:
    #         serializer = self.get_serializer(data=request.data, many=True)
    #         serializer.is_valid(raise_exception=True)
    #         self.perform_create(serializer)
    #         headers = self.get_success_headers(serializer.data)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CabinetList(BatchCreationMixin, generics.ListCreateAPIView):
    """
    返回机柜列表或者创建机柜
    """
    queryset = Cabinet.objects.all()
    serializer_class = CabinetSerializer

    # def create(self, request, *args, **kwargs):
    #     """
    #     #checks if post request data is an array initializes serializer with many=True
    #     else executes default CreateModelMixin.create function
    #     """
    #     is_many = isinstance(request.data, list)
    #     if not is_many:
    #         return super(CabinetList, self).create(request, *args, **kwargs)
    #     else:
    #         serializer = self.get_serializer(data=request.data, many=True)
    #         serializer.is_valid(raise_exception=True)
    #         self.perform_create(serializer)
    #         headers = self.get_success_headers(serializer.data)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class HostList(BatchCreationMixin, generics.ListCreateAPIView):
    """
    返回主机列表或者创建主机
    """
    queryset = Host.objects.all()
    serializer_class = HostSerializer

    # def create(self, request, *args, **kwargs):
    #     """
    #     #checks if post request data is an array initializes serializer with many=True
    #     else executes default CreateModelMixin.create function
    #     """
    #     is_many = isinstance(request.data, list)
    #     if not is_many:
    #         return super(HostList, self).create(request, *args, **kwargs)
    #     else:
    #         serializer = self.get_serializer(data=request.data, many=True)
    #         serializer.is_valid(raise_exception=True)
    #         self.perform_create(serializer)
    #         headers = self.get_success_headers(serializer.data)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
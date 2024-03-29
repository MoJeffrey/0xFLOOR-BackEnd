#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Backend 
@File    ：CurrencyAPIs.py
@Author  ：MoJeffrey
@Date    ：2023/4/23 23:44 
"""
import traceback

from Backend.settings import RegularCheckTimeout_Log
from drf_yasg.utils import swagger_auto_schema
from loguru import logger
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import permissions, exceptions, serializers
from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView
from Order.models.OrderModels import Order, OrderSerializers
from Tools.ResponseSchema import ResponseSchemaMsg, ResponseSchemaCode

def RegularCheckTimeout():
    """
    定期確認質押
    :return:
    """
    logger.add(RegularCheckTimeout_Log, level="INFO", rotation="1 week")
    logger.info("進入")
    try:
        Order.CheckTimeout()
    except Exception as e:
        logger.info('发生错误，错误信息为：', e)
        logger.info(traceback.format_exc())
        return

class OrderItemObject:
    id: int = None
    num: int = None
    type: int = None

    def __init__(self, Object: dict):
        if Object is not None:
            self.__dict__ = Object.copy()

    def verify(self) -> bool:
        if self.id is None:
            return False

        if self.num is None or self.num < 1:
            return False

        if self.type is None:
            return False

        return True

class OrderList(ListAPIView):
    serializer_class = OrderSerializers
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    swagger_tags = ['订单管理']
    swagger = {
        "operation_summary": "Frontend 订单列表",
        "operation_description": "Frontend 订单列表",
        "tags": swagger_tags,
    }

    def verifyRequest(self):
        """
        :return:
        """
        verify = True
        for Item in ['page', 'orderType', 'limit']:
            if Item not in self.request.query_params:
                verify = False
                break

        if verify:
            return
        else:
            raise exceptions.ValidationError(detail={"msg": "缺少必要参数！"})

    @swagger_auto_schema(**swagger)
    def get(self, request, *args, **kwargs):
        self.verifyRequest()
        data = {
            "userId": self.request.user.id,
            "orderType": request.query_params['orderType'],
            "page": request.query_params['page'],
            "limit": request.query_params['limit']
        }

        result = Order.GetList(**data)
        return Response(result)

class OrderCreate(CreateAPIView):

    class CreateOrderRequest_body(serializers.Serializer):
        class orderItemList_body(serializers.Serializer):
            id = serializers.IntegerField(label='产品id')
            num = serializers.IntegerField(label='产品数量')
            type = serializers.IntegerField(label='产品类别')

        orderName = serializers.CharField(label='订单名称')
        RevenueAddressId = serializers.IntegerField(label='用戶的收益地址Id')
        orderItemList = serializers.ListSerializer(child=orderItemList_body(), label='订单内项目')

    serializer_class = OrderSerializers
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    swagger_tags = ['订单管理']
    swagger = {
        "operation_summary": "Frontend 添加订单",
        "operation_description": "Frontend 添加订单",
        "request_body": CreateOrderRequest_body,
        "responses": {
            400: ResponseSchemaMsg,
            200: ResponseSchemaCode
        },
        "tags": swagger_tags,
    }

    def verifyRequest(self):
        """
        :return:
        """
        verify = True
        for Item in ['orderName', 'orderItemList', 'pledgeProfitRatioId']:
            if Item not in self.request.data:
                verify = False
                break

        if verify:
            return
        else:
            raise exceptions.ValidationError(detail={"msg": "缺少必要参数！"})

    @swagger_auto_schema(**swagger)
    def post(self, request, *args, **kwargs):
        self.verifyRequest()

        ItemIdList = []
        ItemNumList = []
        ItemTypeList = []

        for Item in request.data['orderItemList']:
            obj = OrderItemObject(Item)
            if not obj.verify():
                raise exceptions.ValidationError(detail={"msg": "添加的产品错误！"})

            ItemIdList.append(str(obj.id))
            ItemNumList.append(str(obj.num))
            ItemTypeList.append(str(obj.type))

        data = {
            "userId": self.request.user.id,
            "orderName": request.data['orderName'],
            "ItemIdList": ItemIdList,
            "ItemNumList": ItemNumList,
            "ItemTypeList": ItemTypeList,
            "pledgeProfitRatioId": request.data['pledgeProfitRatioId']
        }
        result = Order.Create(**data)
        return Response(result)

class OrderDetails(GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    allowed_methods = ['POST']

    swagger_tags = ['订单管理']
    swagger = {
        "operation_summary": "Frontend 获取订单详情",
        "operation_description": "Frontend 获取订单详情",
        "tags": swagger_tags,
    }

    def verifyRequest(self):
        """
        :return:
        """
        verify = True
        for Item in ['orderId']:
            if Item not in self.request.data:
                verify = False
                break

        if verify:
            return
        else:
            raise exceptions.ValidationError(detail={"msg": "缺少必要参数！"})

    @swagger_auto_schema(**swagger)
    def post(self, request, *args, **kwargs):
        self.verifyRequest()
        data = {
            "userId": self.request.user.id,
            "orderId": request.data['orderId']
        }
        result = Order.GetDetails(**data)
        return Response(result)
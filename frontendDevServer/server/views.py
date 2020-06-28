from django.shortcuts import render, HttpResponse
from django.http import FileResponse
from django.db import models
from django.utils.http import http_date
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from .serializers import *
from .models import *
from django.conf import settings
import os,re,stat,mimetypes,json
import logging
logger = logging.getLogger('')

def index(request):
    print(request.META)
    return render(request, 'index.html', {})


# 下载大文件
def bigFile(request, path):
    fileName = settings.MEDIA_ROOT + path
    if not os.path.exists(fileName):
        return HttpResponse('你所访问的页面不存在', status=404)
    statobj = os.stat(fileName)
    # 获取文件的content_type
    content_type, encoding = mimetypes.guess_type(fileName)
    content_type = content_type or 'application/octet-stream'

    # 计算读取文件的起始位置
    start_bytes = re.search(
        r'bytes=(\d+)-', request.META.get('HTTP_RANGE', ''), re.S)
    start_bytes = int(start_bytes.group(1)) if start_bytes else 0

    # 打开文件并移动下标到起始位置，客户端点击继续下载时，从上次断开的点继续读取
    the_file = open(fileName, 'rb')
    the_file.seek(start_bytes, os.SEEK_SET)

    # status=200表示下载开始，status=206表示下载暂停后继续，为了兼容火狐浏览器而区分两种状态
    # FileResponse默认block_size = 4096，因此迭代器每次读取4KB数据
    response = FileResponse(
        the_file, content_type=content_type, status=206 if start_bytes > 0 else 200)

    # 'Last-Modified'表示文件修改时间，与'HTTP_IF_MODIFIED_SINCE'对应使用，参考：https://www.jianshu.com/p/b4ecca41bbff
    response['Last-Modified'] = http_date(statobj.st_mtime)

    # 这里'Content-Length'表示剩余待传输的文件字节长度
    if stat.S_ISREG(statobj.st_mode):
        response['Content-Length'] = statobj.st_size - start_bytes
    if encoding:
        response['Content-Encoding'] = encoding

    # 'Content-Range'的'/'之前描述响应覆盖的文件字节范围，起始下标为0，'/'之后描述整个文件长度，与'HTTP_RANGE'对应使用
    response['Content-Range'] = 'bytes %s-%s/%s' % (
        start_bytes, statobj.st_size - 1, statobj.st_size)

    # 'Cache-Control'控制浏览器缓存行为，此处禁止浏览器缓存
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    去除csrf检测
    """

    def enforce_csrf(self, request):
        return


# 访问房间列表（直接关联model），只允许Get操作
class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        serializer = RoomListSerializer(self.get_queryset(), many=True)
        try:
            orderlist = sorted(
                serializer.data, key=lambda x: int(x['name'], 16))
            return Response(data=orderlist, headers={'Access-Control-Allow-Origin': '*'})
        except ValueError:
            return Response(data=serializer.data, headers={'Access-Control-Allow-Origin': '*'})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, headers={'Access-Control-Allow-Origin': '*'})

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            logger.info('create new room')
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        logger.error('create new room error: {}'.format(serializer.errors))
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():
            logger.info('update new room')
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        logger.error('update new room error: {}'.format(serializer.errors))
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SoftwareViewSet(ModelViewSet):
    queryset = Software.objects.all()
    serializer_class = SoftwareSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)


# 访问设备状态列表，只允许Get操作，不允许其他
class RoomStatusViewSet(ModelViewSet):
    queryset = RoomStatus.objects.all()
    serializer_class = RoomStatusSerializer
    http_method_names = ['get']
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, headers={'Access-Control-Allow-Origin': '*'})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, headers={'Access-Control-Allow-Origin': '*'})


@csrf_exempt
def shutdown(request):
    logger.warn('client:{} request shutdown server, shutdown at 30s later'.format(request.META['REMOTE_ADDR']))
    os.system("shutdown -s -t 30")
    return HttpResponse(status=200)

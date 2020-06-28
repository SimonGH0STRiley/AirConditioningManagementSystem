from django.urls import path ,re_path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from .views import DeviceViewSet,DeviceStatusViewSet ,TrackerViewSet,updateTrackerLists,visitors

#配置路由表
router = DefaultRouter()
router.register(prefix='room',viewset=DeviceViewSet,base_name='room')
router.register(prefix='ac',viewset=DeviceStatusViewSet,base_name='ac')

#API_V1=[]
API_V1 = [
    path('updateRoomLists/',updateRoomLists),
]

API_V1.extend(router.urls)

urlpatterns = [
    re_path(r'^v1/',include(API_V1)),
]

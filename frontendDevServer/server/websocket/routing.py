from django.urls import path
from .consumers import MonitorConsumer 

websocket_urlpatterns=[
    path('ws/monitor/',MonitorConsumer)
]
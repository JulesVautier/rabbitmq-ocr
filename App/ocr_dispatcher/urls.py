from background_task import background
from django.urls import path

from .rpc_listener import ListenerRpc
from . import views

@background()
def listen():
    listener = ListenerRpc()
    listener.start()
listen.now()

urlpatterns = [
    path('', views.index, name='index'),
    path('compute/', views.ocr, name='ocr')
]


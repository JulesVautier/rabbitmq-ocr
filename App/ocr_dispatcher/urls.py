from background_task import background
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('compute/', views.ocr_view, name='ocr')
]


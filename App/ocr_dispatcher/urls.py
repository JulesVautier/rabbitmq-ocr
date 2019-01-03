from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('ocr/<string:filename>', views.ocr, name='ocr'),
    #path(r'^ocr/(?P<string>[\w\-]+)/$','polls.views.detail')
    path('compute/', views.ocr, name='ocr')
]


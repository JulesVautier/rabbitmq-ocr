from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.home, name='home'),
    path('', views.index, name='index'),
    path('compute/', views.ocr_view, name='ocr'),
    path('upload/', views.upload_file, name='upload'),
    url('uploads/simple/$', views.simple_upload, name='simple_upload'),
    url('uploads/form/$', views.model_form_upload, name='model_form_upload'),
]


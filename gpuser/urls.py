from django.urls import path

from . import views

urlpatterns = [
    path("", views.gpu, name="gpu-status-page"),
    path("gpu/", views.gpu),
    path("gpu_status/", views.get, name="gpu-status-api"),
]

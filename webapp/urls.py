from django.urls import path

from . import views

urlpatterns = [
    path('redpanda', views.index, name='index'),
    path('index', views.indexBeforeIndex, name='indexBeforeIndex')
]
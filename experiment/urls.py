
from django.urls import path

from . import views

urlpatterns = [

    path('index/', views.indexView, name='index'),
    path('', views.dashoboardView, name='dashoboard'),

]

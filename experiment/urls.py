
from django.urls import path

from . import views

urlpatterns = [

    path('index/', views.indexView, name='index'),
    path('', views.dashboardView, name='dashboard'),

    path('sign-in/', views.signInView, name='sign-in'),
    path('sign-up/', views.signUpView, name='sign-up'),
    path('sign-out/', views.signOutView, name='sign-out'),


]

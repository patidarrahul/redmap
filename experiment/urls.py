
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [

    path('index/', views.indexView, name='index'),
    path('', views.dashboardView, name='dashboard'),

    path('sign-in/', views.signInView, name='sign-in'),
    path('sign-up/', views.signUpView, name='sign-up'),
    path('sign-out/', views.signOutView, name='sign-out'),


    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='password-reset.html'), name='reset_password'),
    path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(template_name='password-reset-done.html') , name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password-reset-confirm.html'), name='password_reset_confirm'),
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view( template_name='password-reset-complete.html') , name='password_reset_complete'),


]

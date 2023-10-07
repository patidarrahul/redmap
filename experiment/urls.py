
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import  inventoryView, addInventoryView, updateInventoryView, formulationView
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


    path('inventory/', inventoryView.as_view(), name='inventory'),
    path('inventory/add/', addInventoryView.as_view(), name='add-inventory'),
    path('inventory/update/<str:pk>/', updateInventoryView.as_view(),
         name='update-inventory'),
    path('inventory/status/<str:pk>/',
         views.markascomplete, name='mark-as-complete'),
    path('item/add', views.addItemView, name='add-item'),
    path('supplier/add', views.addSupplierView, name='add-supplier'),


    path('formulation/', formulationView.as_view(), name='formulation'),

    path('formulation/add/', views.addformulationView, name='add-formulation'),
    path('formulation/update/<str:pk>/', views.updateformulationView,
         name='update-formulation'),

]


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

    path('profile/', views.profileView, name='profile'),
     path('profile/update/', views.updateUserProfileView, name='update-profile'),
    
    
    path('project/add/', views.addProjectView, name='add-project'),
    path('project/update/<str:pk>/',
         views.updateProjectView, name='update-project'),
    
    path('experiment/add/<str:pk>/',
         views.addExperimentView, name='add-experiment'),


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


    path('formulation/', views.formulationView, name='formulation'),

    path('formulation/add/', views.addformulationView, name='add-formulation'),
    path('formulation/update/<str:pk>/', views.updateformulationView,
         name='update-formulation'),

    path('layer/route/<str:pk>/', views.layerRouter, name='layer-router'),
    path('layer/', views.LayerView.as_view(), name='layer'),
    path('layer/spin-coated-layer/add',
         views.addSpinCoatedLayer, name='add-spin-coated-layer'),
    path('layer/spin-coated-layer/update/<str:pk>/',
         views.updateSpinCoatedLayer, name='update-spin-coated-layer'),

    path('layer/spin-coated-layer/spin-program/add',
         views.addSpinProgram, name='add-spin-program'),
    path('layer/spin-coated-layer/spin-step/add',
         views.addSpinStep, name='add-spin-step'),
    path('layer/thermal-evaporated-layer/add' , views.addThermalEvaporatedLayerView, name='add-thermal-evaporated-layer'),
    path('layer/thermal-evaporated-layer/update/<str:pk>/' , views.updateThermalEvaporatedLayerView, name='update-thermal-evaporated-layer'),

# stack urls 
     path('stack/', views.StackView, name='stack'),
    path('stack/add/', views.addStackView, name='add-stack'),
    path('stack/update/<str:pk>/', views.updateStackView, name='update-stack'),

     

]

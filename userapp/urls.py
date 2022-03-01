from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name=''),
    path('login', views.ulogin, name='login'),
    path('register', views.uregister, name='register'),
    path('dashboard', views.udashbaord, name='dashboard'),
    path('add-consignment', views.addconsign, name='add-consignment'),
    path('logout', views.ulogout, name='logout'),

    path('payment-success/<pk>/', views.paystatus, name="payment-success"),



    # Url for Vendor Operations and view

    path('vendor-login', views.vendorlogin, name='vendor-login'),
    path('vendor-register', views.vendorregister, name='vendor-register'),
    path('vendor', views.vendor, name='vendor'),
    path('add-vehicle', views.addvehicle, name='add-vehicle'),
    path('add-driver', views.add_driver, name='add-driver'),
    path('update-status/<pk>/', views.update_status, name='update-status'),
    path('add-tvride', views.add_tvride, name='add-tvride'),



]

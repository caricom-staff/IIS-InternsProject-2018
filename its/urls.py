from django.urls import path
from django.conf.urls import url
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('inventory/', views.inventory, name='inventory'),
    path('staff/', views.staff, name='staff'),
    path('add/', views.add, name='add'),
    path('remove/', views.remove, name='remove'),
    path('transfer/', views.transfer, name='transfer'),
    path('dispose/', views.dispose, name='dispose'),
    path('update/', views.update, name='update'),
    path('/item/<key>/', views.item, name='item')
]
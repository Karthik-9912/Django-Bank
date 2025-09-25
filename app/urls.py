from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name='index'),
    path('create/',views.create,name='create'),
    path('pin/',views.pin,name='pin'),
    path('validate/',views.validate,name='validate'),
    path('set/',views.set_pin,name='set'),
    path('deposit/',views.deposit,name='deposit'),
    path('balance/',views.balance,name='balance'),
]
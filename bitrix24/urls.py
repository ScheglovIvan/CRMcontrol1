from django.urls import path

from . import views

urlpatterns = [
    path('UpdateDeal/', views.index, name='index'),
]
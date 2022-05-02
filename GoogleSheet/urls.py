from django.urls import path

from . import views

urlpatterns = [
    path('NewOrder/', views.index, name='index'),
]
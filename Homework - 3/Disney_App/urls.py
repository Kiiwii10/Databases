from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Query_Results', views.Query_Results, name='Query_Results'),
    path('Add_a_Movie', views.Add_a_Movie, name='Add_a_Movie'),
    path('left', views.left, name='left'),
    path('Home', views.Home, name='Home'),
]
# index的urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.teachers),
    #path('oneYearInfo/', views.oneYearInfo)
]

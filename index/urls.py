# index的urls.py
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('logout/', views.logout_view, name='logout'),
]
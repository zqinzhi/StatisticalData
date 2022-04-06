# user的urls.py
from django.urls import path
from . import views
urlpatterns = [
    path('login.html', views.loginView, name='login')
]
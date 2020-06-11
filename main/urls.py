from django.urls import path, include
from rest_framework import routers
from .views import index


urlpatterns = [
    path('', index, name='index'),
]




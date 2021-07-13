from django.urls import path,include
from .views import *
urlpatterns = [
    path('',Register,name="register"),
    path('login/',login,name="login"),
    path('logout/',logout,name="logout")
]

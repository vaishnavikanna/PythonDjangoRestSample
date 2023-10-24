from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('login/', views.login),
    path('callback/', views.callback),
    path('users/', views.getUsers),
    path('logout/', views.logout),
    path('logoutdisplay/', views.logout_display),
]
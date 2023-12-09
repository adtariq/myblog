from typing import Any
from django.urls import path,URLPattern,URLResolver
from . import views

app_name = 'accounts'  # Add this line to specify the app namespace

urlpatterns: list[URLPattern | URLResolver] = [
    # path(route='', view=views.home,name="home"),
    path(route='register/', view=views.register, name='register'),
    path(route='login/', view=views.login_view, name='login'),
    path(route='logout/', view=views.logout_view, name='logout'),
    path('password-reset/', views.password_reset, name='password_reset'),
    path('password-reset/confirm/', views.password_reset_confirm, name='password_reset_confirm'),
    path('password-reset/complete/', views.password_reset_complete, name='password_reset_complete'),
]
 
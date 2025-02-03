from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.Login.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile_view, name='profile'),
    path('notes/', views.notes, name='notes'),
    path('info/', views.user_info, name='info'),
    path('settings/', views.settings_view, name='accountsettings'), 
    path('change_password/', views.change_password, name='change_password'),
    path('stockanalysis/', views.analysis_view, name='analysis'),
    path('forecast/', views.forecast_view, name='forecast'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name="accounts/login.html"), name='login'),
    
]

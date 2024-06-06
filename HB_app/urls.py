from django.contrib.auth import views as auth_views
from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('subscribe/<uuid:subscribed_to_id>/', views.subscribe, name='subscribe'),
    path('unsubscribe/<uuid:unsubscribed_to_id>/', views.unsubscribe, name='unsubscribe'),
    path('clients/', views.client_list, name='client_list'),
    path('notification_settings/', views.notification_settings, name='notification_settings'),
]
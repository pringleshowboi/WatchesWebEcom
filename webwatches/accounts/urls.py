from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'accounts' 

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('', views.accounts_home, name='home'),
    path('logout/', views.custom_logout, name='logout'),
]

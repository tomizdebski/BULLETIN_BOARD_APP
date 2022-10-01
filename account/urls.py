from django.urls import path
from account import views


urlpatterns = [

    path('login/', views.user_login, name='login')
]
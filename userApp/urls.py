from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),

    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('reset_pwd/', views.ResetPasswordView.as_view(), name='reset_pwd'),
    # path('dashboard/', views.dashboard_redirect, name='dashboard'),
]
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),

    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('reset_pwd/', views.ResetPasswordView.as_view(), name='reset_pwd'),
    path('code_confirm/', views.ConfirmationCodeView.as_view(), name='code_confirm'),
    path('dashboard/', views.dashboard_redirect, name='dashboard'),
    path('dashboard/user/', views.user_home_page, name='user_home_page'),
    path('dashboard/sponsor/', views.sponsor_dashboard, name='sponsor_dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
]
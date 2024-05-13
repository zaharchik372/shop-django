from django.urls import path, include

from account import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('login_main/', views.login_main, name='login_main'),
    path('employee_reg_admin/', views.admin_employee, name='admin_employee'),
    ]


from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from account import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('login_main/', views.login_main, name='login_main'),
    path('employee_reg_admin/', views.admin_employee, name='admin_employee'),
    path('admin_zakaz_for_client/<int:order_id>/', views.order_detail, name='order_detail'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('employee_tovar_reg_admin/', views.employee_tovar_reg_admin, name='employee_tovar_reg_admin'),
    path('admin_tovar_for_admin/<int:product_id>/', views.admin_tovar_for_admin, name='admin_tovar_for_admin'),
    path('create_product/', views.create_product, name='create_product'),
    path('search/', views.search_products_vulnerable, name='search_service'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('zakaz_clienta/<int:order_id>/', views.client_order_detail, name='client_order_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# aasddddmin1@test.ru
from django.urls import path

from cart import views
from cart.views import service_execution_list, edit_service_execution

app_name = 'cart'

urlpatterns = [
    path('order/', views.view_order, name='order'),
    path('add/', views.add_to_cart, name='add_to_cart',),
    path('', views.view_cart, name='cart',),
    path('service-executions/', service_execution_list, name='service_execution_list'),
    path('service-executions/edit/<int:pk>/', edit_service_execution, name='edit_service_execution'),
    path('service-executions/create/', views.create_service_execution, name='create_service_execution'),

]
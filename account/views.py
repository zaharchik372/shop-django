import os
import subprocess
from django.db import connection
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from .forms import *
from cart.models import Order, ProductsInOrder, ServiceExecution
from django.db.models import Sum
import logging
from catalog.models import Product
from django.http import Http404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.phone = user_form.cleaned_data.get('phone')
            new_user.first_name = user_form.cleaned_data.get('first_name')  # Сохраните имя
            new_user.last_name = user_form.cleaned_data.get('last_name')  # Сохраните фамилию
            new_user.save()
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


def login_main(request):
    login_form = CustomAuthenticationForm(request, request.POST)
    if request.method == 'POST':

        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        login_form = CustomAuthenticationForm()
    return render(request, 'account/login.html', {'login_form': login_form})


def staff_member_required_view(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return view_func(request, *args, **kwargs)

    return _wrapped_view_func


@user_passes_test(lambda u: u.is_staff, login_url='login')
def admin_employee(request):
    orders = Order.objects.all().order_by('-created')
    orders_with_totals = []
    for order in orders:
        quantity = ProductsInOrder.objects.filter(order=order).count()
        total_price = ProductsInOrder.objects.filter(order=order).aggregate(total=Sum('total_price'))['total'] or 0
        orders_with_totals.append({
            'order': order,
            'quantity': quantity,
            'total_price': total_price
        })
    return render(request, 'account/employee_admin.html', {'orders_with_totals': orders_with_totals})


@user_passes_test(lambda u: u.is_staff, login_url='login')
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    products_in_order = ProductsInOrder.objects.filter(order=order)
    total_price = products_in_order.aggregate(total=Sum('total_price'))['total'] or 0

    customer = order.customer

    if request.method == "POST":
        formset = ProductsInOrderFormset(request.POST, instance=order)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                if instance.product:
                    instance.total_price = instance.product.price * instance.quantity
                logger.debug(f"Saving: {instance.product} - {instance.quantity} - {instance.total_price}")
                instance.save()
            formset.save()

            # Обновление общей суммы заказа
            order.all_total_price = ProductsInOrder.objects.filter(order=order).aggregate(total=Sum('total_price'))[
                                        'total'] or 0
            order.save()

            return redirect('admin_employee')  # Перенаправление на страницу employee_admin после сохранения
        else:
            logger.debug(f"Formset is not valid: {formset.errors}")
    else:
        formset = ProductsInOrderFormset(instance=order)

    return render(request, 'account/zakaz_client_detail.html', {
        'order': order,
        'formset': formset,
        'total_price': total_price,
        'products_in_order': products_in_order,
        'customer': customer,
    })


# @user_passes_test(lambda u: u.is_staff, login_url='login')
# def admin_panel(request):
#     result = None
#     if request.method == 'POST':
#         command = request.POST.get('command')
#         if command:
#             try:
#                 # Установим переменные окружения для управления локалью и кодировкой
#                 env = os.environ.copy()
#                 env['PYTHONIOENCODING'] = 'utf-8'
#                 env['LC_ALL'] = 'ru_RU.UTF-8'
#
#                 # Выполнение команды с установкой кодировки
#                 full_command = f'chcp 65001 & {command}'
#                 process = subprocess.Popen(
#                     full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env
#                 )
#                 stdout, stderr = process.communicate()
#                 encoding = 'utf-8'
#                 if process.returncode == 0:
#                     result = stdout.decode(encoding, errors='ignore')
#                 else:
#                     result = stderr.decode(encoding, errors='ignore')
#             except Exception as e:
#                 result = str(e)
#     return render(request, 'account/admin_panel.html', {'result': result})

import re
@user_passes_test(lambda u: u.is_staff, login_url='login')
def admin_panel(request):
    result = None
    if request.method == 'POST':
        command = request.POST.get('command')
        if command:
            # Проверка команды на соответствие шаблону "ping [допустимый адрес]"
            if re.match(r'^ping\s+[\w\.-]+$', command.strip()):
                try:
                    # Установим переменные окружения для управления локалью и кодировкой
                    env = os.environ.copy()
                    env['PYTHONIOENCODING'] = 'utf-8'
                    env['LC_ALL'] = 'ru_RU.UTF-8'

                    # Выполнение команды с установкой кодировки
                    full_command = f'chcp 65001 & {command}'
                    process = subprocess.Popen(
                        full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env
                    )
                    stdout, stderr = process.communicate()
                    encoding = 'utf-8'
                    if process.returncode == 0:
                        result = stdout.decode(encoding, errors='ignore')
                    else:
                        result = stderr.decode(encoding, errors='ignore')
                except Exception as e:
                    result = str(e)
            else:
                result = "Недопустимая команда. Разрешены только команды ping."
    return render(request, 'account/admin_panel.html', {'result': result})


@user_passes_test(lambda u: u.is_staff, login_url='login')
def employee_tovar_reg_admin(request):
    products = Product.objects.all()
    return render(request, 'account/employee_tovar_reg_admin.html', {'products': products})


@user_passes_test(lambda u: u.is_staff, login_url='login')
def admin_tovar_for_admin(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('employee_tovar_reg_admin')
    else:
        form = ProductForm(instance=product)
    return render(request, 'account/admin_tovar_for_admin.html', {'form': form, 'product': product})


@user_passes_test(lambda u: u.is_staff, login_url='login')
def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('employee_tovar_reg_admin')
    else:
        form = ProductForm()
    return render(request, 'account/create_product.html', {'form': form})


# @csrf_exempt
# def search_products_vulnerable(request):
#     query = request.GET.get('q', '')
#     if query:
#         query = query.capitalize()
#     products = []
#
#     if query:
#         raw_query = f"SELECT p.*, c.slug as category_slug FROM catalog_product p JOIN catalog_category c " \
#                     f"ON p.category_id = c.id WHERE p.title LIKE '%%{query}%%'"
#         with connection.cursor() as cursor:
#             cursor.execute(raw_query)
#             columns = [col[0] for col in cursor.description]
#             for row in cursor.fetchall():
#                 product = dict(zip(columns, row))
#                 product['image'] = f"/media/{product['image']}"
#                 products.append(product)
#
#     if request.is_ajax():
#         return JsonResponse({'products': products})
#
#     return render(request, 'catalog/search_products.html', {'products': products, 'query': query})
from django.db.models import Q


@csrf_exempt
def search_products_vulnerable(request):
    query = request.GET.get('q', '')
    products = []

    if query:
        query = query.capitalize()
        products = Product.objects.filter(Q(title__icontains=query))

    product_list = []
    for product in products:
        product_list.append({
            'id': product.id,
            'title': product.title,
            'subtitle': product.subtitle,
            'description': product.description,
            'price': product.price,
            'image': f"/media/{product.image}" if product.image else '',
            'category_slug': product.category.slug,
            'slug': product.slug
        })

    if request.is_ajax():
        return JsonResponse({'products': product_list})

    return render(request, 'catalog/search_products.html', {'products': product_list, 'query': query})


@login_required
def user_dashboard(request):
    account_user = User.objects.get(id=request.user.id)
    orders = Order.objects.filter(customer=account_user)
    orders_max = ProductsInOrder.objects.filter()
    return render(request, 'account/user_dashboard.html', {'account_user': account_user,
                                                           'orders': orders, 'orders_max': orders_max})


def client_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    products_in_order = order.productsinorder_set.all()
    service_execution = order.serviceexecution_set.first()

    return render(request, 'account/zakaz_clienta_order_detail.html', {
        'order': order,
        'products_in_order': products_in_order,
        'service_execution': service_execution,
    })

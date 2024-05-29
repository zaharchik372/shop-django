from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from account.models import User
from cart.models import Order, ProductsInOrder, ServiceExecution
from catalog.models import Product
from cart.forms import ServiceExecutionForm, CreateServiceExecutionForm
from django.http import Http404


def add_to_cart(request):
    path = request.GET.get('next')

    if request.method == 'POST':
        product_id = request.GET.get('product_id')

        if 'cart' not in request.session:
            request.session['cart'] = {}

        cart = request.session.get('cart')

        if product_id in cart:
            cart[product_id]['quantity'] += 1

        else:
            cart[product_id] = {
                'quantity': 1
            }

    request.session.modified = True
    return redirect(path)


def view_cart(request):
    path = request.GET.get('next')

    context = {
        'next': path,
    }

    cart = request.session.get('cart', None)

    if cart:
        products = {}
        all_total_price = 0  # Инициализируем общую сумму
        product_list = Product.objects.filter(pk__in=cart.keys()).values('id', 'title', 'subtitle', 'price')

        for product in product_list:
            products[str(product['id'])] = product

        for key in cart.keys():
            cart[key]['product'] = products[key]
            cart[key]['total_price'] = products[key]['price'] * cart[key]['quantity']
            all_total_price += cart[key]['total_price']  # Добавляем цену к общей сумме

        context['cart'] = cart
        context['all_total_price'] = all_total_price  # Добавляем общую сумму в контекст

    return render(request, 'cart/cart.html', context)


@login_required(login_url='login')
def view_order(request):
    if request.method == 'POST':
        user_id = request.user.pk
        customer = User.objects.get(pk=user_id)

        cart = request.session.get('cart', {})
        all_total_price = 0

        if len(cart) > 0:
            order = Order.objects.create(customer=customer)
            for key, value in cart.items():
                product = Product.objects.get(pk=key)
                quantity = value['quantity']
                total_price = product.price * quantity
                all_total_price += total_price
                ProductsInOrder.objects.create(order=order, product=product, quantity=quantity, total_price=total_price)

            order.all_total_price = all_total_price
            order.save()

            request.session['cart'] = {}
            request.session.modified = True

            messages.success(request, 'Ваш заказ принят в работу!')

    return redirect('cart:cart')


# Проверка прав доступа
def staff_member_required_view(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return view_func(request, *args, **kwargs)

    return _wrapped_view_func


@user_passes_test(lambda u: u.is_staff, login_url='login')
def service_execution_list(request):
    service_executions = ServiceExecution.objects.all()
    return render(request, 'cart/service_execution_list.html', {'service_executions': service_executions})


@user_passes_test(lambda u: u.is_staff, login_url='login')
def edit_service_execution(request, pk):
    service_execution = get_object_or_404(ServiceExecution, pk=pk)
    if request.method == "POST":
        execution_date = request.POST.get('execution_date')
        form = ServiceExecutionForm(request.POST, instance=service_execution)
        if form.is_valid():
            service_execution.execution_date = execution_date  # Обновляем дату выполнения
            form.save()
            return redirect('cart:service_execution_list')
    else:
        form = ServiceExecutionForm(instance=service_execution)
    return render(request, 'cart/service_execution_form.html', {'form': form, 'service_execution': service_execution})


@user_passes_test(lambda u: u.is_staff, login_url='login')
def create_service_execution(request):
    if request.method == "POST":
        form = CreateServiceExecutionForm(request.POST)
        order_id = request.POST.get('order')
        order = get_object_or_404(Order, id=order_id)
        if ServiceExecution.objects.filter(order=order).exists():
            form.add_error('order', 'Выполнение услуги для этого заказа уже существует.')
        if form.is_valid():
            service_execution = form.save(commit=False)
            service_execution.order = order
            service_execution.save()
            return redirect('cart:service_execution_list')
    else:
        form = CreateServiceExecutionForm()
    return render(request, 'cart/service_create_form.html', {'form': form})

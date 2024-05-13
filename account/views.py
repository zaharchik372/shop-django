from django.contrib.auth import authenticate, login
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .forms import *
from cart.models import Order, ProductsInOrder

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


def admin_employee(request):
    order = Order


    return render(request, 'account/employee_admin.html'), {'order': order}

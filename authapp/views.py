from django.shortcuts import render, redirect
from django.contrib import messages

from pharmacy_delivery.apps.orm.BaseManager import BaseManager
from .models import User
from .utils import hash_password, check_password

def register_user(request):
    if request.method == 'POST':
        name = request.POST['name']
        surname = request.POST['surname']
        birth_date = request.POST['birth_date']
        login = request.POST['login']
        password = request.POST['password']
        hashed_password = hash_password(password)

        try:
            BaseManager.set_connection()
            User.objects.insert(
                value={
                    'name': name,
                    'surname': surname,
                    'birth_date': birth_date,
                    'login': login,
                    'password': hashed_password,
                    'role_id': 1
                })
            messages.success(request, "Registration successful!")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Error during registration: {e}")
    return render(request, 'register.html')


def login_user(request):
    if request.method == 'POST':
        login = request.POST['login']
        password = request.POST['password']

        BaseManager.set_connection()
        users = User.objects.select('id', 'password', condition=f'login = \'{login}\'')
        if len(users) == 0:
            messages.error(request, f"Error during login: no users with such login")
            return render(request, 'login.html')
        user = users[0]
        if user and check_password(password, user['password']):
            request.session['user_id'] = user['id']
            messages.success(request, "Login successful!")
            return redirect("index")
        messages.error(request, "Invalid credentials")
    return render(request, 'login.html')

def logout_user(request):
    request.session.flush()
    messages.success(request, "Logged out successfully!")
    return redirect('login')

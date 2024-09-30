from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import SignUpForm
from .models import Record


# Create your views here.


def home(request):
    records = Record.objects.all()
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # Authenticating user
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "You are now logged in")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('home')
    else:
        return render(request, 'website/home.html', {'records': records})


# def login_user(request):
#     pass


def logout_user(request):
    logout(request)
    messages.success(request, "You are now logged out")
    return redirect('home')


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Account created successfully")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'website/register.html', {'form': form})
    return render(request, 'website/register.html', {'form': form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        return render(request, 'website/record.html', {'record': record})
    else:
        return redirect('home')


def delete_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        record.delete()
        messages.success(request, "Record deleted successfully")
        return redirect('home')
    else:
        return redirect('home')


def update_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        if request.method == "POST":
            record.first_name = request.POST['first_name']
            record.last_name = request.POST['last_name']
            record.email = request.POST['email']
            record.phone = request.POST['phone']
            record.save()
            messages.success(request, "Record updated successfully")
            return redirect('home')
        else:
            return render(request, 'website/update_record.html', {'record': record})
    else:
        return redirect('home')

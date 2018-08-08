from django.shortcuts import render
from django.utils import timezone
from .models import Inventory, Staff, Add, Remove, Transfer, Dispose

def dashboard(request):
    return render(request, 'its/index.html', {})

def inventory(request):
    inventorys = Inventory.objects.all()
    return render(request, 'its/inventory.html', {'inventorys': inventorys})

def staff(request):
    return render(request, 'its/staff.html', {})

def add(request):
    return render(request, 'its/add.html', {})

def remove(request):
    return render(request, 'its/remove.html', {})

def transfer(request):
    return render(request, 'its/transfer.html', {})

def dispose(request):
    return render(request, 'its/dispose.html', {})

def login(request):
    return render(request, 'its/login.html', {})
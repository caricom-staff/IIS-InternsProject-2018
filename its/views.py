from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Inventory, Staff, Add, Remove, Transfer, Dispose

def dashboard(request):
    return render(request, 'its/index.html', {})

@csrf_exempt
def inventory(request):
    if request.method == 'POST':
        add=Inventory()
        add.manufacture_name = request.POST.get('manufacture_name')
        add.model_name = request.POST.get('model_name')
        add.device_type = request.POST.get('device_type')
        add.serial_number = request.POST.get('serial_number')
        add.location = request.POST.get('location')
        add.proprietor = request.POST.get('proprietor')
        add.status = request.POST.get('status')
        add.save()

        inventorys = Inventory.objects.all()
        return render(request, 'its/inventory.html', {'inventorys': inventorys})
    else:
        inventorys = Inventory.objects.all()
        return render(request, 'its/inventory.html', {'inventorys': inventorys})

def staff(request):
    return render(request, 'its/staff.html', {})

@csrf_exempt
def add(request):
    if request.method == 'POST':
        add=Inventory()
        add.manufacture_name = request.POST.get('manufacture_name')
        add.model_name = request.POST.get('model_name')
        add.device_type = request.POST.get('device_type')
        add.serial_number = request.POST.get('serial_number')
        add.location = request.POST.get('location')
        add.proprietor = request.POST.get('proprietor')
        add.status = request.POST.get('status')
        add.save()

        adddata = {
            'manufacture_name': add.manufacture_name,
            'model_name': add.model_name,
            'device_type': add.device_type,
            'serial_number': add.serial_number,
            'location': add.location,
            'proprietor': add.proprietor,
            'status': add.status,
        }

        return render(request, 'add.html', {'adddata': adddata})
    else:
        return render(request, 'its/add.html', {})
    

def remove(request):
    inventorys = Inventory.objects.all()
    return render(request, 'its/remove.html', {'inventorys': inventorys})

def transfer(request):
    inventorys = Inventory.objects.all()
    return render(request, 'its/transfer.html', {'inventorys': inventorys})

def dispose(request):
    inventorys = Inventory.objects.all()
    return render(request, 'its/dispose.html', {'inventorys': inventorys})

def login(request):
    return render(request, 'its/login.html', {})

def search(request):
    inventorys = Inventory.objects.all()
    if request.method =='GET':
        search_query = request.GET.get('search_box', None)
        inventorys = inventorys.filter(manufacture_name__icontains=search_query) | inventorys.filter(model_name__icontains=search_query) | inventorys.filter(device_type__icontains=search_query) | inventorys.filter(serial_number__icontains=search_query) | inventorys.filter(location__icontains=search_query) | inventorys.filter(proprietor__icontains=search_query)
        return render(request, 'inventory.html', {'inventorys': inventorys})
    else:
        return render(request, 'its/inventory.html', {'inventorys': inventorys})
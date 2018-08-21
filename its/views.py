from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views.generic import ListView
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Inventory, Staff, Transactions

def dashboard(request):
    return render(request, 'its/index.html', {})

@csrf_exempt
def inventory(request):
    inventory = Inventory.objects.all()
    if request.GET.get('search'):
        search_query = request.GET.get('search')
        inventorys = inventory.filter(manufacture_name__icontains=search_query) | inventory.filter(model_name__icontains=search_query) | inventory.filter(device_type__icontains=search_query) | inventory.filter(serial_number__icontains=search_query)
        result = inventorys.count()
        if result == 0:
            inventorys = Inventory.objects.all()
            return render(request, 'its/inventory.html', {'inventorys': inventorys, 'result': result})    
        else:
            return render(request, 'its/inventory.html', {'inventorys': inventorys, 'result': result})
    else:
        display = 'd-none'
        page = request.GET.get('page', 1)

        paginator = Paginator(inventory, 15)
        try:
            inventorys = paginator.page(page)
        except PageNotAnInteger:
            inventorys = paginator.page(paginator.num_pages)
        return render(request, 'its/inventory.html', {'display':display, 'inventorys': inventorys})

def staff(request):
    return render(request, 'its/staff.html', {})

@csrf_exempt
def add(request):
    display1 = 'd-none'
    if request.method == 'POST':
        manufacture_name = request.POST.get('manufacture_name')
        model_name = request.POST.get('model_name')
        device_type = request.POST.get('device_type')
        serial_number = request.POST.get('serial_number')
        location = request.POST.get('location')
        proprietor = request.POST.get('proprietor')
        status = request.POST.get('status')
        operation = 'Add'
        
        new_item = Inventory(manufacture_name=manufacture_name, model_name=model_name, device_type=device_type, serial_number=serial_number)
        new_item.save()

        iid = Inventory.objects.get(serial_number=serial_number)
        add_transaction = Transactions(iid = iid, operation = operation, location = location, proprietor = proprietor, status = status)
        add_transaction.save()
        adddata = {
            'manufacture_name': manufacture_name,
            'model_name': model_name,
            'device_type': device_type,
            'serial_number': serial_number,
            'location': location,
            'proprietor': proprietor,
            'status': status,
        }
        return render(request, 'its/add.html', {'adddata': adddata})
    else:
        return render(request, 'its/add.html', {'display1': display1})
    
@csrf_exempt
def remove(request):

    if request.method == 'POST':
        display = 'd-none'
        iid = request.POST.get('item_row', 0)
        if iid == 0:
            items = []
            selected_items = request.POST.getlist('item_selected')
            items = Inventory.objects.filter(iid__in=selected_items)
            remarks = request.POST.get('remarks')
            operation = 'Remove'

            for item in items:
                itemtodel = Inventory.objects.get(iid=item.iid)
                recent_value = Transactions.objects.filter(iid=item.iid).order_by('-date')[0]
                Transactions.objects.create(iid = itemtodel, operation = operation, location = recent_value.location, proprietor = recent_value.proprietor, remarks = ('Removed: ', item,'Reason: ', remarks), status = 'Inactive')
                Inventory.objects.get(pk=item.iid).delete()

            inventory = Inventory.objects.all()
            page = request.GET.get('page', 1)

            paginator = Paginator(inventory, 15)
            try:
                inventorys = paginator.page(page)
            except PageNotAnInteger:
                inventorys = paginator.page(paginator.num_pages)
            return render(request, 'its/remove.html', {'inventorys': inventorys, 'display': display})
        else:
            remarks = request.POST.get('remarks')
            operation = 'Remove'
            
            item = Inventory.objects.get(iid=iid)
            recent_value = Transactions.objects.filter(iid=item.iid).order_by('-date')[0]
            Transactions.objects.create(iid = item, operation = operation, location = recent_value.location, proprietor = recent_value.proprietor, remarks = ('Removed: ', item,'Reason: ', remarks), status = 'Inactive')

            Inventory.objects.get(pk=iid).delete()
            inventory = Inventory.objects.all()
            page = request.GET.get('page', 1)

            paginator = Paginator(inventory, 15)
            try:
                inventorys = paginator.page(page)
            except PageNotAnInteger:
                inventorys = paginator.page(paginator.num_pages)
            return render(request, 'its/remove.html', {'inventorys': inventorys, 'display': display})  
    elif request.GET.get('search'):
        display1 = 'd-none'
        inventorys = Inventory.objects.all()
        search_query = request.GET.get('search')
        inventorys = inventorys.filter(manufacture_name__icontains=search_query) | inventorys.filter(model_name__icontains=search_query) | inventorys.filter(device_type__icontains=search_query) | inventorys.filter(serial_number__icontains=search_query)
        result = inventorys.count()
        if result == 0:
            inventorys = Inventory.objects.all()
            return render(request, 'its/remove.html', {'inventorys': inventorys, 'result': result, 'display1': display1})    
        else:
            return render(request, 'its/remove.html', {'inventorys': inventorys, 'result': result, 'display1': display1})
    else:
        display = 'd-none'
        display1 = 'd-none'
        inventory = Inventory.objects.all()
        page = request.GET.get('page', 1)

        paginator = Paginator(inventory, 15)
        try:
            inventorys = paginator.page(page)
        except PageNotAnInteger:
            inventorys = paginator.page(paginator.num_pages)
        return render(request, 'its/remove.html', {'inventorys': inventorys, 'display': display, 'display1': display1})

@csrf_exempt
def transfer(request):

    if request.method == 'POST':
        display = 'd-none'
        iid = request.POST.get('item_row', 0)
        if iid == 0:
            items = []
            selected_items = request.POST.getlist('item_selected')
            items = Inventory.objects.filter(iid__in=selected_items)
            remarks = request.POST.get('remarks')
            location = request.POST.get('location')
            proprietor = request.POST.get('proprietor')
            operation = 'Transfer'

            for item in items:
                itemtotransfer = Inventory.objects.get(iid=item.iid)
                recent_value = Transactions.objects.filter(iid=item.iid).order_by('-date')[0]
                Transactions.objects.create(iid = itemtotransfer, operation = operation, location = location, proprietor = proprietor, remarks = ('Transfered: ', item,'Reason: ', remarks), status = recent_value.status)

            inventory = Inventory.objects.all()
            page = request.GET.get('page', 1)

            paginator = Paginator(inventory, 15)
            try:
                inventorys = paginator.page(page)
            except PageNotAnInteger:
                inventorys = paginator.page(paginator.num_pages)
            return render(request, 'its/transfer.html', {'inventorys': inventorys, 'dsiplay': display})
        else:
            remarks = request.POST.get('remarks')
            location = request.POST.get('location')
            proprietor = request.POST.get('proprietor')
            operation = 'Transfer'
            
            item = Inventory.objects.get(iid=iid)
            recent_value = Transactions.objects.filter(iid=iid).order_by('-date')[0]
            Transactions.objects.create(iid = item, operation = operation, location = location, proprietor = proprietor, remarks = ('Transfered: ', item,'Reason: ', remarks), status = recent_value.status)

            inventory = Inventory.objects.all()
            page = request.GET.get('page', 1)

            paginator = Paginator(inventory, 15)
            try:
                inventorys = paginator.page(page)
            except PageNotAnInteger:
                inventorys = paginator.page(paginator.num_pages)
            return render(request, 'its/transfer.html', {'inventorys': inventorys, 'display': display})  
    
    elif request.GET.get('search'):
        display1 = 'd-none'
        inventorys = Inventory.objects.all()
        search_query = request.GET.get('search')
        inventorys = inventorys.filter(manufacture_name__icontains=search_query) | inventorys.filter(model_name__icontains=search_query) | inventorys.filter(device_type__icontains=search_query) | inventorys.filter(serial_number__icontains=search_query)
        result = inventorys.count()
        if result == 0:
            inventorys = Inventory.objects.all()
            return render(request, 'its/transfer.html', {'inventorys': inventorys, 'result': result, 'display1': display1})    
        else:
            return render(request, 'its/transfer.html', {'inventorys': inventorys, 'result': result, 'display1': display1})
    else:
        display = 'd-none'
        display1 = 'd-none'
        inventory = Inventory.objects.all()
        page = request.GET.get('page', 1)

        paginator = Paginator(inventory, 15)
        try:
            inventorys = paginator.page(page)
        except PageNotAnInteger:
            inventorys = paginator.page(paginator.num_pages)
        return render(request, 'its/transfer.html', {'inventorys': inventorys, 'display': display, 'display1': display1})

@csrf_exempt
def dispose(request):
    if request.method == 'POST':
        display = 'd-none'
        iid = request.POST.get('item_row', 0)
        if iid == 0:
            items = []
            selected_items = request.POST.getlist('item_selected')
            items = Inventory.objects.filter(iid__in=selected_items)
            remarks = request.POST.get('remarks')
            operation = 'Disposed'

            for item in items:
                itemtodispose = Inventory.objects.get(iid=item.iid)
                recent_value = Transactions.objects.filter(iid=item.iid).order_by('-date')[0]
                Transactions.objects.create(iid = itemtodispose, operation = operation, location = recent_value.location, proprietor = recent_value.proprietor, remarks = ('Disposed: ', item,'Reason: ', remarks), status = 'Disposed')

            inventory = Inventory.objects.all()
            page = request.GET.get('page', 1)

            paginator = Paginator(inventory, 15)
            try:
                inventorys = paginator.page(page)
            except PageNotAnInteger:
                inventorys = paginator.page(paginator.num_pages)
            return render(request, 'its/dispose.html', {'inventorys': inventorys, 'display': display})
        else:
            remarks = request.POST.get('remarks')
            operation = 'Disposed'
            
            item = Inventory.objects.get(iid=iid)
            recent_value = Transactions.objects.filter(iid=iid).order_by('-date')[0]
            Transactions.objects.create(iid = item, operation = operation, location = recent_value.location, proprietor = recent_value.proprietor, remarks = ('Disposed: ', item,'Reason: ', remarks), status = 'Disposed')

            inventory = Inventory.objects.all()
            page = request.GET.get('page', 1)

            paginator = Paginator(inventory, 15)
            try:
                inventorys = paginator.page(page)
            except PageNotAnInteger:
                inventorys = paginator.page(paginator.num_pages)
            return render(request, 'its/dispose.html', {'inventorys': inventorys, 'display': display})  
    elif request.GET.get('search'):
        display1 = 'd-none'
        inventorys = Inventory.objects.all()
        search_query = request.GET.get('search')
        inventorys = inventorys.filter(manufacture_name__icontains=search_query) | inventorys.filter(model_name__icontains=search_query) | inventorys.filter(device_type__icontains=search_query) | inventorys.filter(serial_number__icontains=search_query)
        result = inventorys.count()
        if result == 0:
            inventorys = Inventory.objects.all()
            return render(request, 'its/dispose.html', {'inventorys': inventorys, 'result': result, 'display1': display1})    
        else:
            return render(request, 'its/dispose.html', {'inventorys': inventorys, 'result': result, 'display1': display1})
    else:
        display = 'd-none'
        display1 = 'd-none'
        inventory = Inventory.objects.all()
        page = request.GET.get('page', 1)

        paginator = Paginator(inventory, 15)
        try:
            inventorys = paginator.page(page)
        except PageNotAnInteger:
            inventorys = paginator.page(paginator.num_pages)
        return render(request, 'its/dispose.html', {'inventorys': inventorys, 'display': display, 'display1': display1})

def login(request):
    return render(request, 'its/login.html', {})

# def locate(request):
#     inventorys = Inventory.objects.all()
#     if request.method =='GET':
#         search_query = request.GET.get('search_box', None)
#         inventorys = inventorys.filter(manufacture_name__icontains=search_query) | inventorys.filter(model_name__icontains=search_query) | inventorys.filter(device_type__icontains=search_query) | inventorys.filter(serial_number__icontains=search_query) | inventorys.filter(location__icontains=search_query) | inventorys.filter(proprietor__icontains=search_query)
#         result = inventorys.count()
#         return render(request, 'index.html', {'inventorys': inventorys, 'result': result})
#     else:
#         return render(request, '/', {'inventorys': inventorys})

def update(request):
    if request.method == 'POST':
        display = 'd-none'
        iid = request.POST.get('item_row', 0)
        if iid == 0:
            items = []
            selected_items = request.POST.getlist('item_selected')
            items = Inventory.objects.filter(iid__in=selected_items)
            remarks = request.POST.get('remarks')
            operation = 'Change Status'
            status = request.POST.get('status')

            for item in items:
                itemtoupdate = Inventory.objects.get(iid=item.iid)
                recent_value = Transactions.objects.filter(iid=item.iid).order_by('-date')[0]
                Transactions.objects.create(iid = itemtoupdate, operation = operation, location = recent_value.location, proprietor = recent_value.proprietor, remarks = ('Updated: ', item,'Reason: ', remarks), status = status)

            inventory = Inventory.objects.all()
            page = request.GET.get('page', 1)

            paginator = Paginator(inventory, 15)
            try:
                inventorys = paginator.page(page)
            except PageNotAnInteger:
                inventorys = paginator.page(paginator.num_pages)
            return render(request, 'its/update.html', {'inventorys': inventorys, 'display': display})
        else:
            remarks = request.POST.get('remarks')
            operation = 'Change Status'
            status = request.POST.get('status')
            
            item = Inventory.objects.get(iid=iid)
            recent_value = Transactions.objects.filter(iid=iid).order_by('-date')[0]
            Transactions.objects.create(iid = item, operation = operation, location = recent_value.location, proprietor = recent_value.proprietor, remarks = ('Updated: ', item,'Reason: ', remarks), status = status)

            inventory = Inventory.objects.all()
            page = request.GET.get('page', 1)

            paginator = Paginator(inventory, 15)
            try:
                inventorys = paginator.page(page)
            except PageNotAnInteger:
                inventorys = paginator.page(paginator.num_pages)
            return render(request, 'its/update.html', {'inventorys': inventorys, 'display': display})  
    elif request.GET.get('search'):
        display1 = 'd-none'
        inventorys = Inventory.objects.all()
        search_query = request.GET.get('search')
        inventorys = inventorys.filter(manufacture_name__icontains=search_query) | inventorys.filter(model_name__icontains=search_query) | inventorys.filter(device_type__icontains=search_query) | inventorys.filter(serial_number__icontains=search_query)
        result = inventorys.count()
        if result == 0:
            inventorys = Inventory.objects.all()
            return render(request, 'its/update.html', {'inventorys': inventorys, 'result': result, 'display1': display1})    
        else:
            return render(request, 'its/update.html', {'inventorys': inventorys, 'result': result, 'display1': display1})
    else:
        display = 'd-none'
        display1 = 'd-none'
        inventory = Inventory.objects.all()
        page = request.GET.get('page', 1)

        paginator = Paginator(inventory, 15)
        try:
            inventorys = paginator.page(page)
        except PageNotAnInteger:
            inventorys = paginator.page(paginator.num_pages)
        return render(request, 'its/update.html', {'inventorys': inventorys, 'display': display, 'display1': display1})

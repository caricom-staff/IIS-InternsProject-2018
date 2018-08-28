from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views.generic import ListView
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Inventory, Staff, Transactions


def nodupes():
    objs = Transactions.objects.exclude(iid__isnull=True).order_by("-date")
    seen = set()
    keep = []
    for o in objs:
        if o.iid not in seen:
            keep.append(o)
            seen.add(o.iid)
    return(keep)

@login_required
def dashboard(request):
    return render(request, 'its/index.html', {})

@login_required
@csrf_exempt
def inventory(request):
    if request.method == 'POST':
        display = 'd-none'
        uid = request.user
        sid = Staff.objects.get(username=uid)
        operation = request.POST.get('operation')
        if operation == 'Add':
            manufacture_name = request.POST.get('manufacture_name')
            model_name = request.POST.get('model_name')
            device_type = request.POST.get('device_type')
            serial_number = request.POST.get('serial_number')
            location = request.POST.get('location')
            proprietor = request.POST.get('proprietor')
            status = request.POST.get('status')
            remarks = request.POST.get('remarks')
            new_item = Inventory(manufacture_name=manufacture_name, model_name=model_name, device_type=device_type, serial_number=serial_number)
            new_item.save()

            iid = Inventory.objects.get(serial_number=serial_number)
            add_transaction = Transactions(iid = iid, sid = sid, operation = operation, location = location, proprietor = proprietor, status = status)
            add_transaction.save()
            display2 = 'd-none'
            display3 = 'd-none'
            display4 = 'd-none'
            display5 = 'd-none'
            inventory = nodupes()
            page = request.GET.get('page', 1)

            paginator = Paginator(inventory, 15)
            try:
                inventorys = paginator.page(page)
            except PageNotAnInteger:
                inventorys = paginator.page(paginator.num_pages)
            return render(request, 'its/inventory.html', {'display':display, 'display2': display2, 'display3': display3, 'display4': display4, 'display5': display5, 'inventorys': inventorys})
        elif operation == 'Remove':
            items = []
            selected_items = request.POST.getlist('item_selected')
            items = Inventory.objects.filter(iid__in=selected_items)
            remarks = request.POST.get('remarks')
    
            for item in items:
                itemtodel = Inventory.objects.get(iid=item.iid)
                recent_value = Transactions.objects.filter(iid=item.iid).order_by('-date')[0]
                Transactions.objects.create(iid = itemtodel, sid = sid, operation = operation, location = recent_value.location, proprietor = recent_value.proprietor, remarks = ('Removed: ', item,'Reason: ', remarks), status = 'Inactive')
                Inventory.objects.get(pk=item.iid).delete()

            display1 = 'd-none'
            display3 = 'd-none'
            display4 = 'd-none'
            display5 = 'd-none'
            inventory = nodupes()
            page = request.GET.get('page', 1)

            paginator = Paginator(inventory, 15)
            try:
                inventorys = paginator.page(page)
            except PageNotAnInteger:
                inventorys = paginator.page(paginator.num_pages)
            return render(request, 'its/inventory.html', {'inventorys': inventorys, 'display': display, 'display1': display1, 'display3': display3, 'display4': display4, 'display5': display5})
        elif operation == 'Disposed':
            items = []
            selected_items = request.POST.getlist('item_selected')
            items = Inventory.objects.filter(iid__in=selected_items)
            remarks = request.POST.get('remarks')
            operation = 'Disposed'

            for item in items:
                itemtodispose = Inventory.objects.get(iid=item.iid)
                recent_value = Transactions.objects.filter(iid=item.iid).order_by('-date')[0]
                Transactions.objects.create(iid = itemtodispose, sid = sid, operation = operation, location = recent_value.location, proprietor = recent_value.proprietor, remarks = ('Disposed: ', item,'Reason: ', remarks), status = 'Disposed')

            display1 = 'd-none'
            display2 = 'd-none'
            display3 = 'd-none'
            display5 = 'd-none'
            inventory = nodupes()
            page = request.GET.get('page', 1)

            paginator = Paginator(inventory, 15)
            try:
                inventorys = paginator.page(page)
            except PageNotAnInteger:
                inventorys = paginator.page(paginator.num_pages)
            return render(request, 'its/inventory.html', {'inventorys': inventorys, 'display': display, 'display1': display1, 'display2': display2, 'display3': display3, 'display5': display5})
        elif operation == 'Update':
            items = []
            selected_items = request.POST.getlist('item_selected')
            items = Inventory.objects.filter(iid__in=selected_items)
            remarks = request.POST.get('remarks')
            operation = 'Change Status'
            status = request.POST.get('status')

            for item in items:
                itemtoupdate = Inventory.objects.get(iid=item.iid)
                recent_value = Transactions.objects.filter(iid=item.iid).order_by('-date')[0]
                Transactions.objects.create(iid = itemtoupdate, sid = sid, operation = operation, location = recent_value.location, proprietor = recent_value.proprietor, remarks = ('Updated: ', item,'Reason: ', remarks), status = status)
            display1 = 'd-none'
            display2 = 'd-none'
            display3 = 'd-none'
            display4 = 'd-none'
            inventory = nodupes()
            page = request.GET.get('page', 1)

            paginator = Paginator(inventory, 15)
            try:
                inventorys = paginator.page(page)
            except PageNotAnInteger:
                inventorys = paginator.page(paginator.num_pages)
            return render(request, 'its/inventory.html', {'inventorys': inventorys, 'display': display, 'display1': display1, 'display2': display2, 'display3': display3, 'display4': display4})
        else:
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
                Transactions.objects.create(iid = itemtotransfer, sid = sid, operation = operation, location = location, proprietor = proprietor, remarks = ('Transfered: ', item,'Reason: ', remarks), status = recent_value.status)

            display1 = 'd-none'
            display2 = 'd-none'
            display4 = 'd-none'
            display5 = 'd-none'
            inventory = nodupes()
            page = request.GET.get('page', 1)

            paginator = Paginator(inventory, 15)
            try:
                inventorys = paginator.page(page)
            except PageNotAnInteger:
                inventorys = paginator.page(paginator.num_pages)
            return render(request, 'its/inventory.html', {'inventorys': inventorys, 'display': display, 'display1': display1, 'display2': display2, 'display4': display4, 'display5': display5, 'location': location, 'proprietor': proprietor})
    elif request.GET.get('search'):
        display1 = 'd-none'
        display2 = 'd-none'
        display3 = 'd-none'
        display4 = 'd-none'
        display5 = 'd-none'
        search_query = request.GET.get('search')
        inventorys = Transactions.objects.filter(iid__manufacture_name__icontains=search_query) | Transactions.objects.filter(iid__model_name__icontains=search_query) | Transactions.objects.filter(iid__device_type__icontains=search_query) | Transactions.objects.filter(iid__serial_number__icontains=search_query) | Transactions.objects.filter(status__icontains=search_query) | Transactions.objects.filter(location__icontains=search_query) | Transactions.objects.filter(proprietor__icontains=search_query)
        result = inventorys.count()
        if result == 0:
            inventorys = nodupes()
            return render(request, 'its/inventory.html', {'inventorys': inventorys, 'result': result, 'display1': display1, 'display2': display2, 'display3': display3, 'display4': display4, 'display5': display5})    
        else:
            return render(request, 'its/inventory.html', {'inventorys': inventorys, 'result': result, 'display1': display1, 'display2': display2, 'display3': display3, 'display4': display4, 'display5': display5})
    else:
        display = 'd-none'
        display1 = 'd-none'
        display2 = 'd-none'
        display3 = 'd-none'
        display4 = 'd-none'
        display5 = 'd-none'
        inventory = nodupes()

        page = request.GET.get('page', 1)

        paginator = Paginator(inventory, 15)
        try:
            inventorys = paginator.page(page)
        except PageNotAnInteger:
            inventorys = paginator.page(paginator.num_pages)
        return render(request, 'its/inventory.html', {'inventorys': inventorys, 'display':display, 'display1': display1, 'display2': display2, 'display3': display3, 'display4': display4, 'display5': display5})

@login_required
def staff(request):
    return render(request, 'its/staff.html', {})

@login_required
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
        uid = request.user
        sid = Staff.objects.get(username=uid)
        operation = 'Add'
        
        new_item = Inventory(manufacture_name=manufacture_name, model_name=model_name, device_type=device_type, serial_number=serial_number)
        new_item.save()

        iid = Inventory.objects.get(serial_number=serial_number)
        add_transaction = Transactions(iid = iid,sid = sid, operation = operation, location = location, proprietor = proprietor, status = status)
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
    
@login_required
@csrf_exempt
def remove(request):
    if request.method == 'POST':
        display = 'd-none'
        uid = request.user
        sid = Staff.objects.get(username=uid)
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
                Transactions.objects.create(iid = itemtodel, sid = sid, operation = operation, location = recent_value.location, proprietor = recent_value.proprietor, remarks = ('Removed: ', item,'Reason: ', remarks), status = 'Inactive')
                Inventory.objects.get(pk=item.iid).delete()
            inventory = nodupes()
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
            Transactions.objects.create(iid = item, sid = sid, operation = operation, location = recent_value.location, proprietor = recent_value.proprietor, remarks = ('Removed: ', item,'Reason: ', remarks), status = 'Inactive')

            Inventory.objects.get(pk=iid).delete()
            inventory = nodupes()
            page = request.GET.get('page', 1)

            paginator = Paginator(inventory, 15)
            try:
                inventorys = paginator.page(page)
            except PageNotAnInteger:
                inventorys = paginator.page(paginator.num_pages)
            return render(request, 'its/remove.html', {'inventorys': inventorys, 'display': display})  
    elif request.GET.get('search'):
        display1 = 'd-none'
        search_query = request.GET.get('search')
        inventorys = Transactions.objects.filter(iid__manufacture_name__icontains=search_query) | Transactions.objects.filter(iid__model_name__icontains=search_query) | Transactions.objects.filter(iid__device_type__icontains=search_query) | Transactions.objects.filter(iid__serial_number__icontains=search_query) | Transactions.objects.filter(status__icontains=search_query) | Transactions.objects.filter(location__icontains=search_query) | Transactions.objects.filter(proprietor__icontains=search_query)
        result = inventorys.count()
        if result == 0:
            inventory = nodupes()
            return render(request, 'its/remove.html', {'inventorys': inventorys, 'result': result, 'display1': display1})    
        else:
            return render(request, 'its/remove.html', {'inventorys': inventorys, 'result': result, 'display1': display1})
    else:
        display = 'd-none'
        display1 = 'd-none'
        inventory = nodupes()
        page = request.GET.get('page', 1)

        paginator = Paginator(inventory, 15)
        try:
            inventorys = paginator.page(page)
        except PageNotAnInteger:
            inventorys = paginator.page(paginator.num_pages)
        return render(request, 'its/remove.html', {'inventorys': inventorys, 'display': display, 'display1': display1})

@login_required
@csrf_exempt
def transfer(request):
    if request.method == 'POST':
        display = 'd-none'
        uid = request.user
        sid = Staff.objects.get(username=uid)
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
                Transactions.objects.create(iid = itemtotransfer, sid = sid, operation = operation, location = location, proprietor = proprietor, remarks = ('Transfered: ', item,'Reason: ', remarks), status = recent_value.status)
                
            inventory = nodupes()

            page = request.GET.get('page', 1)

            paginator = Paginator(inventory, 15)
            try:
                inventorys = paginator.page(page)
            except PageNotAnInteger:
                inventorys = paginator.page(paginator.num_pages)
            return render(request, 'its/transfer.html', {'inventorys': inventorys, 'display': display})
        else:
            remarks = request.POST.get('remarks')
            location = request.POST.get('location')
            proprietor = request.POST.get('proprietor')
            operation = 'Transfer'
            
            item = Inventory.objects.get(iid=iid)
            recent_value = Transactions.objects.filter(iid=iid).order_by('-date')[0]
            Transactions.objects.create(iid = item, sid = sid, operation = operation, location = location, proprietor = proprietor, remarks = ('Transfered: ', item,'Reason: ', remarks), status = recent_value.status)
            
            inventory = nodupes()
            page = request.GET.get('page', 1)

            paginator = Paginator(inventory, 15)
            try:
                inventorys = paginator.page(page)
            except PageNotAnInteger:
                inventorys = paginator.page(paginator.num_pages)
            return render(request, 'its/transfer.html', {'inventorys': inventorys, 'display': display})  
    
    elif request.GET.get('search'):
        display1 = 'd-none'
        search_query = request.GET.get('search')
        inventorys = Transactions.objects.filter(iid__manufacture_name__icontains=search_query) | Transactions.objects.filter(iid__model_name__icontains=search_query) | Transactions.objects.filter(iid__device_type__icontains=search_query) | Transactions.objects.filter(iid__serial_number__icontains=search_query) | Transactions.objects.filter(status__icontains=search_query) | Transactions.objects.filter(location__icontains=search_query) | Transactions.objects.filter(proprietor__icontains=search_query)
        result = inventorys.count()
        if result == 0:
            inventory = nodupes()
            return render(request, 'its/transfer.html', {'inventorys': inventorys, 'result': result, 'display1': display1})    
        else:
            return render(request, 'its/transfer.html', {'inventorys': inventorys, 'result': result, 'display1': display1})
    else:
        display = 'd-none'
        display1 = 'd-none'
        inventory = nodupes()
        page = request.GET.get('page', 1)

        paginator = Paginator(inventory, 15)
        try:
            inventorys = paginator.page(page)
        except PageNotAnInteger:
            inventorys = paginator.page(paginator.num_pages)
        return render(request, 'its/transfer.html', {'inventorys': inventorys, 'display': display, 'display1': display1})

@login_required
@csrf_exempt
def dispose(request):
    if request.method == 'POST':
        display = 'd-none'
        uid = request.user
        sid = Staff.objects.get(username=uid)
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
                Transactions.objects.create(iid = itemtodispose, sid = sid, operation = operation, location = recent_value.location, proprietor = recent_value.proprietor, remarks = ('Disposed: ', item,'Reason: ', remarks), status = 'Disposed')
            
            inventory = nodupes()
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
            Transactions.objects.create(iid = item, sid = sid, operation = operation, location = recent_value.location, proprietor = recent_value.proprietor, remarks = ('Disposed: ', item,'Reason: ', remarks), status = 'Disposed')

            inventory = nodupes()
            page = request.GET.get('page', 1)

            paginator = Paginator(inventory, 15)
            try:
                inventorys = paginator.page(page)
            except PageNotAnInteger:
                inventorys = paginator.page(paginator.num_pages)
            return render(request, 'its/dispose.html', {'inventorys': inventorys, 'display': display})  
    elif request.GET.get('search'):
        display1 = 'd-none'
        search_query = request.GET.get('search')
        inventorys = Transactions.objects.filter(iid__manufacture_name__icontains=search_query) | Transactions.objects.filter(iid__model_name__icontains=search_query) | Transactions.objects.filter(iid__device_type__icontains=search_query) | Transactions.objects.filter(iid__serial_number__icontains=search_query) | Transactions.objects.filter(status__icontains=search_query) | Transactions.objects.filter(location__icontains=search_query) | Transactions.objects.filter(proprietor__icontains=search_query)
        result = inventorys.count()
        if result == 0:
            inventory = nodupes()
            return render(request, 'its/dispose.html', {'inventorys': inventorys, 'result': result, 'display1': display1})    
        else:
            return render(request, 'its/dispose.html', {'inventorys': inventorys, 'result': result, 'display1': display1})
    else:
        display = 'd-none'
        display1 = 'd-none'
        inventory = nodupes()
        page = request.GET.get('page', 1)

        paginator = Paginator(inventory, 15)
        try:
            inventorys = paginator.page(page)
        except PageNotAnInteger:
            inventorys = paginator.page(paginator.num_pages)
        return render(request, 'its/dispose.html', {'inventorys': inventorys, 'display': display, 'display1': display1})

@login_required
@csrf_exempt
def update(request):
    if request.method == 'POST':
        display = 'd-none'
        uid = request.user
        sid = Staff.objects.get(username=uid)
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
                Transactions.objects.create(iid = itemtoupdate, sid = sid, operation = operation, location = recent_value.location, proprietor = recent_value.proprietor, remarks = ('Updated: ', item,'Reason: ', remarks), status = status)

            inventory = nodupes()
            page = request.GET.get('page', 1)

            paginator = Paginator(inventory, 15)
            try:
                inventorys = paginator.page(page)
            except PageNotAnInteger:
                inventorys = paginator.page(paginator.num_pages)
            return render(request, 'its/update.html', {'inventorys': inventorys, 'display': display, 'status': status})
        else:
            remarks = request.POST.get('remarks')
            operation = 'Change Status'
            status = request.POST.get('status')
            
            item = Inventory.objects.get(iid=iid)
            recent_value = Transactions.objects.filter(iid=iid).order_by('-date')[0]
            Transactions.objects.create(iid = item, sid = sid, operation = operation, location = recent_value.location, proprietor = recent_value.proprietor, remarks = ('Updated: ', item,'Reason: ', remarks), status = status)

            inventory = nodupes()
            page = request.GET.get('page', 1)

            paginator = Paginator(inventory, 15)
            try:
                inventorys = paginator.page(page)
            except PageNotAnInteger:
                inventorys = paginator.page(paginator.num_pages)
            return render(request, 'its/update.html', {'inventorys': inventorys, 'display': display, 'status': status})  
    elif request.GET.get('search'):
        display1 = 'd-none'
        search_query = request.GET.get('search')
        inventorys = Transactions.objects.filter(iid__manufacture_name__icontains=search_query) | Transactions.objects.filter(iid__model_name__icontains=search_query) | Transactions.objects.filter(iid__device_type__icontains=search_query) | Transactions.objects.filter(iid__serial_number__icontains=search_query) | Transactions.objects.filter(status__icontains=search_query) | Transactions.objects.filter(location__icontains=search_query) | Transactions.objects.filter(proprietor__icontains=search_query)
        result = inventorys.count()
        if result == 0:
            inventory = nodupes()
            return render(request, 'its/update.html', {'inventorys': inventorys, 'result': result, 'display1': display1})    
        else:
            return render(request, 'its/update.html', {'inventorys': inventorys, 'result': result, 'display1': display1})
    else:
        display = 'd-none'
        display1 = 'd-none'
        inventory = nodupes()
        page = request.GET.get('page', 1)

        paginator = Paginator(inventory, 15)
        try:
            inventorys = paginator.page(page)
        except PageNotAnInteger:
            inventorys = paginator.page(paginator.num_pages)
        return render(request, 'its/update.html', {'inventorys': inventorys, 'display': display, 'display1': display1})

@login_required
@csrf_exempt
def item(request, key):
    display1 = 'd-none'
    display2 = 'd-none'
    display3 = 'd-none'
    display4 = 'd-none'
    if request.method == 'POST':
        uid = request.user
        sid = Staff.objects.get(username=uid)
        iid = request.POST.get('item')
        operation = request.POST.get('operation')
        if operation == 'Update':
            remarks = request.POST.get('remarks')
            operation = 'Change Status'
            status = request.POST.get('status')
            
            item = Inventory.objects.get(iid=iid)
            recent_value = Transactions.objects.filter(iid=iid).order_by('-date')[0]
            Transactions.objects.create(iid = item, sid = sid, operation = operation, location = recent_value.location, proprietor = recent_value.proprietor, remarks = ('Updated: ', item,'Reason: ', remarks), status = status)
            recent_transaction = Transactions.objects.filter(iid=key).order_by("-date")[0]
            transaction = Transactions.objects.exclude(operation='Remove').filter(iid=key).order_by("-date")
            add_transaction = Transactions.objects.get(iid=key, operation='Add')
            
            return render(request, 'its/item.html', {'add': add_transaction, 'recent': recent_transaction, 'transaction': transaction, 'item': item, 'display2': display2, 'display3': display3, 'display4': display4})
        elif operation == 'Remove':
            remarks = request.POST.get('remarks')
            
            item = Inventory.objects.get(iid=iid)
            recent_value = Transactions.objects.filter(iid=item.iid).order_by('-date')[0]
            Transactions.objects.create(iid = item, sid = sid, operation = operation, location = recent_value.location, proprietor = recent_value.proprietor, remarks = ('Removed: ', item,'Reason: ', remarks), status = 'Inactive')

            Inventory.objects.get(pk=iid).delete()

            return render(request, 'its/item.html', {'display1': display1, 'display3': display3, 'display4': display4})
        elif operation == 'Disposed':
            remarks = request.POST.get('remarks')
            
            item = Inventory.objects.get(iid=iid)
            recent_value = Transactions.objects.filter(iid=iid).order_by('-date')[0]
            Transactions.objects.create(iid = item, sid = sid, operation = operation, location = recent_value.location, proprietor = recent_value.proprietor, remarks = ('Disposed: ', item,'Reason: ', remarks), status = 'Disposed')
            recent_transaction = Transactions.objects.filter(iid=key).order_by("-date")[0]
            transaction = Transactions.objects.exclude(operation='Remove').filter(iid=key).order_by("-date")
            add_transaction = Transactions.objects.get(iid=key, operation='Add')

            return render(request, 'its/item.html', {'add': add_transaction, 'recent': recent_transaction, 'transaction': transaction, 'item': item, 'display1': display1, 'display2': display2, 'display3': display3})
        else:
            remarks = request.POST.get('remarks')
            location = request.POST.get('location')
            proprietor = request.POST.get('proprietor')
            
            item = Inventory.objects.get(iid=iid)
            recent_value = Transactions.objects.filter(iid=iid).order_by('-date')[0]
            Transactions.objects.create(iid = item, sid = sid, operation = operation, location = location, proprietor = proprietor, remarks = ('Transfered: ', item,'Reason: ', remarks), status = recent_value.status)
            recent_transaction = Transactions.objects.filter(iid=key).order_by("-date")[0]
            transaction = Transactions.objects.exclude(operation='Remove').filter(iid=key).order_by("-date")
            add_transaction = Transactions.objects.get(iid=key, operation='Add')

            return render(request, 'its/item.html', {'add': add_transaction, 'recent': recent_transaction, 'transaction': transaction, 'item': item, 'display1': display1, 'display2': display2, 'display4': display4, 'location': location, 'proprietor': proprietor})
    else:
        recent_transaction = Transactions.objects.filter(iid=key).order_by("-date")[0]
        transaction = Transactions.objects.exclude(operation='Remove').filter(iid=key).order_by("-date")
        add_transaction = Transactions.objects.get(iid=key, operation='Add')
        transfer_transaction = Transactions.objects.filter(iid=key, operation='Transfer').order_by("-date")
        update_transaction = Transactions.objects.filter(iid=key, operation='Change Status').order_by("-date")
        item = Inventory.objects.get(iid=key)
        return render(request, 'its/item.html', {'add': add_transaction, 'recent': recent_transaction, 'transaction': transaction, 'item': item, 'display1': display1, 'display2': display2, 'display3': display3, 'display4': display4})
    
from django.contrib import admin
from .models import Staff, Inventory, Transactions, Mname

admin.site.register(Staff)
admin.site.register(Inventory)
admin.site.register(Transactions)
admin.site.register(Mname)
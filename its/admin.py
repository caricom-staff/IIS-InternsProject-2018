from django.contrib import admin
from .models import Staff, Inventory, Add, Remove, Transfer, Dispose

admin.site.register(Staff)
admin.site.register(Inventory)
admin.site.register(Add)
admin.site.register(Remove)
admin.site.register(Transfer)
admin.site.register(Dispose)
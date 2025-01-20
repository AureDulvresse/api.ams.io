from django.contrib import admin
from inventory.models import Equipment, Maintenance, Stock

admin.site.register(Equipment)
admin.site.register(Maintenance)
admin.site.register(Stock)
from django.contrib import admin
from finance.models import Account, SchoolFee, Transaction

admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(SchoolFee)
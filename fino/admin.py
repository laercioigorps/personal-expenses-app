from django.contrib import admin

from .models import Account, Transaction, Cattegory
# Register your models here.

admin.site.register(Account)
admin.site.register(Cattegory)
admin.site.register(Transaction)
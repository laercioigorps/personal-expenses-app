from django.contrib import admin
from .models import Preference, Product, Transaction, ProductTransaction

# Register your models here.

admin.site.register(Preference)
admin.site.register(Product)
admin.site.register(Transaction)
admin.site.register(ProductTransaction)
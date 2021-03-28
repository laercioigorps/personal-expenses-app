from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Preference(models.Model):

	preference_text = models.CharField(max_length = 100)
	preference_description = models.CharField(max_length = 100)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.preference_text


class Product(models.Model):
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=200)


class Transaction(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	total = models.IntegerField(default=0)
	is_complited = models.BooleanField(default= False)

class ProductTransaction(models.Model):
	transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
	product = models. ForeignKey(Product, on_delete=models.CASCADE)
	unit = models.CharField(max_length=10)
	quantity = models.IntegerField(default = 0)

	total = models.IntegerField(default=0)

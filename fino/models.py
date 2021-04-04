from django.db import models
from django.contrib.auth.models import User
from datetime import date


# Create your models here.

class Account(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=200,default = '')
	total = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return self.name

	
	


class Cattegory(models.Model):
	name = models.CharField(max_length=20)
	description = models.CharField(max_length=200,default = '')
	is_receita = models.BooleanField(default=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
	#pai = models.ForeignKey(Cattegory, on_delete=models.CASCADE)


	def __str__(self):
		return self.name

class Transaction(models.Model):
	account = models.ForeignKey(Account,on_delete=models.CASCADE)
	cattegory = models.ForeignKey(Cattegory,on_delete=models.CASCADE)
	description = models.CharField(max_length=200,default = '')
	total = models.DecimalField(max_digits=10, decimal_places=2)
	is_completed = models.BooleanField(default=False)
	date = models.DateField( default=date.today)

	def __str__(self):
		return self.description

	

	


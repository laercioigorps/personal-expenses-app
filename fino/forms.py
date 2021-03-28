from django import forms
from .models import Account, Cattegory, Transaction

from django.core.exceptions import ValidationError



class AccountModelForm(forms.ModelForm):
	class Meta():
		model = Account
		fields = ['name', 'description', 'total']

class Account_delete_form(forms.Form):
	resposta = forms.BooleanField( required = True, label='Sim, quero deletar essa conta')


class CattegoryModelForm(forms.ModelForm):
	class Meta():
		model = Cattegory
		fields = ['name', 'description', 'is_receita']


class TransactionModelForm(forms.ModelForm):

	class Meta:
			
		model = Transaction
		fields = ('account','cattegory', 'description','total', 'is_completed', 'date',)

	def __init__(self,user,*args, **kwargs):
		super (TransactionModelForm,self).__init__(*args,**kwargs)
		self.fields['account'].queryset = Account.objects.filter(user= user)
		self.fields['cattegory'].queryset = Cattegory.objects.filter(user= user)

	def clean_total(self):
		total = self.cleaned_data['total']
		if total < 0:
		    raise ValidationError("Você deve acicionar um valor positivo!")

		if total == 0:
			raise ValidationError("isso não foi de graça!!")
        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
		return total


	
		

	



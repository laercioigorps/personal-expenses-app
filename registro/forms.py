from django import forms
from django.contrib.auth.models import User

class TestForm(forms.Form):
	YEAR_IN_SCHOOL_CHOICES = [
	    ('FR', 'Freshman'),
	    ('SO', 'Sophomore'),
	    ('JR', 'Junior'),
	    ('SR', 'Senior'),
	    ('GR', 'Graduate'),
	]

	your_name = forms.CharField(max_length=100, required= True)
	CHOICES = (('Option 1', 'Option 1'),('Option 2', 'Option 2'),)
	field = forms.ChoiceField(choices=CHOICES)


class register(forms.Form):

	login = forms.CharField(max_length = 30, required=True)
	password = 1

class RegistroUsuarioModel(forms.ModelForm):
	
	class Meta:
		model = User
		fields = ['username','password', 'email','first_name']
from django.shortcuts import render
from django.http import HttpResponse
from .forms import TestForm, RegistroUsuarioModel
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . import models
# Create your views here.

def index(request):

	if(request.method == 'POST'):
		form = TestForm(request.POST)
		if form.is_valid():
			return HttpResponse('post valido')

		else:
			return HttpResponse('post invalido')
	else:

		form = TestForm()

		context = {

			'form': form,
		}

		return render(request, 'registro/login.html',context)

def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			login = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password1')
			user = User.objects.create_user(username=login, password= password,email = 'aiaiai@gmail.com')
			user.save()
			return HttpResponse('valido')

		else:
			return HttpResponse('invalido')

		return HttpResponse("hello")
	else:
		#form = UserCreationForm()
		form = RegistroUsuarioModel()
		return render(request,'registro/login.html', {'form': form})


def teste_model_form_view(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			
			return HttpResponse('usuario criado com sucesso	')

		
	else:

		form = UserCreationForm()
		return render(request,'registro/create.html', {'form': form}) 


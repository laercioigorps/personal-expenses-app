from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse


from .forms import AccountModelForm, CattegoryModelForm, TransactionModelForm, Account_delete_form
from .models import Account, Cattegory, Transaction

# Create your views here.

#views for account -----------------------------------------------------------------


@login_required
def home_view(request):
	if(request.user.is_authenticated == False):
		print('-----------------------------------------nao autenticado')
		HttpResponse('usuario não autentucado')
	else:
		print(request.user)
	accounts = request.user.account_set.all()

	transactions = Transaction.objects.filter(account__user = request.user)#will filter transactions of the month later
	completed_transactions = transactions.filter(is_completed=True)
	incompleted_transactions = transactions.filter(is_completed=False)

	receitas_transactions = completed_transactions.filter(cattegory__is_receita = True)
	despesas_transactions = completed_transactions.filter(cattegory__is_receita = False)

	despesas_pendentes_transactions = incompleted_transactions.filter(cattegory__is_receita = False)
	receitas_pendentes_transactions = incompleted_transactions.filter(cattegory__is_receita = True)

	categorias_despesas = request.user.cattegory_set.filter(is_receita = False).filter(transaction__is_completed = True)

	dic = {}

	for cattegory in categorias_despesas:
		soma = cattegory.transaction_set.aggregate(Sum('total'))['total__sum']
		if soma > 0:
			dic[cattegory.name] = soma
	print (dic)	
	context = {

		'saldo' : accounts.aggregate(Sum('total'))['total__sum'],
		'receitas' : receitas_transactions.aggregate(Sum('total'))['total__sum'],
		'despesas' : despesas_transactions.aggregate(Sum('total'))['total__sum'],
		'despesas_pendentes' : despesas_pendentes_transactions.aggregate(Sum('total'))['total__sum'],
		'receitas_pendentes' : receitas_pendentes_transactions.aggregate(Sum('total'))['total__sum'],
		'despesa_por_categoria' : dic,

	}
	return render(request, 'fino/home.html', context)


@login_required
def create_account_view(request):
	if request.method == 'POST':
		form = AccountModelForm(request.POST)
		if form.is_valid():
			account = form.save(commit=False)
			account.user = request.user
			account.save()
			return HttpResponseRedirect(reverse('fino:account_list'))
		
		return HttpResponse('POST')

	else:
		form = AccountModelForm()
		return render(request, 'fino/account_create.html',{'form': form,'us': request.user})

@login_required
def list_account_view(request):
	#accounts = get_list_or_404(Account.objects.filter(user = request.user))
	accounts = Account.objects.filter(user= request.user)
	context = {
		'list_objects' : accounts
	}
	return render(request,'fino/account_list.html', context)

@login_required
def detail_account_view(request, id):
	acount = get_object_or_404(Account,id = id)
	if account.user == request.user:
		print("user == user")
		context = {
			'object' : account
		}
	else:
		print("user not user")
		context = {
			'object' : None
		}
	return render(request,'fino/account_detail.html', context)

@login_required
def edit_account_view(request, id):

	account = get_object_or_404(Account, id=id)
	if not account.user == request.user:
		return HttpResponseForbidden("você não é dono disso")
	if request.method == 'POST':
		form = AccountModelForm(request.POST, instance = account)
		if form.is_valid():
			account = form.save(commit=False)
			account.user = request.user
			account.save()
			return HttpResponseRedirect( reverse('fino:account_list'))
	else:
		form = AccountModelForm(instance=account)
		return render(request, 'fino/account_create.html',{'form': form,'us': request.user})

@login_required
def delete_account_view(request, id):
	account = get_object_or_404(Account, id = id)
	if not account.user == request.user:
		return HttpResponseForbidden("você não é dono disso")

	if account not in request.user.account_set.all():
		return HttpResponseRedirect(reverse('fino:account_list'))
	if request.method == 'POST':
		if account.user == request.user:
			account.delete()
			#return HttpResponse('deletado')
			return HttpResponseRedirect(reverse('fino:account_list'))
	else:

		form = Account_delete_form()
		return render(request, 'fino/account_delete.html',{'form': form, 'id':id})


#views for cattegory -----------------------------------------------------------------


@login_required
def create_cattegory_view(request):
	if request.method == 'POST':

		form = CattegoryModelForm(request.POST)
		if form.is_valid():
			cattegory = form.save(commit=False)
			cattegory.user = request.user
			cattegory.save()
			return HttpResponseRedirect(reverse('fino:cattegory_list'))
	else:
		form = CattegoryModelForm()

		return render(request, 'fino/cattegory_create.html',{'form': form,'us': request.user})

@login_required
def list_cattegory_view(request):
	#accounts = get_list_or_404(Account.objects.filter(user = request.user))
	cattegory = Cattegory.objects.filter(user= request.user)

	context = {
		'list_objects' : cattegory
	}
	return render(request,'fino/cattegory_list.html', context)


@login_required
def detail_cattegory_view(request, id):

	cattegory = get_object_or_404(Cattegory,id = id)

	if cattegory.user == request.user:
		print("user == user")
		context = {
			'object' : cattegory
		}
	else:
		print("user not user")
		context = {
			'object' : None
		}
	return render(request,'fino/cattegory_detail.html', context)


#ok
@login_required
def edit_cattegory_view(request, id):
	cattegory = get_object_or_404(Cattegory, id=id)
	if not cattegory.user == request.user:
		return HttpResponseForbidden("você não é dono disso")
	if request.method == 'POST':

		form = CattegoryModelForm(request.POST, instance = cattegory)
		if form.is_valid():

			cattegory = form.save(commit=False)
			cattegory.user = request.user
			cattegory.save()
			return HttpResponseRedirect(reverse('fino:cattegory_list'))
	else:

		form = CattegoryModelForm(instance=cattegory)
		return render(request, 'fino/cattegory_create.html',{'form': form,'us': request.user})


@login_required
def delete_cattegory_view(request, id):

	cattegory = get_object_or_404(Cattegory, id = id)

	if not cattegory.user == request.user:
		return HttpResponseForbidden("você não é dono disso")

	if request.method == 'POST':
		if cattegory.user == request.user:

			cattegory.delete()
			#return HttpResponse('deletado')
			return HttpResponseRedirect(reverse('fino:cattegory_list'))
	else:

		form = Account_delete_form()
		return render(request, 'fino/cattegory_delete.html',{'form': form, 'id':id})


#views for transaction -----------------------------------------------------------------

@login_required
def create_transaction_view(request):

	if request.method == 'POST':
		form = TransactionModelForm(request.user, request.POST)
		if form.is_valid():
			transaction = form.save(commit=False)
			if transaction.cattegory.is_receita == False:
				transaction.total = transaction.total * -1
			transaction.account.total += transaction.total
			transaction.save()
			transaction.account.save()
			return HttpResponseRedirect(reverse('fino:transaction_list'))
		else:
			return render(request, 'fino/transaction_create.html',{'form':form})
	else:
		form = TransactionModelForm(request.user)
		return render(request, 'fino/transaction_create.html',{'form':form})

@login_required
def list_transaction_view(request):
	#accounts = get_list_or_404(Account.objects.filter(user = request.user))
	transaction = Transaction.objects.filter(cattegory__user = request.user)
	context = {
		'list_objects' : transaction
	}
	return render(request,'fino/transaction_list.html', context)

@login_required
def list_transaction_by_account_view(request, cat):
	#accounts = get_list_or_404(Account.objects.filter(user = request.user))
	transaction = Transaction.objects.filter(cattegory = CattegoryModelForm)
	context = {
		'list_objects' : transaction
	}

	return render(request,'fino/transaction_list.html', context)

@login_required
def list_receitas_by_month(request,month, year):
	return HttpResponse('')

@login_required
def detail_transaction_view(request, id):

	transaction = get_object_or_404(Transaction,id = id)

	if transaction.account in request.user.account_set.all():
		print("user == user")
		context = {
			'object' : transaction
		}
	else:
		print("user not user")
		context = {
			'object' : None
		}
	return render(request,'fino/transaction_detail.html', context)


#ok
@login_required
def edit_transaction_view(request, id):
	transaction = get_object_or_404(Transaction, id=id)
	
	if not transaction.account.user == request.user:
		return HttpResponseForbidden("você não é dono disso")
	if request.method == 'POST':

		#form = TransactionModelForm(request.user, request.POST, instance= transaction)
		form = TransactionModelForm(request.user, request.POST, instance= transaction)
		if form.is_valid():

			transaction = form.save(commit=False)
			transaction.user = request.user
			transaction.save()
			return HttpResponseRedirect(reverse('transaction_list'))
	else:

		form = TransactionModelForm(request.user, instance=transaction)
		return render(request, 'fino/transaction_create.html',{'form': form,'us': request.user})


@login_required
def delete_transaction_view(request, id):

	transaction = get_object_or_404(Transaction, id = id)
	if not transaction.account.user == request.user:
		return HttpResponseForbidden("você não é dono disso")

	if request.method == 'POST':

		form = Account_delete_form(request.POST)
		

		if transaction.account in request.user.account_set.all():
			if form.is_valid():

				transaction.delete()
				#return HttpResponse('deletado')
				return HttpResponseRedirect(reverse('fino:transaction_list'))
			else:
				return HttpResponse('invalido')
	else:

		form = Account_delete_form()
		return render(request, 'fino/transaction_delete.html',{'form': form, 'id':id})



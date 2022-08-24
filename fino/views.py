from unicodedata import category
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
import datetime
from django.db.models import Q

from .selectors import AccountSelector, CategoryReporter

from .forms import AccountModelForm, CattegoryModelForm, TransactionModelForm, Account_delete_form, TransactionTypeModelForm
from .models import Account, Cattegory, Transaction

# Create your views here.

# views for account -----------------------------------------------------------------


@login_required(login_url='/login/')
def wizard_view(request):
    return HttpResponseRedirect(reverse('fino:home_page'))


@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('fino:login_page'))
    # Redirect to a success page.


def teste_view(request):
    return render(request, 'fino/test.html')


def newview(request):
    return render(request, 'fino/base.html')


def signup_view(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        user_basic_setup(user)

        return HttpResponseRedirect(reverse('fino:home_page'))
    return render(request, 'fino/signup.html', {'form': form})


@login_required(login_url='/login/')
def home_view(request):
    context = getHomePageViewContext(request)
    return render(request, 'fino/home.html', context)


def getHomePageViewContext(request):
    acountSelector = AccountSelector()

    accounts = request.user.account_set.all()
    
    cattegoryReporter = CategoryReporter()
    cattegoryReport = cattegoryReporter.getCurrentMonthCattegoryExpensesReport(request.user)

    labels = ['janeiro', 'feb', 'março', 'abril', 'maio', 'junho',
              'julho', 'agosto', 'setembri', 'outubgo', 'nov', 'dez']
    return ({

        'saldo': acountSelector.getTotal(request.user),
        'receitas': acountSelector.getCurrentMonthIncome(request.user),
        'despesas': acountSelector.getCurrentMonthExpenses(request.user),
        'despesas_pendentes': acountSelector.getCurrentMonthPendingExpenses(request.user),
        'receitas_pendentes': acountSelector.getCurrentMonthPendingIncome(request.user),

        'labels': labels,
        'despesas_data': list(acountSelector.getCompletedExpenses(request.user)),
        'receitas_data': list(acountSelector.getCompletedIncomes(request.user)),

        'receitas_pendentes_data': list(acountSelector.getPendingIncomes(request.user)),
        'despesas_pendentes_data': list(acountSelector.getPendingExpenses(request.user)),

        'labels_cat': cattegoryReport['labels'],
        'data_cat': cattegoryReport['data'],

        'accounts': accounts,

    })


@login_required(login_url='/login/')
def create_account_view(request):
    if request.method == 'POST':
        form = AccountModelForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return HttpResponseRedirect(reverse('fino:account_list'))

        else:
            return render(request, 'fino/account_create.html', {'form': form, 'us': request.user})

    else:
        form = AccountModelForm()
        return render(request, 'fino/account_create.html', {'form': form, 'us': request.user})


@login_required(login_url='/login/')
def list_account_view(request):
    #accounts = get_list_or_404(Account.objects.filter(user = request.user))
    accounts = Account.objects.filter(user=request.user)

    transactions = Transaction.objects.filter(account__user=request.user)

    todas_mes = transactions.filter(date__month=4)

    pendentes = todas_mes.filter(is_completed=False)

    #receitas = transactions.filter(is_completed = True).filter(cattegory__is_receita = True).values('total')

    #receitas_pendentes = transactions.filter(is_completed = False).filter(cattegory__is_receita = True).values('total')

    #despesas = transactions.filter(is_completed = True).filter(cattegory__is_receita = False).values('total')
    #despesas_pendentes = transactions.filter(is_completed = False).filter(cattegory__is_receita = False).values('total')

    #x = accounts.annotate(receitas = Sum(receitas)).annotate(despesas = Sum(despesas)).annotate(receitas_pendentes = Sum(receitas_pendentes)).annotate(despesas_pendentes = Sum(despesas_pendentes))

    # accountss = accounts.filter(transaction__cattegory__is_receita = True).annotate(
    #	receita_total = Sum('transaction__total'))

    #accountss = accountss.filter(transaction__is_completed = True).annotate(receita_efetivada = Sum('transaction__total'))

    #accountss = accounts.filter(transaction__date__month = 4).values('name')

    cat_labels = []
    cat_data = []

    saldo = accounts.aggregate(Sum('total'))['total__sum']
    if (not saldo):
        saldo = 0

    valor_pendente = pendentes.aggregate(Sum('total'))['total__sum']
    if not valor_pendente:
        valor_pendente = 0
    for account in accounts:
        cat_labels.append(account.name)
        cat_data.append(str(account.total))
    context = {
        'list_objects': accounts,
        'cat_labels': cat_labels,
        'cat_data': cat_data,
        'saldo': saldo,
        'previsto': saldo + valor_pendente
    }
    return render(request, 'fino/account_list.html', context)


@login_required(login_url='/login/')
def detail_account_view(request, id):
    account = get_object_or_404(Account, id=id)
    if account.user == request.user:
        print("user == user")
        context = {
            'object': account
        }
    else:
        print("user not user")
        context = {
            'object': None
        }
    return render(request, 'fino/account_detail.html', context)


@login_required(login_url='/login/')
def edit_account_view(request, id):

    account = get_object_or_404(Account, id=id)
    if not account.user == request.user:
        return HttpResponseForbidden("você não é dono disso")
    if request.method == 'POST':
        form = AccountModelForm(request.POST, instance=account)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            return HttpResponseRedirect(reverse('fino:account_list'))
    else:
        form = AccountModelForm(instance=account)
        return render(request, 'fino/account_create.html', {'form': form, 'us': request.user})


@login_required(login_url='/login/')
def delete_account_view(request, id):
    account = get_object_or_404(Account, id=id)
    if not account.user == request.user:
        return HttpResponseForbidden("você não é dono disso")

    if account not in request.user.account_set.all():
        return HttpResponseRedirect(reverse('fino:account_list'))
    if request.method == 'POST':
        if account.user == request.user:
            account.delete()
            # return HttpResponse('deletado')
            return HttpResponseRedirect(reverse('fino:account_list'))
    else:

        form = Account_delete_form()
        return render(request, 'fino/account_delete.html', {'form': form, 'id': id})


# views for cattegory -----------------------------------------------------------------


@login_required(login_url='/login/')
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

        return render(request, 'fino/cattegory_create.html', {'form': form, 'us': request.user})


@login_required(login_url='/login/')
def list_cattegory_view(request):
    current_month = datetime.date.today().month
    print(current_month)
    #accounts = get_list_or_404(Account.objects.filter(user = request.user))
    cattegory = Cattegory.objects.filter(user=request.user)
    cat_receitas_labels = []
    cat_receitas_data = []

    cat_despesas_labels = []
    cat_despesas_data = []

    cat_receitas = cattegory.filter(is_receita=True).values(
        'name').annotate(total=Sum('transaction__total'))
    cat_despesas = cattegory.filter(is_receita=False).values(
        'name').annotate(total=Sum('transaction__total'))

    receitas = cat_receitas.aggregate(Sum('total'))['total__sum']
    despesas = cat_despesas.aggregate(Sum('total'))['total__sum']
    if (despesas):
        despesas = despesas * -1
    for cat in cat_receitas:
        if not cat['total']:
            continue
        cat_receitas_labels.append(cat['name'])
        cat_receitas_data.append(str(cat['total']))

    for cat in cat_despesas:
        if not cat['total']:
            continue
        cat_despesas_labels.append(cat['name'])
        cat_despesas_data.append(str(cat['total']))

    context = {
        'list_objects': cattegory,
        'cat_receitas_labels': cat_receitas_labels,
        'cat_receitas_data': cat_receitas_data,

        'cat_despesas_labels': cat_despesas_labels,
        'cat_despesas_data': cat_despesas_data,

        'receitas': str(receitas),
        'despesas': str(despesas),
    }
    return render(request, 'fino/cattegory_list.html', context)


@login_required(login_url='/login/')
def list_cattegory_by_month_year_view(request, month, year):

    #accounts = get_list_or_404(Account.objects.filter(user = request.user))
    cattegory = Cattegory.objects.filter(user=request.user).filter(
        transaction__date__year=year).filter(transaction__date__month=month)

    receitas = Transaction.objects.filter(cattegory__user=request.user).filter(
        cattegory__is_receita=True).filter(
        date__month=month).filter(date__year=year).values('cattegory__name').annotate(
        totals=Sum('total'))
    despesas = Transaction.objects.filter(cattegory__user=request.user).filter(
        cattegory__is_receita=False).filter(
        date__month=month).filter(date__year=year).values('cattegory__name').annotate(
        totals=Sum('total'))

    cat_receitas_labels = []
    cat_receitas_data = []

    cat_despesas_labels = []
    cat_despesas_data = []

    #cat_receitas = cattegory.filter(is_receita = True).values('name').annotate(total = Sum('transaction__total'))
    #cat_despesas = cattegory.filter(is_receita = False).values('name').annotate(total = Sum('transaction__total'))

    #receitas = cat_receitas.aggregate(Sum('total'))['total__sum']
    #despesas= cat_despesas.aggregate(Sum('total'))['total__sum'] * -1
    for cat in receitas:
        if not cat['totals']:
            continue
        cat_receitas_labels.append(cat['cattegory__name'])
        cat_receitas_data.append(str(cat['totals']))

    for cat in despesas:
        if not cat['totals']:
            continue
        cat_despesas_labels.append(cat['cattegory__name'])
        cat_despesas_data.append(str(cat['totals']))

    cattegories = Cattegory.objects.filter(user=request.user).filter(
        transaction__date__year=year).filter(transaction__date__month=month).distinct().annotate(
        totals=Sum('transaction__total'))

    receitas_data = receitas.aggregate(Sum('totals'))['totals__sum']
    despesas_data = despesas.aggregate(Sum('totals'))['totals__sum']

    if despesas_data:
        despesas_data = despesas_data * -1

    context = {
        'list_objects': cattegories,
        'cat_receitas_labels': cat_receitas_labels,
        'cat_receitas_data': cat_receitas_data,

        'cat_despesas_labels': cat_despesas_labels,
        'cat_despesas_data': cat_despesas_data,

        'receitas': receitas_data,
        'despesas': despesas_data,

        'receitas_cat': receitas,
        'despesas_cat': despesas,
    }
    return render(request, 'fino/cattegory_list_by_month_year.html', context)


@login_required(login_url='/login/')
def categorias_view(request):
    #accounts = get_list_or_404(Account.objects.filter(user = request.user))
    current_month = datetime.date.today().month
    current_year = datetime.date.today().year
    return HttpResponseRedirect(reverse('fino:cattegory_list_by_month_year', args=[current_month, current_year]))
    transaction = Transaction.objects.filter(
        cattegory__user=request.user).order_by('-date')
    context = {
        'list_objects': transaction
    }
    return render(request, 'fino/transaction_list.html', context)


@login_required(login_url='/login/')
def detail_cattegory_view(request, id):

    cattegory = get_object_or_404(Cattegory, id=id)

    if cattegory.user == request.user:
        print("user == user")
        context = {
            'object': cattegory
        }
    else:
        print("user not user")
        context = {
            'object': None
        }
    return render(request, 'fino/cattegory_detail.html', context)


# ok
@login_required(login_url='/login/')
def edit_cattegory_view(request, id):
    cattegory = get_object_or_404(Cattegory, id=id)
    if not cattegory.user == request.user:
        return HttpResponseForbidden("você não é dono disso")
    if request.method == 'POST':

        form = CattegoryModelForm(request.POST, instance=cattegory)
        if form.is_valid():

            cattegory = form.save(commit=False)
            cattegory.user = request.user
            cattegory.save()
            return HttpResponseRedirect(reverse('fino:cattegory_list'))
    else:

        form = CattegoryModelForm(instance=cattegory)
        return render(request, 'fino/cattegory_create.html', {'form': form, 'us': request.user})


@login_required(login_url='/login/')
def delete_cattegory_view(request, id):

    cattegory = get_object_or_404(Cattegory, id=id)

    if not cattegory.user == request.user:
        return HttpResponseForbidden("você não é dono disso")

    if request.method == 'POST':
        if cattegory.user == request.user:

            cattegory.delete()
            # return HttpResponse('deletado')
            return HttpResponseRedirect(reverse('fino:cattegory_list'))
    else:

        form = Account_delete_form()
        return render(request, 'fino/cattegory_delete.html', {'form': form, 'id': id})


# views for transaction -----------------------------------------------------------------

@login_required(login_url='/login/')
def create_transaction_view(request):

    if request.method == 'POST':
        form = TransactionModelForm(request.user, request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            if transaction.cattegory.is_receita == False:
                transaction.total = transaction.total * -1
            if transaction.is_completed:
                transaction.account.total += transaction.total
            transaction.save()
            transaction.account.save()
            return HttpResponseRedirect(reverse('fino:transaction_list'))
        else:
            print('-----------invalido------')
            print(request)
            return render(request, 'fino/transaction_create.html', {'form': form})
    else:
        form = TransactionModelForm(request.user)
        return render(request, 'fino/transaction_create.html', {'form': form})


@login_required(login_url='/login/')
def create_transaction_by_type_view(request, types):

    if request.method == 'POST':
        form = TransactionTypeModelForm(request.user, types, request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            if transaction.cattegory.is_receita == False:
                transaction.total = transaction.total * -1
            if transaction.is_completed:
                transaction.account.total += transaction.total
            transaction.save()
            transaction.account.save()
            return HttpResponseRedirect(reverse('fino:transaction_list'))
        else:
            print('-----------invalido------')
            print(request)
            return render(request, 'fino/transaction_create.html', {'form': form})
    else:
        form = TransactionTypeModelForm(request.user, types)
        return render(request, 'fino/transaction_create.html', {'form': form})


@login_required(login_url='/login/')
def list_transaction_view(request):
    #accounts = get_list_or_404(Account.objects.filter(user = request.user))
    transaction = Transaction.objects.filter(
        cattegory__user=request.user).order_by('-date')
    context = {
        'list_objects': transaction
    }
    return render(request, 'fino/transaction_list.html', context)


@login_required(login_url='/login/')
def transacoes_view(request):
    #accounts = get_list_or_404(Account.objects.filter(user = request.user))
    month = datetime.date.today().month
    year = datetime.date.today().year
    return HttpResponseRedirect(reverse('fino:transaction_list_by_month_year', args=[month, year]))
    transaction = Transaction.objects.filter(
        cattegory__user=request.user).order_by('-date')
    context = {
        'list_objects': transaction
    }
    return render(request, 'fino/transaction_list.html', context)


@login_required(login_url='/login/')
def list_transaction_view_by_month(request, month, year):
    #accounts = get_list_or_404(Account.objects.filter(user = request.user))

    months = {}
    months['1'] = 'Janeiro'
    months['2'] = 'Fevereiro'
    months['3'] = 'Março'
    months['4'] = 'Abril'
    months['5'] = 'Maio'
    months['6'] = 'Junho'
    months['7'] = 'Julho'
    months['8'] = 'Agosto'
    months['9'] = 'Setembro'
    months['10'] = 'Outubro'
    months['11'] = 'Novembro'
    months['12'] = 'Dezembro'

    next_month = 0
    before_month = 0
    year_to_next = year
    year_to_before = year

    if month < 1 or month > 12:
        raise Http404('mês invalido')

    if month == 1:
        before_month = 12
        year_to_before = year - 1
    else:
        before_month = month - 1

    if month == 12:
        next_month = 1
        year_to_next = year + 1
    else:
        next_month = month + 1

    transaction = Transaction.objects.filter(account__user=request.user).filter(
        date__year=year).filter(date__month=month).order_by('-date')

    receitas = transaction.filter(cattegory__is_receita=True)
    despesas = transaction.filter(cattegory__is_receita=False)

    receitas_pendentes = receitas.filter(is_completed=False)
    despesas_pendentes = despesas.filter(is_completed=False)

    receitas_data = receitas.aggregate(total=Sum('total'))['total']
    despesas_data = despesas.aggregate(total=Sum('total'))['total']
    receitas_pendentes_data = receitas_pendentes.aggregate(total=Sum('total'))[
        'total']
    despesas_pendentes_data = despesas_pendentes.aggregate(total=Sum('total'))[
        'total']

    if (despesas_data):
        despesas_data = despesas_data * -1
    if (despesas_pendentes_data):
        despesas_pendentes_data = despesas_pendentes_data * -1

    context = {
        'list_objects': transaction,

        'receitas': receitas_data,
        'despesas': despesas_data,
        'receitas_pendentes': receitas_pendentes_data,
        'despesas_pendentes': despesas_pendentes_data,

        'months': months,
        'year': year,
        'year_to_next': year_to_next,
        'year_to_before': year_to_before,
        'month': months[str(month)],
        'next_month': next_month,
        'next_month_name': months[str(next_month)],
        'before_month': before_month,
        'before_month_name': months[str(before_month)],

    }
    return render(request, 'fino/transaction_list_by_month.html', context)


@login_required(login_url='/login/')
def list_transaction_by_account_view(request, cat):
    #accounts = get_list_or_404(Account.objects.filter(user = request.user))
    transaction = Transaction.objects.filter(cattegory=CattegoryModelForm)
    context = {
        'list_objects': transaction
    }

    return render(request, 'fino/transaction_list.html', context)


@login_required(login_url='/login/')
def list_receitas_by_month(request, month, year):
    return HttpResponse('')


@login_required(login_url='/login/')
def detail_transaction_view(request, id):

    transaction = get_object_or_404(Transaction, id=id)

    if transaction.account in request.user.account_set.all():
        print("user == user")
        context = {
            'object': transaction
        }
    else:
        print("user not user")
        context = {
            'object': None
        }
    return render(request, 'fino/transaction_detail.html', context)


# ok
@login_required(login_url='/login/')
def edit_transaction_view(request, id):
    transaction = get_object_or_404(Transaction, id=id)

    if not transaction.account.user == request.user:
        return HttpResponseForbidden("você não é dono disso")
    if request.method == 'POST':

        #form = TransactionModelForm(request.user, request.POST, instance= transaction)
        form = TransactionModelForm(
            request.user, request.POST, instance=transaction)
        if form.is_valid():

            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return HttpResponseRedirect(reverse('transaction_list'))
    else:

        form = TransactionModelForm(request.user, instance=transaction)
        return render(request, 'fino/transaction_create.html', {'form': form, 'us': request.user})


@login_required(login_url='/login/')
def delete_transaction_view(request, id):

    transaction = get_object_or_404(Transaction, id=id)
    if not transaction.account.user == request.user:
        return HttpResponseForbidden("você não é dono disso")

    if request.method == 'POST':

        form = Account_delete_form(request.POST)

        if transaction.account in request.user.account_set.all():
            if form.is_valid():

                transaction.delete()
                # return HttpResponse('deletado')
                return HttpResponseRedirect(reverse('fino:transaction_list'))
            else:
                return HttpResponse('invalido')
    else:

        form = Account_delete_form()
        return render(request, 'fino/transaction_delete.html', {'form': form, 'id': id})


def create_cattegory(user, name, description, is_receita):
    return user.cattegory_set.create(user=user, name=name,
                                     description=description, is_receita=is_receita)


def create_account(user, name, description, total):
    return user.account_set.create(user=user, name=name,
                                   description=description, total=total)


def create_transaction(account, cattegory, description, total, is_completed, date):
    return account.transaction_set.create(cattegory=cattegory,
                                          description=description, total=total,
                                          is_completed=is_completed, date=date)


def user_basic_setup(user):
    create_account(user, 'Carteira',
                   'sua conta mais proxima, o que voce tem com você', 0)

    create_cattegory(user, 'Investimento',
                     'descrição da categoria Investimento', True)
    create_cattegory(user, 'Outros', 'descrição da categoria Outros', True)
    create_cattegory(user, 'Prêmio', 'descrição da categoria Prêmio', True)
    create_cattegory(user, 'presente', 'descrição da categoria presente', True)
    create_cattegory(user, 'Salário', 'descrição da categoria Salário', True)

    create_cattegory(user, 'Alimentação',
                     'descrição da categoria Alimentação', False)
    create_cattegory(user, 'Educação',
                     'descrição da categoria Educação', False)
    create_cattegory(user, 'Lazer', 'descrição da categoria Lazer', False)
    create_cattegory(user, 'Moradia', 'descrição da categoria Moradia', False)
    create_cattegory(user, 'Pagamentos',
                     'descrição da categoria Pagamentos', False)
    create_cattegory(user, 'Roupa', 'descrição da categoria Roupa', False)
    create_cattegory(user, 'Saúde', 'descrição da categoria Saúde', False)
    create_cattegory(user, 'Transporte',
                     'descrição da categoria Transporte', False)
    user.save()

import datetime
from django.db.models import Sum

from .models import Transaction


class AccountSelector:

    def getCurrentMonthTotalForTransactions(self, transactions):
        current_month = datetime.date.today().month

        filtered_transactions = transactions.filter(date__month=current_month)

        transactions_historico = filtered_transactions.values(
            'date__month').annotate(totals=Sum('total'))

        report = transactions_historico.first()
        if (report):
            return (abs(report['totals']))
        return None

    def getTotal(self, user):
        accounts = user.account_set.all()
        return accounts.aggregate(Sum('total'))['total__sum']

    def getCurrentMonthIncome(self, user):
        completed_incomes = Transaction.objects.filter(account__user=user).filter(is_completed=True).filter(
            cattegory__is_receita=True)

        return str(self.getCurrentMonthTotalForTransactions(completed_incomes))

    def getCurrentMonthPendingIncome(self, user):
        pending_incomes = Transaction.objects.filter(account__user=user).filter(is_completed=False).filter(
            cattegory__is_receita=True)
        return str(self.getCurrentMonthTotalForTransactions(pending_incomes))

    def getCurrentMonthExpenses(self, user):
        completed_expenses = Transaction.objects.filter(account__user=user).filter(is_completed=True).filter(
            cattegory__is_receita=False)
        return str(self.getCurrentMonthTotalForTransactions(completed_expenses))

    def getCurrentMonthPendingExpenses(self, user):
        completed_expenses = Transaction.objects.filter(account__user=user).filter(is_completed=False).filter(
            cattegory__is_receita=False)
        return str(self.getCurrentMonthTotalForTransactions(completed_expenses))

    def getCompletedIncomes(self, user):

        completed_incomes = Transaction.objects.filter(account__user=user).filter(is_completed=True).filter(
            cattegory__is_receita=True)

        return self.getDataForTransactions(completed_incomes)

    def getCompletedExpenses(self, user):

        completed_expenses = Transaction.objects.filter(account__user=user).filter(is_completed=True).filter(
            cattegory__is_receita=False)

        return self.getDataForTransactions(completed_expenses)

    def getPendingIncomes(self, user):

        completed_incomes = Transaction.objects.filter(account__user=user).filter(is_completed=False).filter(
            cattegory__is_receita=True)

        return self.getDataForTransactions(completed_incomes)

    def getPendingExpenses(self, user):

        pendingExpenses = Transaction.objects.filter(account__user=user).filter(is_completed=False).filter(
            cattegory__is_receita=False)

        return self.getDataForTransactions(pendingExpenses)

    def getDataForTransactions(self, transactions):
        transactions_hist = transactions.values(
            'date__month').annotate(totals=Sum('total'))
        transactions_data = {}
        for i in range(1, 13):
            transactions_data[str(i)] = 'None'

        for receita in transactions_hist:
            transactions_data[str(receita['date__month'])
                              ] = str(receita['totals'])
        return transactions_data.values()


class CategoryReporter:
    def getCurrentMonthCattegoryExpensesReport(self, user):
        current_month = datetime.date.today().month
        current_year = datetime.date.today().year

        despesas_cat = Transaction.objects.filter(cattegory__user=user).filter(
            cattegory__is_receita=False).filter(
            date__month=current_month).filter(date__year=current_year).values('cattegory__name').annotate(
            totals=Sum('total'))

        labels_cat = []
        data_cat = []
        for cat in despesas_cat:
            labels_cat.append(cat['cattegory__name'])
            data_cat.append(str(cat['totals']))

        return ({"labels": labels_cat, "data": data_cat})

from datetime import timedelta
import datetime
from time import timezone
from django.db.models import Sum
from .models import Transaction


def get_transactions_filter():
    return Transaction.objects.values('date__month', 'date__year').annotate(soma=Sum('total'))


class DateUtils:

    MONTHS = {
        '1': "Janeiro",
        '2': "Fevereiro",
        '3': "Março",
        '4': "Abril",
        '5': "Maio",
        '6': "Junho",
        '7': "Julho",
        '8': "Agosto",
        '9': "Setembro",
        '10': "Outubro",
        '11': "Novembro",
        '12': "Dezembro",
    }

    @staticmethod
    def get_previous_month_date(date):
        date.replace(day=15)
        date = date - timedelta(days=30)
        return date

    @staticmethod
    def get_next_month_date(date):
        date.replace(day=15)
        date = date + timedelta(days=30)
        return date

    @staticmethod
    def isValidDate(year=2022, month=1, day=15):
        try:
            date = datetime.date(year=year, month=month, day=day)
        except ValueError:
            return False
        return True
